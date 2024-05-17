import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from sklearn.cluster import KMeans
import joblib
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from s3 import read_files_from_s3
import google.generativeai as genai
from pandasai import SmartDatalake
import requests
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
from video import video_main
from feedback import feedback_main

# Load environment variables
load_dotenv()
bucket_name = 'new-trail01'
file_keys = ['Accused_Data.csv', 'FIR_Details_Data.csv']
os.environ["GOOGLE_API_KEY"] = os.getenv('GEN_AI')
gen_api = os.getenv('GEN_AI')
pandasai_api_key = os.getenv('PANDASAI_API_KEY')
os.environ['PANDASAI_API_KEY'] = pandasai_api_key
rapidapi_key = os.getenv('RAPIDAPI_KEY')

# Configure Google Generative AI
genai.configure(api_key=gen_api)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

@st.cache_data()
def load_data():
    return read_files_from_s3(bucket_name, file_keys)

data_frames = load_data()
accused_data = data_frames['Accused_Data.csv']
fir_data = data_frames['FIR_Details_Data.csv']

with st.sidebar:
    selected = option_menu("Main Menu", ['DashBoard', 'MapView', 'Video Analysis', 'Forecast', 'chatbot', 'Feedback'],
                           icons=['bar-chart', 'radar', 'camera-reels', 'graph-up-arrow', 'chat-left-dots-fill'], 
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

# MapView Section
elif selected == 'MapView':
    def apply_kmeans(df, n_clusters=10):
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        df['cluster'] = kmeans.fit_predict(df[['Latitude', 'Longitude']])
        return df, kmeans.cluster_centers_

    def visualize_clusters(df, centers):
        map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
        map = folium.Map(location=map_center, zoom_start=12)
        marker_cluster = MarkerCluster().add_to(map)

        for _, row in df.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],  # Fixed here: Access columns separately
                icon=folium.Icon(icon='record', color='red'),
            ).add_to(marker_cluster)

        for center in centers:
            folium.Marker(
                location=center,
                icon=folium.Icon(icon='star', color='blue'),
                popup='Patrol Center'
            ).add_to(map)

        return map

    st.title('Patrolling Map')
    fir_data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    df = fir_data.drop_duplicates(subset=['Latitude', 'Longitude', 'CrimeHead_Name'])
    clusters = st.slider('Select number of clusters', min_value=3, max_value=20, value=10, step=1)
    df, centers = apply_kmeans(df, clusters)
    crime_map = visualize_clusters(df, centers)
    folium_static(crime_map)

# Forecast Section
elif selected == 'Forecast':
    @st.cache_resource
    def load_model(district):
        model_path = f'models/{district}_model.pkl'
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            st.error(f"No pre-trained model found for {district}.")
            return None

    def prepare_data(data, district_name):
        district_data = data[data['UnitName'] == district_name]
        district_data['Offence_From_Date'] = pd.to_datetime(district_data['Offence_From_Date'])
        district_data = district_data.set_index('Offence_From_Date')
        return district_data.resample('M').size()

    def plot_forecast(forecast, title):
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(forecast['ds'], forecast['yhat'], label='Forecast (yhat)', color='red', marker='o')
        ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2, label='Forecast Confidence Interval')
        ax.plot(forecast['ds'], forecast['trend'], label='Trend', color='blue', linestyle='--')
        ax.set_title(title)
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Crimes')
        ax.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(fig)

    st.title('District-Wise Crime Rate Prediction using Facebook Prophet')

    if 'UnitName' not in fir_data.columns:
        st.error("The dataset does not contain 'UnitName'. Please upload a dataset with location data.")
    else:
        fir_data = fir_data[fir_data['Offence_From_Date'] >= '2019-01-01']
        fir_data.dropna(subset=['Offence_From_Date', 'UnitName'], inplace=True)

        if fir_data.empty:
            st.error("No data available from 2019 onwards. Please check your dataset.")
        else:
            district_list = fir_data['UnitName'].unique()
            selected_district = st.selectbox('Select a District for Analysis', district_list)
            forecast_periods = st.slider('Select number of months to forecast', min_value=12, max_value=48, value=12, step=12)

            with st.spinner(f'Loading model for {selected_district}...'):
                model = load_model(selected_district)

            if model:
                district_resampled = prepare_data(fir_data, selected_district)
                df_prophet = pd.DataFrame(district_resampled.reset_index())
                df_prophet.columns = ['ds', 'y']

                with st.spinner('Generating forecast...'):
                    future = model.make_future_dataframe(periods=forecast_periods, freq='M')
                    forecast = model.predict(future)

                plot_forecast(forecast, f'Forecast Visualization for {selected_district}')
            else:
                st.error("Model loading failed.")

# Video Analysis Section
elif selected == 'Video Analysis':
    video_main()

# Feedback Section
elif selected == 'Feedback':
    feedback_main()

# Chatbot Section
elif selected == 'chatbot':
    def trans(txt):
        url = "https://microsoft-translator-text.p.rapidapi.com/translate"
        querystring = {"to[0]":"kn","api-version":"3.0","profanityAction":"NoAction","textType":"plain"}
        payload = [{ "Text": txt }]
        headers = {
	   "content-type": "application/json",
	   "X-RapidAPI-Key": "c9cf11c221msh7ba92db113f7b27p125495jsnd35a5d990324",
	   "X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
   }

        response = requests.post(url, json=payload, headers=headers, params=querystring)

        if response.status_code == 200:
            parsed_data = response.json()
            translated_text = parsed_data[0]['translations'][0]['text']
            return translated_text
        else:
            return "Server Limit Exceeded"


    data = fir_data
    lake = SmartDatalake([data])

    llm = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    st.title("Data Chat Bot Interface")
    st.header("Chat with Data")
    bu = st.checkbox("Kannada")

    user_input = st.text_input("Ask a question about the data:")

    if user_input:
        try:
            with st.spinner("Processing your question..."):
                r = lake.chat(user_input)
                Human_prompt = f"Given the question {user_input}, you will receive an answer {r} from the Database. Frame a user-friendly response using this."

                response = llm.generate_content(Human_prompt)
                response = response.text
                if bu:
                    response = trans(response)

            st.text_area("Bot Response:", value=response, height=300)
        except Exception as e:
            st.error(f"Error processing your question: {e}")
    else:
        st.write("Please enter a question to start chatting.")
