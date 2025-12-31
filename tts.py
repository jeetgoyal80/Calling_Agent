import pyttsx3
import time

def speak(text, pause=0.5):
    print("🔊 System:", text)

    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    # Force voice selection (important on Windows)
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

    time.sleep(pause)
