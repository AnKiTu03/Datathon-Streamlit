import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from feedback import feedback_main
from PIL import Image

# Function to embed iframes
def embed_iframe(url):
    components.iframe(url, height=st.session_state['iframe_height'], width=st.session_state['iframe_width'], scrolling=True)

# Set the page configuration
st.set_page_config(
    page_title="Crime Analysis Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Set default iframe dimensions in session state
if 'iframe_height' not in st.session_state:
    st.session_state['iframe_height'] = st.get_option('browser.gpu-height') - 200  # Leave some space for the header
if 'iframe_width' not in st.session_state:
    st.session_state['iframe_width'] = st.get_option('browser.gpu-width')

# Load and display the banner image
image = Image.open("1.jpg")
st.image(image, use_column_width=True)

# Sidebar with navigation menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ['DashBoard', 'Forecast', 'Patrolling', 'Video Analysis', 'Victim Analysis', 'Map Analysis', 'Chatbot', 'Feedback'],
        icons=['bar-chart', 'graph-up-arrow', 'radar', 'camera-reels', 'person-bounding-box', 'globe-central-south-asia', 'chat-left-dots-fill', 'pencil-square'],
        menu_icon="cast",
        default_index=0,
        styles={
            "icon": {"font-size": "24px"},
            "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#48A6EE", "margin-top": "10px"},
            "nav-link-selected": {"background-color": "#48A6EE", "font-weight": "bold"}
        }
    )

# Display respective content based on the selected tab
if selected == 'DashBoard':
    st.title('Dashboard')
    embed_iframe("https://frontpage-ksp.streamlit.app/?embed=true")

elif selected == 'Forecast':
    st.title('Crime Forecast')
    embed_iframe("https://forecast-ksp.streamlit.app/?embed=true")

elif selected == 'Patrolling':
    st.title('Map View')
    st.write("Attempting to load the map view iframe...")
    embed_iframe("https://ksp-data.s3.amazonaws.com/index.html")
    st.write("If the map does not load, please check the URL and ensure it is correct and accessible.")

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
