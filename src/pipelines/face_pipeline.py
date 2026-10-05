import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students, get_student_pk

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec

def get_face_embeddings(image_np):
    try:
        detector, sp, facerec = load_dlib_models()

        if image_np.ndim == 3 and image_np.shape[2] == 4:
            image_np = image_np[:, :, :3]

        image_np = np.ascontiguousarray(image_np, dtype=np.uint8)
        faces = detector(image_np, 2)
        encodings = []

        for face in faces:
            shape = sp(image_np, face)
            face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
            encodings.append(np.array(face_descriptor))

        return encodings
    except Exception as e:
        st.error(f"Error extracting face embeddings: {e}")
        return []

def get_confidence_label(distance):
    if distance is None:
        return "Unknown"
    if distance <= 0.40:
        return "High Confidence"
    elif distance <= 0.52:
        return "Medium Confidence"
    elif distance <= 0.60:
        return "Low Confidence"
    else:
        return "Low Confidence"

@st.cache_resource
def get_trained_model():
    X = []
    Y = []

    student_db = get_all_students()
    if not student_db:
        return None

    for student in student_db:
        s_id = get_student_pk(student)
        embedding = student.get('face_embedding')
        if embedding and s_id is not None:
            X.append(np.array(embedding))
            Y.append(s_id)

    if len(X) == 0:
        return None

    clf = None
    if len(set(Y)) >= 2:
        try:
            clf = SVC(kernel='linear', probability=True, class_weight='balanced')
            clf.fit(X, Y)
        except Exception:
            clf = None

    return {'clf': clf, 'X': X, 'Y': Y}

def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}
    details = {}

    model_data = get_trained_model()
    if not model_data or not encodings:
        return {}, [], len(encodings), {}

    clf = model_data['clf']
    X_train = model_data['X']
    Y_train = model_data['Y']
    all_students = sorted(list(set(Y_train)))

    resemblance_threshold = 0.60

    for encoding in encodings:
        predicted_id = None
        if clf is not None and len(all_students) >= 2:
            try:
                predicted_id = clf.predict([encoding])[0]
            except Exception:
                predicted_id = None

        if predicted_id is None:
            distances = [np.linalg.norm(x - encoding) for x in X_train]
            min_idx = int(np.argmin(distances))
            predicted_id = Y_train[min_idx]
            best_match_score = distances[min_idx]
        else:
            matched_indices = [i for i, y in enumerate(Y_train) if y == predicted_id]
            distances = [np.linalg.norm(X_train[i] - encoding) for i in matched_indices]
            best_match_score = min(distances) if distances else 999.0

        if best_match_score <= resemblance_threshold:
            detected_students[predicted_id] = True
            details[predicted_id] = {
                'score': round(float(best_match_score), 3),
                'confidence_label': get_confidence_label(best_match_score)
            }

    return detected_students, all_students, len(encodings), details
