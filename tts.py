import pyttsx3

def speak_text(text):
    """Converts text to speech with a different female voice."""
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty("voices")

    # Print available voices (for debugging)
    # for index, voice in enumerate(voices):
    #     print(f"{index}: {voice.name} - {voice.id}")

    # Try setting a different female voice
    female_voices = [voice for voice in voices if "female" in voice.name.lower()]
    
    if female_voices:
        engine.setProperty("voice", female_voices[-1].id)  # Choose a different female voice
    else:
        engine.setProperty("voice", voices[1].id)  # Fallback to the second voice

    engine.say(text)
    engine.runAndWait()
