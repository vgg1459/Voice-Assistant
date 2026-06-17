# NLS Voice Assistant (All-in-One)

A streamlined, containerized voice assistant that integrates **Ollama** for intelligent reasoning, **Whisper** for robust speech-to-text, and **Streamlit** for a clean user interface.

## 🚀 How to Run (For Evaluation)
Follow these steps to build and launch the assistant. Ensure you have [Docker](https://www.docker.com/) installed on your machine.

The image provided have already been built so please run the below command:
Here is a professionally formatted README.md based on your specific Dockerfile and setup. It uses the "Small File / Automatic Download" approach so your professor gets a lightweight .tar file.

NLS Voice Assistant (Evaluation)
A containerized AI Voice Assistant featuring Ollama (Qwen 2.5), OpenAI Whisper, and Streamlit. This assistant provides high-fidelity speech-to-text and LLM reasoning in a single "All-in-One" Docker environment.

1. Load the Image
Load the provided image file into your local Docker environment:

```
docker load -i nls_assistant_full.tar
```

2. Start the Application
Run the following command to launch the integrated Ollama and Streamlit servers:

```bash
docker run --rm -p 8501:8501 \
  -e OLLAMA_MODEL=qwen2.5:7b-instruct \
  -e PYTHONPATH=/app/source \
  nls-voice-assistant:allinone
  ```

3. Open the Dashboard
Once the container initialization is complete, open your web browser and go to: 👉 http://localhost:8501


## Important: First Run Initialization
During the initial launch, the container will automatically download the necessary AI models. This process is required for local inference and will happen only once:

Ollama Model (qwen2.5:7b-instruct): ~4–5 GB
Whisper Model (small): ~461 MB

Note: This may take several minutes depending on your internet speed. This is expected behavior and ensures the assistant runs locally thereafter.



**Steps to Run without Docker:**
1. Pip install -r requirements.txt
2. Download these two files and store in Source/Models : kokoro-v1.0.onnx and voices-v1.0.bin from here: https://github.com/thewh1teagle/kokoro-onnx
3. Install ollama and pull a llm model and make sure its running on local
4. use Command : streamlit run ui.py to launch UI.
