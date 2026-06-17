import streamlit as st
from audiorecorder import audiorecorder
from source.main import transcribe_audio, speak_text
import os
from source.util.process_query import get_calendar_or_chat

st.set_page_config(page_title="Voice Assistant UI", page_icon="🎤")

st.markdown('<div class="centered">', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_placeholder = st.empty()

def render_chat():
    with chat_placeholder.container():
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            st.write(msg)
        st.markdown('</div>', unsafe_allow_html=True)

render_chat()

audio = audiorecorder("🎤 Speak", "⏹ Stop")

def analyze_text(user_text: str) -> str:
    # text_lower = user_text.lower()
    reply = get_calendar_or_chat(user_text)
    return reply

if len(audio) > 0:
    os.makedirs("source/uploads", exist_ok=True)
    wav_file = os.path.join("source/uploads", "recording.wav")
    audio.export(wav_file, format="wav")

    st.session_state.messages.append("Transcribing...")
    render_chat()

    text = transcribe_audio(wav_file)

    if st.session_state.messages[-1] == "Transcribing...":
        st.session_state.messages.pop()

    st.session_state.messages.append(f"User: {text}")
    render_chat()

    st.session_state.messages.append("Analyzing...")
    render_chat()

    assistant_reply = analyze_text(text)
    if assistant_reply:
        if st.session_state.messages[-1] == "Analyzing...":
            st.session_state.messages.pop()
        st.session_state.messages.append(f"Assistant: {assistant_reply}")
        render_chat()
        speak_text(assistant_reply)

    if os.path.exists(wav_file):
        os.remove(wav_file)