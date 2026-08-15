"""
Voice Assistant (Beginner Tier)
-----------------------------------
A simple voice-controlled assistant that listens via the microphone,
understands a small set of commands, and replies using text-to-speech.

Supported commands:
    "hello"                     -> predefined greeting
    "what time is it" / "date"  -> tells current time / date
    "search for <topic>"        -> opens a browser search for <topic>
    "exit" / "quit" / "stop"    -> ends the program

Setup:
    pip install SpeechRecognition pyttsx3 pyaudio
    (On Linux you may also need: sudo apt-get install portaudio19-dev)

Run:
    python voice_assistant.py
"""

import datetime
import webbrowser

import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)


def speak(text: str):
    """Speak text out loud and print it, so the interaction is visible too."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    """Capture audio from the microphone and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat it?")
        return ""
    except sr.RequestError:
        speak("I'm having trouble reaching the speech recognition service.")
        return ""


def handle_command(command: str) -> bool:
    """
    Process a recognized command.
    Returns False if the assistant should stop, True to keep listening.
    """
    if not command:
        return True

    if "hello" in command:
        speak("Hello! How can I help you today?")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    elif "search for" in command:
        topic = command.split("search for", 1)[1].strip()
        if topic:
            speak(f"Searching the web for {topic}")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        else:
            speak("What would you like me to search for?")

    elif any(word in command for word in ("exit", "quit", "stop")):
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("I don't know that command yet. Try: hello, time, date, "
              "'search for <topic>', or 'exit'.")

    return True


def main():
    speak("Voice assistant ready. Say 'hello' to begin, or 'exit' to quit.")
    running = True
    while running:
        command = listen()
        running = handle_command(command)


if __name__ == "__main__":
    main()
