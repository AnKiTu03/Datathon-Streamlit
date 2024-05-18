import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from PIL import Image

def embed_iframe(url, height=800, width=1200):
    components.iframe(url, height=height, width=width, scrolling=True)

st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Load and display banner image
image = Image.open("1.jpg")
st.image(image.resize((1200, 200)), use_column_width=True)

# Sidebar with navigation menu
with st.sidebar:
    selected = option_menu("Main Menu", 
                           ['Patrolling'],
                           icons=['radar'], 
                           menu_icon="cast", default_index=0, 
                           styles={
                               "icon": {"font-size": "24px"}, 
                               "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#48A6EE", "margin-top": "10px"},
                               "nav-link-selected": {"background-color": "#48A6EE", "font-weight": "100"}
                           })

if selected == 'Patrolling':
    st.title('Map View')
    st.write("Attempting to load the map view iframe...")
    iframe_src = "http://ksp-data.s3-website-us-east-1.amazonaws.com"
    embed_iframe(iframe_src)
    st.write("If the map does not load, please check the URL and ensure it is correct and accessible.")
