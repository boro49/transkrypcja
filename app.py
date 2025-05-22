#!/usr/bin/env python3
"""
MP3 → tekst w Streamlit.
"""

from pathlib import Path
import tempfile
import streamlit as st
import whisper


@st.cache_resource(show_spinner=False)
def load_model(size: str = "small") -> whisper.Whisper:
    """Pobierz model Whisper wybranego rozmiaru."""
    return whisper.load_model(size)


def transcribe(mp3_bytes: bytes, model_size: str) -> str:
    """Zamień MP3 (bytes) na tekst."""
    model = load_model(model_size)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(mp3_bytes)
        tmp_path = Path(tmp.name)

    result = model.transcribe(str(tmp_path))
    tmp_path.unlink()          # sprzątnij plik tymczasowy
    return result["text"]


st.title("Transkryptor MP3")

model_size = st.selectbox(
    "Model",
    ["tiny", "base", "small", "medium", "large"],
    index=2,
)

mp3_file = st.file_uploader("Wrzuć plik MP3", type="mp3")

if mp3_file:
    with st.spinner("Transkrypcja..."):
        text = transcribe(mp3_file.read(), model_size)

    st.success("Gotowe")
    st.text_area("Tekst", value=text, height=300)
    st.download_button("Pobierz .txt", text, file_name="transkrypt.txt")

