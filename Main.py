import streamlit as st
from st_on_hover_tabs import on_hover_tabs
from feedback import feedback_main
from PIL import Image

def embed_iframe(url):
    iframe_code = f'''
    <style>
    .embed-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }}
    </style>
    <div class='embed-container'>
        <iframe src="{url}" frameborder="0" allowfullscreen></iframe>
    </div>
    '''
    st.markdown(iframe_code, unsafe_allow_html=True)

st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.header("Crime Analysis Dashboard")
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

image = Image.open("1.jpg")
image = image.resize((1200, 200))  # Set custom width and height

with st.sidebar:
    tabs = on_hover_tabs(tabName=['DashBoard', 'Forecast', 'Patrolling', 'Video Analysis', 'Victim Analysis', 'Map Analysis', 'Chatbot', 'Feedback'],
                         iconName=['dashboard', 'graph-up-arrow', 'radar', 'camera-reels', 'person-bounding-box', 'globe-central-south-asia', 'chat-left-dots-fill', 'pencil-square'],
                         default_choice=0)

if tabs == 'DashBoard':
    st.image(image, use_column_width=True)
    embed_iframe("https://frontpage-ksp.streamlit.app/?embed=true")

elif tabs == 'MapView':
    st.title('Map View')
    embed_iframe("http://ksp-data.s3-website-us-east-1.amazonaws.com")

elif tabs == 'Video Analysis':
    st.title("Video Analysis")
    embed_iframe("https://video-crime.streamlit.app/?embed=true")

elif tabs == 'Forecast':
    st.title('Crime Forecast')
    embed_iframe("https://forecast-ksp.streamlit.app/?embed=true")

elif tabs == 'Victim Analysis':
    st.title('Victim Analysis')
    embed_iframe("https://victim-ksp.streamlit.app/?embed=true")

elif tabs == 'Chatbot':
    st.title('Crime Chatbot')
    embed_iframe("https://chatbot-ksp.streamlit.app/?embed=true")

elif tabs == 'Map Analysis':
    st.title('Map Analysis')
    embed_iframe("https://map-ksp.streamlit.app/?embed=true")

elif tabs == 'Feedback':
    feedback_main()
