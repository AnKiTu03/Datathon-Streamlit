import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from feedback import feedback_main
from PIL import Image

st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Load and display banner image
image = Image.open("1.jpg")


def embed_iframe(url):
    iframe_code = f'''
    <style>
    .embed-container {{
        position: absolute;
        top: 200px;  /* Adjust this value based on the height of your image */
        left: 0;
        right: 0;
        bottom: 0;
        width: 100%;
        height: calc(100% - 200px);  /* Adjust this value based on the height of your image */
        border: none;
    }}
    .embed-container iframe {{
        width: 100%;
        height: 100%;
        border: none;
    }}
    </style>
    <div class="embed-container">
        <iframe src="{url}" allowfullscreen></iframe>
    </div>
    '''
    st.markdown(iframe_code, unsafe_allow_html=True)

# Sidebar with navigation menu
with st.sidebar:
    selected = option_menu("Main Menu", 
                           ['DashBoard', 'Forecast', 'Patrolling', 'Video Analysis', 'Victim Analysis','Chatbot', 'Feedback'],
                           icons=['bar-chart', 'graph-up-arrow', 'radar', 'camera-reels', 'person-bounding-box', 'chat-left-dots-fill', 'pencil-square'], 
                           menu_icon="cast", default_index=0, 
                           styles={
                               "icon": {"font-size": "24px"}, 
                               "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#48A6EE", "margin-top": "10px"},
                               "nav-link-selected": {"background-color": "#48A6EE", "font-weight": "100"}
                           })

# Embed respective content based on the selected tab
if selected == 'DashBoard':
    st.image(image.resize((1200, 200)), use_column_width=True)
    components.iframe("https://frontpage-ksp.streamlit.app/?embed=true", height=900, scrolling=True)

elif selected == 'Forecast':
    components.iframe("https://forecast-ksp.streamlit.app/?embed=true", height=900, scrolling=True)

elif selected == 'Patrolling':
    st.title('Patrolling Map')
    st.markdown("""
        <div style="background-color: #48A6EE; padding: 10px; border-radius: 5px; color: black; font-weight: bold;">
            This map shows red points as patrol centers and clusters of crime incidents. Zoom in and out to see the clusters change in size and number.
        </div>
    """, unsafe_allow_html=True)
    st.write(" ")
    st.warning('Please wait till the map is loading ...', icon="⚠️")
    iframe_src = "https://ksp-data.s3.amazonaws.com/index.html"
    components.iframe(iframe_src, height=800, scrolling=True)


elif selected == 'Video Analysis':
    components.iframe("https://video-crime.streamlit.app/?embed=true", height=900, scrolling=True)

elif selected == 'Victim Analysis':
    components.iframe("https://victim-ksp.streamlit.app/?embed=true", height=900, scrolling=True)

elif selected == 'Chatbot':
    components.iframe("https://chatbot-ksp.streamlit.app/?embed=true", height=900, scrolling=True)

elif selected == 'Feedback':
    feedback_main()
