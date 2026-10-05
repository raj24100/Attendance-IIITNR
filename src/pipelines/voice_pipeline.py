from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

DEFAULT_VOICE_THRESHOLD = 0.65

@st.cache_resource
def load_voice_encoder():
    try:
        return VoiceEncoder()
    except Exception as e:
        st.error(f"Error initializing Voice Encoder: {e}")
        return None

def get_voice_embedding(audio_bytes):
    if not audio_bytes:
        return None
    try:
        encoder = load_voice_encoder()
        if not encoder:
            return None

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        if len(audio) < sr * 0.5:
            st.warning("Audio sample too short (minimum 0.5 seconds required)")
            return None

        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f"Voice embedding error: {e}")
        return None

def identify_speaker(new_embedding, candidates_dict, threshold=DEFAULT_VOICE_THRESHOLD):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding:
            try:
                emb_arr = np.array(stored_embedding)
                new_arr = np.array(new_embedding)
                similarity = float(np.dot(new_arr, emb_arr))
                if similarity > best_score:
                    best_score = similarity
                    best_sid = sid
            except Exception:
                continue

    if best_score >= threshold:
        return best_sid, best_score

    return None, max(best_score, 0.0)

def process_bulk_audio(audio_bytes, candidates_dict, threshold=DEFAULT_VOICE_THRESHOLD):
    if not audio_bytes or not candidates_dict:
        return {}

    try:
        encoder = load_voice_encoder()
        if not encoder:
            return {}

        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        if len(audio) < sr * 0.5:
            st.warning("Bulk audio recording is too short.")
            return {}

        segments = librosa.effects.split(audio, top_db=30)
        identified_results = {}

        for start, end in segments:
            if (end - start) < sr * 0.5:
                continue

            segment_audio = audio[start:end]
            try:
                wav = preprocess_wav(segment_audio)
                embedding = encoder.embed_utterance(wav)
                sid, score = identify_speaker(embedding, candidates_dict, threshold)

                if sid:
                    if sid not in identified_results or score > identified_results[sid]:
                        identified_results[sid] = score
            except Exception:
                continue

        return identified_results
    except Exception as e:
        st.error(f"Bulk voice processing error: {e}")
        return {}