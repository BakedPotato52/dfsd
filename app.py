try:
    import speech_recognition as sr
except ModuleNotFoundError:
    print("Error: The 'speech_recognition' module is not installed. Install it using 'pip install SpeechRecognition'.")
    exit()

try:
    import spacy
except ModuleNotFoundError:
    print("Error: The 'spacy' module is not installed. Install it using 'pip install spacy' and download the model with 'python -m spacy download en_core_web_sm'.")
    exit()

from gtts import gTTS
import os

# Initialize Spacy NLP (Ensure the model is downloaded)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Error: The Spacy language model 'en_core_web_sm' is not available. Download it using 'python -m spacy download en_core_web_sm'.")
    exit()

def audio_to_text():
    """Capture audio input and convert it to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Request Error: {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out.")
    return ""

def parse_to_isl(text):
    """Convert the text to a simplified ISL grammar structure."""
    if not text.strip():
        print("Error: No input text provided for ISL parsing.")
        return ""

    doc = nlp(text)
    isl_structure = []

    for token in doc:
        # Simplistic rule: Add nouns and verbs directly in order
        if token.pos_ in ["NOUN", "VERB", "PRON"]:
            isl_structure.append(token.text)

    if not isl_structure:
        isl_structure.append("No ISL grammar generated from input.")

    isl_sentence = " ".join(isl_structure)
    print(f"ISL Grammar Output: {isl_sentence}")
    return isl_sentence

def text_to_speech(text, n):
    """Convert text to speech for confirmation or narration."""
    if not text.strip():
        print("Error: No text to convert to speech.")
        text = "No valid ISL grammar to convert to speech."

    tts = gTTS(text=text, lang='en')
    tts.save(f"content/output.mp3")
    os.system(f"start content/output.mp3" if os.name == "nt" else f"xdg-open output{n}.mp3")

def main():
    """Main program to orchestrate the process."""
    print("Audio-to-Sign Language Translator\n")

    # Counter for output files
    output_counter = 1

    # Step 1: Audio to Text
    text = audio_to_text()
    if not text:
        print("Failed to capture audio input.")
        return

    # Step 2: Text to ISL Grammar
    isl_output = parse_to_isl(text)

    # Step 3: Text-to-Speech for ISL Grammar Output (Optional)
    text_to_speech(isl_output, output_counter)
    output_counter += 1

    # Future Step: Sign Language Animation (requires ISL dataset and avatar rendering)
    print("Future Scope: Generate ISL signs using a signing avatar.")

if __name__ == "__main__":
    main()

