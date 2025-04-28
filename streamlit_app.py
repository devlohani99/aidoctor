import streamlit as st
import os
from dotenv import load_dotenv
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# Load environment variables
load_dotenv()

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
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("AI Doctor")
st.markdown("Upload an image and/or record audio to get medical analysis")

# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Audio input
    audio_file = st.file_uploader("Record or Upload Audio", type=['wav', 'mp3'])
    
    # Image input
    image_file = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])

with col2:
    if st.button("Analyze"):
        if audio_file or image_file:
            with st.spinner("Processing..."):
                # Process speech to text
                speech_to_text_output = ""
                if audio_file:
                    # Save temporary audio file
                    with open("temp_audio.wav", "wb") as f:
                        f.write(audio_file.getbuffer())
                    
                    speech_to_text_output = transcribe_with_groq(
                        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                        audio_filepath="temp_audio.wav",
                        stt_model="whisper-large-v3"
                    )
                    st.text_area("Speech to Text", speech_to_text_output, height=100)
                    
                    # Clean up temp file
                    if os.path.exists("temp_audio.wav"):
                        os.remove("temp_audio.wav")

                # Process image if provided
                if image_file:
                    # Save temporary image file
                    with open("temp_image.jpg", "wb") as f:
                        f.write(image_file.getbuffer())
                    
                    # Analyze image
                    doctor_response = analyze_image_with_query(
                        query=speech_to_text_output,
                        model="llama-3.3-70b-versatile",
                        encoded_image=encode_image("temp_image.jpg")
                    )
                    st.text_area("Doctor's Response", doctor_response, height=150)
                    
                    # Generate audio response
                    with st.spinner("Generating voice response..."):
                        audio_path = "temp_response.mp3"
                        voice_path = text_to_speech_with_elevenlabs(
                            input_text=doctor_response,
                            output_filepath=audio_path
                        )
                        
                        # Play audio if generated successfully
                        if os.path.exists(voice_path):
                            with open(voice_path, "rb") as f:
                                st.audio(f.read(), format="audio/mp3")
                    
                    # Clean up temp files
                    for temp_file in ["temp_image.jpg", "temp_response.mp3"]:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
        else:
            st.warning("Please upload an audio file or image to analyze") 