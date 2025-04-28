import streamlit as st
import os
from dotenv import load_dotenv
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import process_audio_file, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs
from audio_recorder_streamlit import audio_recorder
from io import BytesIO

# Load environment variables
load_dotenv()

# Create temp directory if it doesn't exist
os.makedirs("temp", exist_ok=True)

# Set page config
st.set_page_config(page_title="AI Doctor", layout="wide")

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .stApp {
        max-width: 1000px;
        margin: 0 auto;
    }
    .audio-recorder {
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("AI Doctor")
st.markdown("Record your symptoms or upload an image for analysis")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Audio recording
    st.write("Record your symptoms:")
    audio_bytes = audio_recorder()
    
    # Image input
    image_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

with col2:
    if st.button("Analyze"):
        if audio_bytes is not None or image_file:
            with st.spinner("Processing..."):
                # Process speech to text
                speech_to_text_output = ""
                if audio_bytes is not None:
                    # Save temporary audio file
                    temp_audio_path = "temp/input_audio.wav"
                    with open(temp_audio_path, "wb") as f:
                        f.write(audio_bytes)
                    
                    if os.path.exists(temp_audio_path):
                        speech_to_text_output = transcribe_with_groq(
                            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                            audio_filepath=temp_audio_path,
                            stt_model="whisper-large-v3"
                        )
                        st.text_area("Your recorded message:", speech_to_text_output, height=100)
                    
                    # Clean up temp file
                    if os.path.exists(temp_audio_path):
                        os.remove(temp_audio_path)

                # Process image if provided
                if image_file:
                    # Save temporary image file
                    temp_image_path = "temp/input_image.jpg"
                    with open(temp_image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                    
                    # Analyze image
                    doctor_response = analyze_image_with_query(
                        query=speech_to_text_output,
                        model="llama-3.3-70b-versatile",
                        encoded_image=encode_image(temp_image_path)
                    )
                    st.text_area("Doctor's Response", doctor_response, height=150)
                    
                    # Generate audio response
                    if doctor_response:
                        with st.spinner("Generating voice response..."):
                            audio_path = "temp/response.mp3"
                            voice_path = text_to_speech_with_elevenlabs(
                                input_text=doctor_response,
                                output_filepath=audio_path
                            )
                            
                            # Play audio if generated successfully
                            if voice_path and os.path.exists(voice_path):
                                with open(voice_path, "rb") as f:
                                    st.audio(f.read(), format="audio/mp3")
                    
                    # Clean up temp files
                    for temp_file in [temp_image_path, "temp/response.mp3"]:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
        else:
            st.warning("Please record your symptoms or upload an image to analyze") 