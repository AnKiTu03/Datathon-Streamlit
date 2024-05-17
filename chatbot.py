import streamlit as st
import os
from dotenv import load_dotenv
from s3 import read_files_from_s3
from io import BytesIO
import google.generativeai as genai
from pandasai import SmartDatalake
import requests
import pandas as pd

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv('GEN_AI')

gen_api = os.getenv('GEN_AI')
pandasai_api_key = os.getenv('PANDASAI_API_KEY')
os.environ['PANDASAI_API_KEY'] = pandasai_api_key
rapidapi_key = os.getenv('RAPIDAPI_KEY')

# Configure Google Generative AI
genai.configure(api_key=gen_api)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def trans(txt):
    url = "https://microsoft-translator-text.p.rapidapi.com/translate"
    querystring = {"to[0]": "kn", "api-version": "3.0", "profanityAction": "NoAction", "textType": "plain"}
    payload = [{"Text": txt}]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    if response.status_code == 200:
        parsed_data = response.json()
        translated_text = parsed_data[0]['translations'][0]['text']
        return translated_text
    else:
        return "Server Limit Exceeded"

def chat_with_data():
    data_frames = load_data_from_s3()
    data = data_frames['FIR_Details_Data.csv']
    lake = SmartDatalake([data])

    llm = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    st.title("Data Chat Bot Interface")
    st.header("Chat with Data")
    bu = st.checkbox("Kannada")

    user_input = st.text_input("Ask a question about the data:")

    if user_input:
        try:
            with st.spinner("Processing your question..."):
                r = lake.chat(user_input)
                Human_prompt = f"Given the question {user_input}, you will receive an answer {r} from the Database. Frame a user-friendly response using this."
                
                response = llm.generate_content(Human_prompt)
                response = response.text
                if bu:
                    response = trans(response)
                
            st.text_area("Bot Response:", value=response, height=300)
        except Exception as e:
            st.error(f"Error processing your question: {e}")
    else:
        st.write("Please enter a question to start chatting.")




@st.cache_data()
def load_data_from_s3():
    bucket_name = 'new-trail01'
    file_keys = ['FIR_Details_Data.csv']
    return read_files_from_s3(bucket_name, file_keys)



