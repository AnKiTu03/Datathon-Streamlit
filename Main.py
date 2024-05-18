import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from feedback import feedback_main
from PIL import Image

def embed_iframe(url, height=800, width=1200):
    iframe_code = f'<iframe src="{url}" height="{height}" width="{width}" style="border:none;" scrolling="no"></iframe>'
    st.markdown(iframe_code, unsafe_allow_html=True)

st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
image = Image.open("1.jpg")
image = image.resize((1200, 200))  # Set custom width and height
st.image(image, use_column_width=True)

# Sidebar with navigation menu
with st.sidebar:
    selected = option_menu("Main Menu", 
                           ['DashBoard', 'Forecast', 'Patrolling', 'Video Analysis', 'Victim Analysis', 'Map Analysis', 'Chatbot', 'Feedback'],
                           icons=['bar-chart', 'graph-up-arrow', 'radar', 'camera-reels', 'person-bounding-box', 'globe-central-south-asia', 'chat-left-dots-fill', 'pencil-square'], 
                           menu_icon="cast", default_index=0, 
                           styles={
                               "icon": {"font-size": "24px"}, 
                               "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#48A6EE", "margin-top": "10px"},
                               "nav-link-selected": {"background-color": "#48A6EE", "font-weight": "100"}
                           })

if selected == 'DashBoard':
    st.markdown("<h1>Dashboard content goes here.</h1>", unsafe_allow_html=True)

elif selected == 'Forecast':
    st.title('Crime Forecast')
    embed_iframe("https://forecast-ksp.streamlit.app/?embed=true")

elif selected == 'Patrolling':
    st.title('Map View')
    iframe_src = "http://ksp-data.s3-website-us-east-1.amazonaws.com/"
    embed_iframe(iframe_src)

elif selected == 'Video Analysis':
    st.title("Video Analysis")
    embed_iframe("https://video-crime.streamlit.app/?embed=true")

elif selected == 'Victim Analysis':
    st.title('Victim Analysis')
    embed_iframe("https://victim-ksp.streamlit.app/?embed=true")

elif selected == 'Chatbot':
    st.title('Crime Chatbot')
    embed_iframe("https://chatbot-ksp.streamlit.app/?embed=true")

elif selected == 'Map Analysis':
    st.title('Map Analysis')
    embed_iframe("https://map-ksp.streamlit.app/?embed=true")

elif selected == 'Feedback':
    feedback_main()
