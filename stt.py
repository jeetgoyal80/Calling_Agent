import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import re

SAMPLE_RATE = 16000
DURATION = 9  # seconds (important for numbers)

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

    result = model.transcribe("audio/input.wav", language="hi")
    text = result["text"].strip()

    print("📝 Heard:", text)
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
