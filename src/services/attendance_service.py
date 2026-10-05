from src.database.db import (
    get_enrolled_students,
    get_student_pk,
    create_attendance_session,
    save_session_attendance
)

def prepare_session_review(subject_id, detected_student_ids, confidence_details=None):
    """
    Prepares student review state for an attendance session.
    - subject_id: target subject
    - detected_student_ids: set/list of student IDs identified by AI
    - confidence_details: dict of student_id -> {'score': X, 'confidence_label': Y}
    """
    if confidence_details is None:
        confidence_details = {}

    enrolled_students = get_enrolled_students(subject_id)
    detected_set = set(detected_student_ids or [])

    enrolled_map = {}
    default_status_map = {}
    detected_enrolled_ids = set()

    for student in enrolled_students:
        s_id = get_student_pk(student)
        enrolled_map[s_id] = student
        if s_id in detected_set:
            default_status_map[s_id] = "present"
            detected_enrolled_ids.add(s_id)
        else:
            default_status_map[s_id] = "absent"

    return {
        "enrolled_students": enrolled_students,
        "enrolled_map": enrolled_map,
        "detected_enrolled_ids": detected_enrolled_ids,
        "default_status_map": default_status_map,
        "confidence_details": confidence_details
    }

def finalize_and_save_session(subject_id, teacher_id, method, final_status_map, confidence_details=None):
    """
    Creates an attendance session and saves records for ALL enrolled students in the subject.
    - final_status_map: dict of student_id -> 'present' or 'absent'
    """
    if not subject_id or not teacher_id or not final_status_map:
        return False, "Missing required session parameters."

    session = create_attendance_session(subject_id, teacher_id, method=method)
    if not session:
        return False, "Failed to create attendance session in database."

    session_id = session.get("id")
    confidence_map = {}
    if confidence_details:
        for s_id, info in confidence_details.items():
            if isinstance(info, dict) and "score" in info:
                confidence_map[s_id] = info["score"]
            elif isinstance(info, (int, float)):
                confidence_map[s_id] = float(info)

    saved_records = save_session_attendance(
        session_id=session_id,
        records_dict=final_status_map,
        method=method,
        confidence_map=confidence_map
    )

    if saved_records is not None:
        return True, session
    else:
        return False, "Failed to save individual attendance records."
