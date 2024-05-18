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

# Add banner image with custom dimensions
st.image(image)

with st.sidebar:
    selected = option_menu("Main Menu", ['DashBoard', 'MapView', 'Video Analysis', 'Forecast', 'Victim Analysis', 'Chatbot', 'Feedback'],
                           icons=['bar-chart', 'radar', 'camera-reels', 'graph-up-arrow', 'person-bounding-box', 'chat-left-dots-fill', 'pencil-square'], 
                           menu_icon="cast", default_index=0, 
                           styles={
                               "icon": {"font-size": "24px"}, 
                               "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px",  "--hover-color": "#48A6EE", "margin-top": "10px"},
                               "nav-link-selected": {"background-color": "#48A6EE", "font-weight": "100"}
                           })

if selected == 'DashBoard':
    st.title("DashBoard")
    st.markdown("""
        <style>
        .embed-container { 
            position: relative; 
            padding-bottom: 56.25%; 
            height: 0; 
            overflow: hidden; 
            max-width: 100%; 
        } 
        .embed-container iframe, 
        .embed-container object, 
        .embed-container embed { 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
        }
        </style>
        <div class='embed-container'>
            <iframe src="https://frontpage-ksp.streamlit.app/?embed=true" frameborder="0" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)
    
# MapView Section
elif selected == 'MapView':
    st.title('Map View')
    iframe_src = "http://ksp-data.s3-website-us-east-1.amazonaws.com"
    embed_iframe(iframe_src, height=800, width=1200)

# Video Analysis Section
elif selected == 'Video Analysis':
    st.title("Video Analysis")
    st.markdown("""
        <style>
        .embed-container { 
            position: relative; 
            padding-bottom: 56.25%; 
            height: 0; 
            overflow: hidden; 
            max-width: 100%; 
        } 
        .embed-container iframe, 
        .embed-container object, 
        .embed-container embed { 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
        }
        </style>
        <div class='embed-container'>
            <iframe src="https://video-crime.streamlit.app/?embed=true" frameborder="0" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

# Forecast Section
elif selected == 'Forecast':
    st.title('Crime Forecast')
    st.write("Forecasting content goes here.")
    
    # Embed external content using iframe
    st.markdown("""
        <style>
        .embed-container { 
            position: relative; 
            padding-bottom: 56.25%; 
            height: 0; 
            overflow: hidden; 
            max-width: 100%; 
        } 
        .embed-container iframe, 
        .embed-container object, 
        .embed-container embed { 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
        }
        </style>
        <div class='embed-container'>
            <iframe src="https://forecast-ksp.streamlit.app/?embed=true" frameborder="0" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

# Victim Analysis Section
elif selected == 'Victim Analysis':
    st.title('Victim Analysis')
    st.write("Victim Analysis content goes here.")
    
    # Embed external content using iframe
    st.markdown("""
        <style>
        .embed-container { 
            position: relative; 
            padding-bottom: 56.25%; 
            height: 0; 
            overflow: hidden; 
            max-width: 100%; 
        } 
        .embed-container iframe, 
        .embed-container object, 
        .embed-container embed { 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
        }
        </style>
        <div class='embed-container'>
            <iframe src="https://victim-ksp.streamlit.app/?embed=true" frameborder="0" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

# Chatbot Section
elif selected == 'Chatbot':
    st.title('Crime Chatbot')
    st.write("Chatbot content goes here.")
    
    # Embed external content using iframe
    st.markdown("""
        <style>
        .embed-container { 
            position: relative; 
            padding-bottom: 56.25%; 
            height: 0; 
            overflow: hidden; 
            max-width: 100%; 
        } 
        .embed-container iframe, 
        .embed-container object, 
        .embed-container embed { 
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
        }
        </style>
        <div class='embed-container'>
            <iframe src="https://chatbot-ksp.streamlit.app/?embed=true" frameborder="0" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

# Feedback Section
elif selected == 'Feedback':
    feedback_main()
