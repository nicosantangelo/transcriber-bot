# pylint: disable=missing-module-docstring, missing-function-docstring
from faster_whisper import WhisperModel

MODEL_NAME = "large-v2"
FAST_WHISPER_MODEL = WhisperModel(MODEL_NAME, compute_type="int8")


def transcribe(audio_path: str):
    print("Transcribing", audio_path)

    segments, _ = FAST_WHISPER_MODEL.transcribe(
        audio=audio_path, language="es", without_timestamps=True, vad_filter=True
    )

    return segments
