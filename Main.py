import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Load and display banner image
image = Image.open("1.jpg")
st.image(image.resize((1200, 200)), use_column_width=True)

# Define function to embed iframes
def embed_iframe(url, height=800):
    st.components.v1.iframe(url, height=height, width=1200, scrolling=True)

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

# Embed respective content based on the selected tab
if selected == 'DashBoard':
    embed_iframe("https://frontpage-ksp.streamlit.app/?embed=true")

elif selected == 'Forecast':
    st.title('Crime Forecast')
    embed_iframe("https://forecast-ksp.streamlit.app/?embed=true")

elif selected == 'Patrolling':
    st.title('Map View')
    embed_iframe("http://ksp-data.s3-website-us-east-1.amazonaws.com/")

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
    st.title('Feedback')
    st.write("Feedback section content goes here.")
