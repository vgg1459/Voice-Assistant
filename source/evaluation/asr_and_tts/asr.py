import whisper
from pathlib import Path

print("Loading Whisper model...")
model = whisper.load_model("small")


def transcribe_audio(wav_path: str | Path) -> str:
    """
    Transcribe an existing WAV file.
    NO recording. NO file writing.
    """
    result = model.transcribe(str(wav_path))
    return result["text"].strip().lower()
