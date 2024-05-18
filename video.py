import streamlit as st
import cv2
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
gen_api = os.getenv('GEN_AI')

# Function to configure Google Generative AI
def configure_genai(api_key):
    genai.configure(api_key=api_key)

# Function to extract and process frames from video
def extract_frame_from_video(video_file_path, frame_prefix, genai_client, prompt):
    vidcap = cv2.VideoCapture(video_file_path)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))
    frame_interval = fps * 2  # 2 seconds
    frame_count = 0
    count = 0

    with st.spinner("Processing video..."):
        while vidcap.isOpened():
            success, frame = vidcap.read()
            if not success:
                break
            if count % frame_interval == 0:  # Extract 1 frame every 2 seconds
                frame_count += 1
                image_name = f"{frame_prefix}{frame_count}.jpg"
                success, encoded_image = cv2.imencode('.jpg', frame)
                if success:
                    # Directly upload the frame without saving it
                    response = genai_client.upload_file(content=encoded_image.tobytes(), filename=image_name)
                    process_frame(response, prompt, genai_client)
            count += 1
    vidcap.release()

# Function to process each frame using Generative AI
def process_frame(response, prompt, genai_client):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    request = [prompt, response]
    response = model.generate_content(request, request_options={"timeout": 600})
    st.markdown(f"""<div style="background-color: #dceefb; padding: 10px; border-radius: 5px; color: black;">{response.text}</div>""", unsafe_allow_html=True)

def video_main():
    st.title("Crime Video Analysis")

    gen_api = os.getenv('GEN_AI')
    if gen_api:
        configure_genai(gen_api)

    video_file = st.file_uploader("Upload a video file:", type=["mp4", "avi", "mov"])
    if video_file:
        video_path = os.path.join("/tmp", video_file.name)
        with open(video_path, 'wb') as f:
            f.write(video_file.read())
        st.video(video_path)

        frame_prefix = "_frame"

        prompt = ("You are a crime scene investigator analyzing a crime scene.Describe the crime happening in the video. Give me a detailed report of the crime in 100-200 words. Don't include the date, time, or location unless there is a clear idea about it. Keep it formal and professional.")

        if prompt:
            extract_frame_from_video(video_path, frame_prefix, genai, prompt)

if __name__ == '__main__':
    video_main()
