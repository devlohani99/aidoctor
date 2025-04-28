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

def process_audio_file(audio_file, output_path):
    """
    Process uploaded audio file and convert it to the required format.
    
    Args:
    audio_file: The uploaded audio file object
    output_path (str): Path to save the processed audio file
    """
    try:
        # Save the uploaded file temporarily
        audio_segment = AudioSegment.from_file(audio_file)
        audio_segment.export(output_path, format="mp3", bitrate="128k")
        logging.info(f"Audio saved to {output_path}")
        return True
    except Exception as e:
        logging.error(f"An error occurred while processing audio: {e}")
        return False

def transcribe_with_groq(GROQ_API_KEY, audio_filepath, stt_model="whisper-large-v3"):
    """
    Transcribe audio file using Groq API.
    
    Args:
    GROQ_API_KEY (str): API key for Groq
    audio_filepath (str): Path to the audio file
    stt_model (str): Model to use for transcription
    
    Returns:
    str: Transcribed text
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return "Error transcribing audio"

audio_filepath="patient_voice_test_for_patient.mp3"
#record_audio(file_path=audio_filepath)

#Step2: Setup Speech to text–STT–model for transcription
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model="whisper-large-v3"
