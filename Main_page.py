from streamlit_option_menu import option_menu
import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import plotly.express as px
from patrolling import patrolling_main
from forecast import forecast_main
from video import video_main
from feedback import feedback_main
from chatbot import chat_with_data
from s3 import read_files_from_s3
from dotenv import load_dotenv

st.set_page_config(page_title="Crime Analysis Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
# Load environment variables
load_dotenv()
bucket_name = 'new-trail01'
file_keys = ['Accused_Data.csv']

@st.cache_data()
def load_data():
    return read_files_from_s3(bucket_name, file_keys)

data_frames = load_data()
data = data_frames['Accused_Data.csv']

with st.sidebar:
    selected = option_menu("Main Menu", ['DashBoard', 'MapView', 'Video Analysis', 'Forecast', 'chatbot', 'Feedback'],
        icons=['bar-chart', 'radar', 'camera-reels', 'graph-up-arrow', 'chat-left-dots-fill'], menu_icon="cast", default_index=0, styles={
            "icon": {"font-size": "24px"}, 
            "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px",  "--hover-color": "#48A6EE" , "margin-top" : "10px"},
            "nav-link-selected": {"background-color": "#48A6EE" , "font-weight" : "100"}
        })

def Dashboard():
    df = data

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
                                 height=500, width=500)
    fig_city_profession.update_layout(showlegend=True)

    city_caste_counts = df.groupby(['District_Name', 'Caste']).size().reset_index(name='Count')
    fig_city_caste = px.bar(city_caste_counts, x='District_Name', y='Count', color='Caste',
                            title='City wise Caste Distribution',
                            labels={'District_Name': 'City', 'Count': 'Occurrences', 'Caste': 'Caste'},
                            height=500, width=500)
    fig_city_caste.update_layout(showlegend=True)

    st.plotly_chart(fig_heatmap)
    st.plotly_chart(fig_city_profession)
    st.plotly_chart(fig_city_caste)

if selected == 'DashBoard':
    st.write(":house: / DashBoard")
    cols = st.columns([0.7, 0.3])
    with cols[0]:
        st.write("**Dashboard**")
    with cols[1]:
        cols = st.columns(2)
        with cols[0]:
            st.markdown('<input style="width: 150px; height: 25px; outline: none; padding: 5px; border: 1px solid white ; border-radius: 5px; background-color: black;" type="text" placeholder="Search here">', unsafe_allow_html=True)

    cols = st.columns(4)
    with cols[0]:
        ui.card(title="Crime Report", content="45,231", description="+20.1% from last month", key="card1").render()
    with cols[1]:
        ui.card(title="Crime Solved", content="+2350", description="+18.1% from last month", key="card2").render()
    with cols[2]:
        ui.card(title="Cases Pending", content="+3,234", description="+19% from last month", key="card3").render()
    with cols[3]:
        ui.card(title="Active Cases", content="+2350", description="+18.1% from last month", key="card4").render()

    Dashboard()

elif selected == 'MapView':
    patrolling_main()

elif selected == 'Forecast':
    forecast_main()

elif selected == 'Video Analysis':
    video_main()

elif selected == 'Feedback':
    feedback_main()

elif selected == 'chatbot':
    chat_with_data()