from dotenv import load_dotenv
load_dotenv()

#Step1: Setup Audio recorder (ffmpeg & portaudio)
# ffmpeg, portaudio, pyaudio
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_audio_file(uploaded_file, output_path):
    try:
        # Read the uploaded file into memory
        audio_bytes = uploaded_file.read()
        
        # Convert to AudioSegment
        audio = AudioSegment.from_file(BytesIO(audio_bytes))
        
        # Export as wav for speech recognition
        audio.export(output_path, format="wav")
        return True
    except Exception as e:
        logging.error(f"Error processing audio file: {str(e)}")
        return False

def transcribe_with_groq(GROQ_API_KEY, audio_filepath, stt_model="whisper-large-v3"):
    try:
        # Initialize recognizer
        r = sr.Recognizer()
        
        # Load the audio file
        with sr.AudioFile(audio_filepath) as source:
            # Record the audio
            audio = r.record(source)
            
            # Use Google's speech recognition (free and reliable)
            text = r.recognize_google(audio)
            return text
    except Exception as e:
        logging.error(f"Error in speech recognition: {str(e)}")
        return "Could not transcribe audio. Please try again."

audio_filepath="patient_voice_test_for_patient.mp3"
#record_audio(file_path=audio_filepath)

#Step2: Setup Speech to text–STT–model for transcription
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model="whisper-large-v3"
