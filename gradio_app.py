# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr
import tempfile
import shutil
from pathlib import Path

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def text_to_speech(text):
    """Helper function to generate speech and return a valid file path"""
    try:
        # Create temporary file in system's temp directory
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            # Generate speech
            text_to_speech_with_elevenlabs(
                input_text=text,
                output_filepath=temp_file.name
            )
            return temp_file.name
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None

def process_inputs(audio_filepath, image_filepath):
    try:
        # Process speech to text
        speech_to_text_output = ""
        if audio_filepath:
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                audio_filepath=audio_filepath,
                stt_model="whisper-large-v3"
            )

        # Handle the query
        query = system_prompt
        if speech_to_text_output:
            query += " " + speech_to_text_output
        
        doctor_response = analyze_image_with_query(
            query=query,
            model="llama-3.3-70b-versatile",
            encoded_image=None  # Not using image for now since we're using text-only model
        )

        # Generate audio output
        audio_path = text_to_speech(doctor_response)
        if not audio_path or not os.path.exists(audio_path):
            raise Exception("Failed to generate audio response")

        return speech_to_text_output, doctor_response, audio_path

    except Exception as e:
        print(f"Error in process_inputs: {str(e)}")
        return str(e), str(e), None

# Create the interface with proper configuration
with gr.Blocks(
    theme=gr.themes.Default(),
    css="""
        .gradio-container {
            max-width: 900px !important;
            margin: 0 auto;
            background-color: white !important;
        }
        footer {display: none !important}
        body {background-color: white !important}
        .main {background-color: white !important}
        .contain {background-color: white !important}
        .gap {background-color: white !important}
        .gr-interface {background-color: white !important}
        .gr-form {background-color: white !important}
        .gr-group {background-color: white !important}
        .gr-box {background-color: white !important}
    """
) as demo:
    gr.Markdown("# AI Doctor")
    gr.Markdown("Upload an image and/or speak to get medical analysis")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Record Audio"
            )
            image_input = gr.Image(
                type="filepath",
                label="Upload Image"
            )
            
        with gr.Column():
            text_output = gr.Textbox(
                label="Speech to Text",
                interactive=False
            )
            response_output = gr.Textbox(
                label="Doctor's Response",
                interactive=False
            )
            audio_output = gr.Audio(
                label="Doctor's Voice",
                interactive=False,
                format="mp3"
            )
    
    submit_btn = gr.Button("Analyze")
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[text_output, response_output, audio_output],
        api_name="process"
    )

# Launch with proper configuration
if __name__ == "__main__":
    try:
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            debug=True,
            show_error=True,
            show_api=False
        )
    except Exception as e:
        print(f"Error launching interface: {str(e)}")
    finally:
        # Clean up any temporary files
        temp_dir = tempfile.gettempdir()
        for file in os.listdir(temp_dir):
            if file.endswith(".mp3"):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass

#http://127.0.0.1:7860