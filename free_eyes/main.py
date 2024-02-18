import speech_recognition as sr
from openai import OpenAI
from free_eyes.prompts.transcript_to_llm_input import transcript_to_llm_input_prompt
from dotenv import load_dotenv
from gtts import gTTS
import os

load_dotenv()

def listen_and_transcribe():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1  # Increase pause threshold to wait for longer pauses; adjust this value based on testing

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Please say something...")
        
        # Adjust the recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Capture the audio, allowing for a longer phrase time limit
        audio = recognizer.listen(source, phrase_time_limit=20)  # Increase phrase time limit as needed

    try:
        # Recognize speech using Google's speech recognition
        print("You said: " + recognizer.recognize_google(audio))
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        # Error: recognizer does not understand the audio
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        # Error: could not request results from Google's speech recognition service
        print(f"Could not request results from Google Speech Recognition service; {e}")

def main():
    # Run the function
    transcript = listen_and_transcribe()

    print(transcript_to_llm_input_prompt.format(transcript))

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": transcript_to_llm_input_prompt.format(transcript)}
        ]
    )

    print(completion.choices[0].message.content)

    prompt = completion.choices[0].message.content

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # for chunk in completion:
    #     print(chunk.choices[0].delta)

    print(completion.choices[0].message.content)

    response = completion.choices[0].message.content

    # Pass text to gtts module
    speech = gTTS(response, lang="fr")

    # Save the voice file
    speech.save("text.mp3")

    # Play the voice file
    os.system("start text.mp3")


main()