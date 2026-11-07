
import io
import os

import librosa
import numpy as np
import streamlit as st
from resemblyzer import VoiceEncoder, preprocess_wav


# ============================================================
# 1. LOAD THE VOICE ENCODER
# ============================================================
# VoiceEncoder converts a voice recording into a numerical
# vector called an embedding.
#
# An embedding represents voice characteristics and can be
# compared with stored embeddings to identify a speaker.
#
# @st.cache_resource prevents the model from loading again
# every time Streamlit reruns the application.
# ============================================================

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


# ============================================================
# 2. GENERATE A VOICE EMBEDDING
# ============================================================
# audio_bytes: Audio file received from Streamlit or another
#              source as bytes.
#
# Returns: A list of numbers representing the voice.
# Returns None if processing fails.
# ============================================================

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        # Load audio as mono at 16,000 samples per second.
        # sr=16000 resamples the audio to the required rate.
        # mono=True converts stereo audio into one channel.
        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        # Remove unnecessary silence and prepare the waveform.
        # source_sr tells preprocess_wav the current sample rate.
        wav = preprocess_wav(audio, source_sr=sr)

        # Convert the prepared voice into an embedding vector.
        embedding = encoder.embed_utterance(wav)

        # Convert NumPy values into a regular Python list
        # so the embedding can be stored as JSON if needed.
        return embedding.tolist()

    except Exception as e:
        # Display the actual error to help with debugging.
        st.error(f"Voice recognition error: {e}")
        return None


# ============================================================
# 3. IDENTIFY A SPEAKER
# ============================================================
# new_embedding: Embedding of the newly recorded voice.
#
# candidates_dict: Dictionary containing previously stored
#                  speaker IDs and their voice embeddings.
#
# threshold: Minimum similarity score required for a match.
# ============================================================

def identify_speaker(new_embedding, candidates_dict, threshold=0.65):

    # If no voice embedding or registered speakers exist,
    # identification cannot be performed.
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    # Convert embeddings to NumPy arrays for mathematical
    # operations such as dot product.
    new_embedding = np.asarray(new_embedding, dtype=np.float32)

    # Track the speaker with the highest similarity.
    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():

        # Skip speakers whose embeddings are missing.
        if stored_embedding is None:
            continue

        stored_embedding = np.asarray(
            stored_embedding,
            dtype=np.float32
        )

        # Embeddings must have matching dimensions and
        # contain finite numerical values.
        if (
            stored_embedding.shape != new_embedding.shape
            or not np.all(np.isfinite(stored_embedding))
            or not np.all(np.isfinite(new_embedding))
        ):
            continue

        # Resemblyzer normally produces normalized embeddings.
        # Their dot product is therefore cosine similarity.
        similarity = float(np.dot(new_embedding, stored_embedding))

        # Update the best match when a higher score is found.
        if similarity > best_score:
            best_score = similarity
            best_sid = sid

    # Accept the best speaker only when the score meets
    # the configured threshold.
    if best_sid is not None and best_score >= threshold:
        return best_sid, best_score

    # None means that no candidate met the threshold.
    return None, best_score if best_sid is not None else 0.0


# ============================================================
# 4. PROCESS LONG OR BULK AUDIO
# ============================================================
# This function splits a longer recording into non-silent
# segments and attempts to identify the speaker in each one.
#
# IMPORTANT:
# Non-silent segments are NOT guaranteed to contain only one
# speaker. Overlapping voices can produce incorrect matches.
# ============================================================

def process_bulk_audio(audio_bytes, candidates_dict, threshold=0.65):
    try:
        encoder = load_voice_encoder()

        # Resample the recording to 16 kHz mono audio.
        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True
        )

        # Split audio around silent portions.
        # top_db=30 controls the silence detection sensitivity.
        segments = librosa.effects.split(audio, top_db=30)

        # Stores the highest similarity score for each speaker.
        identified_results = {}

        for start, end in segments:

            # Ignore segments shorter than 0.5 seconds.
            # Very short clips may not contain enough voice data.
            if (end - start) < int(sr * 0.5):
                continue

            # Extract the current audio segment.
            segment_audio = audio[start:end]

            # Prepare the segment before generating its embedding.
            wav = preprocess_wav(segment_audio, source_sr=sr)

            # Generate the voice embedding for this segment.
            embedding = encoder.embed_utterance(wav)

            # Compare the embedding with registered speakers.
            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            # Keep the best score if the same speaker appears
            # in multiple segments.
            if sid is not None:
                if (
                    sid not in identified_results
                    or score > identified_results[sid]
                ):
                    identified_results[sid] = score

        # Example output:
        # {"student_101": 0.82, "student_102": 0.74}
        return identified_results

    except Exception as e:
        # Report the actual exception instead of hiding it.
        st.error(f"Bulk audio processing error: {e}")
        return {}
