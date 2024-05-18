import streamlit as st
from streamlit_option_menu import option_menu
from feedback import feedback_main
from PIL import Image

st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
image = Image.open("1.jpg")
image = image.resize((1200, 200))  # Set custom width and height

with st.sidebar:
    selected = option_menu("Main Menu", ['DashBoard', 'Forecast', 'Patrolling', 'Video Analysis', 'Victim Analysis', 'Map Analysis', 'Chatbot', 'Feedback'],
                           icons=['bar-chart', 'graph-up-arrow', 'radar', 'camera-reels', 'person-bounding-box', 'globe-central-south-asia', 'chat-left-dots-fill', 'pencil-square'], 
                           menu_icon="cast", default_index=0, 
                           styles={
                               "icon": {"font-size": "24px"}, 
                               "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px",  "--hover-color": "#48A6EE", "margin-top": "10px"},
                               "nav-link-selected": {"background-color": "#48A6EE", "font-weight": "100"}
                           })

if selected == 'DashBoard':
    st.image(image, use_column_width=True)
    st.components.v1.iframe("https://frontpage-ksp.streamlit.app/?embed=true", height=800, scrolling=True)

elif selected == 'Patrolling':
    st.title('Map View')
    html_code = """
        <iframe src="http://ksp-data.s3-website-us-east-1.amazonaws.com/" style="width:100%; height:800px; border:none;"></iframe>
    """
    st.markdown(html_code, unsafe_allow_html=True)

elif selected == 'Video Analysis':
    st.title("Video Analysis")
    st.components.v1.iframe("https://video-crime.streamlit.app/?embed=true", height=800, scrolling=True)

elif selected == 'Forecast':
    st.title('Crime Forecast')
    st.components.v1.iframe("https://forecast-ksp.streamlit.app/?embed=true", height=800, scrolling=True)

elif selected == 'Victim Analysis':
    st.title('Victim Analysis')
    st.components.v1.iframe("https://victim-ksp.streamlit.app/?embed=true", height=800, scrolling=True)

elif selected == 'Chatbot':
    st.title('Crime Chatbot')
    st.components.v1.iframe("https://chatbot-ksp.streamlit.app/?embed=true", height=800, scrolling=True)

elif selected == 'Map Analysis':
    st.title('Map Analysis')
    st.components.v1.iframe("https://map-ksp.streamlit.app/?embed=true", height=800, scrolling=True)

elif selected == 'Feedback':
    feedback_main()
