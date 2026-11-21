
import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

text = (
    "But perhaps you hate a thing and it is good for you, "
    "and perhaps you love a thing and it is bad for you. "
    "And Allah knows, while you know not."
)

print("Text-to-Speech is starting...")

engine.say(text)
engine.runAndWait()

print("Text-to-Speech finished.")
