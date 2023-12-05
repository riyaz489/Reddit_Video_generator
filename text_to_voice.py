import pyttsx3

from config import VOICE_RATE, VOICE_VOLUME


def text_to_speech(text, output_file):
    engine = pyttsx3.init()
    engine.setProperty('rate', VOICE_RATE)
    engine.setProperty('volume', VOICE_VOLUME)
    engine.save_to_file(text, output_file)

    # engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    text_to_speech("Hello, this is a text-to-speech example using Python.")


