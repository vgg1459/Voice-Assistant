import whisper
import soundfile as sf
import io
import base64
import streamlit as st
# from kokoro import KPipeline
from kokoro_onnx import Kokoro

model = whisper.load_model("small")
# tts_pipeline = KPipeline(lang_code='a')

def load_kokoro():
    return Kokoro("source/models/kokoro-v1.0.onnx", "source/models/voices-v1.0.bin")

kokoro = load_kokoro()

def transcribe_audio(file_path: str) -> str:
    result = model.transcribe(
        str(file_path),
        task="translate",
        language="en",
        verbose=False
    )
    text = result["text"]
    print(f"Transcription: {text}")
    return text

# def speak_text(text: str, voice='af_heart'):
#     generator = tts_pipeline(text, voice=voice)
#
#     for _, (_, _, audio_tensor) in enumerate(generator):
#         audio_np = audio_tensor.detach().cpu().numpy()
#
#         buf = io.BytesIO()
#         sf.write(buf, audio_np, 24000, format='WAV')
#         buf.seek(0)
#         audio_bytes = buf.read()
#
#         b64_audio = base64.b64encode(audio_bytes).decode()
#
#         js = f"""
#         <script>
#         (function() {{
#             const audio = new Audio("data:audio/wav;base64,{b64_audio}");
#             audio.play().catch(err => console.log("Autoplay blocked:", err));
#         }})();
#         </script>
#         """
#         st.components.v1.html(js, height=1, scrolling=False)


def speak_text(
    text: str,
    voice: str = "af_sarah",
    speed: float = 1.0,
    lang: str = "en-us"
):
    if not text.strip():
        return

    # Generate audio
    samples, sample_rate = kokoro.create(
        text,
        voice=voice,
        speed=speed,
        lang=lang
    )

    # Write WAV to memory
    buf = io.BytesIO()
    sf.write(buf, samples, sample_rate, format="WAV")
    buf.seek(0)

    # Base64 encode
    b64_audio = base64.b64encode(buf.read()).decode()

    js = f"""
    <script>
    (function() {{
        const audio = new Audio("data:audio/wav;base64,{b64_audio}");
        audio.play().catch(err => console.log("Autoplay blocked:", err));
    }})();
    </script>
    """

    st.components.v1.html(js, height=1, scrolling=False)
