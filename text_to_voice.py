import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', engine.getProperty('rate')-30)
    engine.setProperty('volume', engine.getProperty('volume')+2)
    engine.save_to_file(text, 'temp_audio.mp3')

    # engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text_to_speech("Hello, this is a text-to-speech example using Python.")


