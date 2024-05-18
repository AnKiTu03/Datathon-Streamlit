import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from s3 import read_files_from_s3
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
import streamlit.components.v1 as components
from feedback import feedback_main

def embed_iframe(url, height=800, width=1200):
    components.iframe(url, height=height, width=width, scrolling=False)

st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Load environment variables
load_dotenv()
bucket_name = 'new-trail01'
file_keys = ['Accused_Data.csv', 'FIR_Details_Data.csv']
os.environ["GOOGLE_API_KEY"] = os.getenv('GEN_AI')
gen_api = os.getenv('GEN_AI')
pandasai_api_key = os.getenv('PANDASAI_API_KEY')
os.environ['PANDASAI_API_KEY'] = pandasai_api_key
rapidapi_key = os.getenv('RAPIDAPI_KEY')



@st.cache_data()
def load_data():
    with st.spinner("Loading data..."):
        return read_files_from_s3(bucket_name, file_keys)

data_frames = load_data()
accused_data = data_frames['Accused_Data.csv']

with st.sidebar:
    selected = option_menu("Main Menu", ['DashBoard', 'MapView', 'Video Analysis', 'Forecast', 'Victim Analysis', 'Chatbot', 'Feedback'],
                           icons=['bar-chart', 'radar', 'camera-reels', 'graph-up-arrow', 'person-bounding-box', 'chat-left-dots-fill', 'pencil-square'], 
                           menu_icon="cast", default_index=0, 
                           styles={
                               "icon": {"font-size": "24px"}, 
                               "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px",  "--hover-color": "#48A6EE", "margin-top": "10px"},
                               "nav-link-selected": {"background-color": "#48A6EE", "font-weight": "100"}
                           })

# Dashboard Section
if selected == 'DashBoard':
    st.write(":house: / DashBoard")
    cols = st.columns([0.7, 0.3])
    with cols[0]:
        st.write("**Dashboard**")
    with cols[1]:
        cols = st.columns(2)
        with cols[0]:
            st.markdown('<input style="width: 150px; height: 25px; outline: none; padding: 5px; border: 1px solid white; border-radius: 5px; background-color: black;" type="text" placeholder="Search here">', unsafe_allow_html=True)

    cols = st.columns(4)
    with cols[0]:
        ui.card(title="Crime Report", content="45,231", description="+20.1% from last month", key="card1").render()
    with cols[1]:
        ui.card(title="Crime Solved", content="+2350", description="+18.1% from last month", key="card2").render()
    with cols[2]:
        ui.card(title="Cases Pending", content="+3,234", description="+19% from last month", key="card3").render()
    with cols[3]:
        ui.card(title="Active Cases", content="+2350", description="+18.1% from last month", key="card4").render()

    df = accused_data

    df_filtered_age = df[(df['age'] > 16) & (df['age'] < 60)]
    crime_pivot = pd.pivot_table(df_filtered_age, values='Year', index='District_Name', columns='age', aggfunc='count', fill_value=0)
    fig_heatmap = px.imshow(crime_pivot,
                            labels=dict(x="Age", y="District", color="Crime Count"),
                            x=crime_pivot.columns,
                            y=crime_pivot.index,
                            title='Crime Incidents by District and Age',
                            color_continuous_scale='viridis')
    fig_heatmap.update_layout(height=600, width=900)

    city_profession_counts = df.groupby(['District_Name', 'Profession']).size().reset_index(name='Count')
    fig_city_profession = px.bar(city_profession_counts, x='District_Name', y='Count', color='Profession',
                                 title='City wise Profession Distribution',
                                 labels={'District_Name': 'City', 'Count': 'Occurrences', 'Profession': 'Profession'},
                                 height=500, width=600)
    fig_city_profession.update_layout(showlegend=True)

    city_caste_counts = df.groupby(['District_Name', 'Caste']).size().reset_index(name='Count')
    fig_city_caste = px.bar(city_caste_counts, x='District_Name', y='Count', color='Caste',
                            title='City wise Caste Distribution',
                            labels={'District_Name': 'City', 'Count': 'Occurrences', 'Caste': 'Caste'},
                            height=500, width=600)
    fig_city_caste.update_layout(showlegend=True)

    with st.spinner("Generating heatmap..."):
        st.plotly_chart(fig_heatmap)

    with st.spinner("Generating city profession distribution chart..."):
        st.plotly_chart(fig_city_profession)

    with st.spinner("Generating city caste distribution chart..."):
        st.plotly_chart(fig_city_caste)

# MapView Section
elif selected == 'MapView':
    st.title('Map View')
    iframe_src = "http://ksp-data.s3-website-us-east-1.amazonaws.com"
    embed_iframe(iframe_src, height=800, width=1200)

# Video Analysis Section
elif selected == 'Video Analysis':
    st.title("Video Analysis")
    st.components.v1.iframe("https://video-crime.streamlit.app/?embed=true&embed_options=disable_scrolling", height=800, width=1200)

# Forecast Section
elif selected == 'Forecast':
    st.title('Crime Forecast')
    st.write("Forecasting content goes here.")
    
    # Embed external content using iframe
    st.components.v1.iframe("https://forecast-ksp.streamlit.app/?embed=true&embed_options=disable_scrolling", height=800, width=1200)

# Victim Analysis Section
elif selected == 'Victim Analysis':
    st.title('Victim Analysis')
    st.write("Victim Analysis content goes here.")
    
    # Embed external content using iframe
    st.components.v1.iframe("https://victim-ksp.streamlit.app/?embed=true&embed_options=disable_scrolling", height=800, width=1200)

# Chatbot Section
elif selected == 'Chatbot':
    st.title('Crime Chatbot')
    st.write("Chatbot content goes here.")
    
    # Embed external content using iframe
    st.components.v1.iframe("https://chatbot-ksp.streamlit.app/?embed=true&embed_options=disable_scrolling", height=800, width=1200)

# Feedback Section
elif selected == 'Feedback':
    feedback_main()
