# stt.py
# Robust Whisper STT tuned for Indian Hinglish / Hindi / Urdu
# Reduces hallucinations & mixed-script garbage

import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import re

SAMPLE_RATE = 16000
DURATION = 11  # longer window helps Indian speech

model = whisper.load_model("base")


def speech_to_text():
    print("\n🎤 Listening... Speak now")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )
    sd.wait()

    write("audio/input.wav", SAMPLE_RATE, recording)

    result = model.transcribe(
        "audio/input.wav",
        # 🔥 KEY FIXES
        language=None,                   # auto-detect (CRITICAL)
        temperature=0.0,                 # stop hallucination
        beam_size=5,
        best_of=5,
        condition_on_previous_text=False,
        initial_prompt=(
            "Indian student speaking Hindi, Hinglish or Urdu "
            "about hostel room problems like light, fan, water."
        )
    )

    text = result["text"].strip()
    text = normalize_text(text)

    print("📝 Heard:", text)
    return text


def normalize_text(text: str) -> str:
    """
    Remove garbage tokens & keep Indian scripts
    """
    text = text.lower()

    # keep English + Hindi + Urdu
    text = re.sub(
        r"[^\w\s\u0900-\u097F\u0600-\u06FF]",
        " ",
        text
    )

    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_digits(text: str) -> str:
    digit_map = {
        "zero": "0", "one": "1", "two": "2", "three": "3",
        "four": "4", "five": "5", "six": "6",
        "seven": "7", "eight": "8", "nine": "9"
    }

    text = text.lower()
    for word, num in digit_map.items():
        text = text.replace(word, num)

    digits = re.findall(r"\d", text)
    return "".join(digits)
