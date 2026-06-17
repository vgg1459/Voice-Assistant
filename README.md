# NLS Voice Assistant

A fully offline voice assistant pipeline — no cloud APIs, no external dependencies at runtime.
Integrates Whisper for speech-to-text, Qwen 2.5 7B (via Ollama) for LLM reasoning,
and Kokoro TTS for text-to-speech, served through a Streamlit UI.

## Stack

- **STT** — OpenAI Whisper (small)
- **LLM** — Qwen 2.5 7B Instruct via Ollama
- **TTS** — Kokoro ONNX (kokoro-v1.0)
- **UI** — Streamlit
- **Containerization** — Docker (all-in-one)

## Run with Docker

```bash
docker run --rm -p 8501:8501 \
  -e OLLAMA_MODEL=qwen2.5:7b-instruct \
  -e PYTHONPATH=/app/source \
  nls-voice-assistant:allinone
```

Open http://localhost:8501 in your browser.

> On first launch, Ollama (~4–5 GB) and Whisper (~461 MB) models download automatically.
> This happens once; subsequent runs are fully local.

## Run without Docker

1. Install dependencies: `pip install -r requirements.txt`
2. Download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from
   [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) and place in `source/models/`
3. Install [Ollama](https://ollama.com), pull your model (`ollama pull qwen2.5:7b-instruct`),
   and ensure it's running locally
4. Launch: `streamlit run ui.py`
