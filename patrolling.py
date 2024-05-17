import pandas as pd
from sklearn.cluster import KMeans
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
import os
from dotenv import load_dotenv
from s3 import read_files_from_s3

# Load environment variables
load_dotenv()
access_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_id = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

# Function to apply KMeans clustering
def apply_kmeans(df, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    df['cluster'] = kmeans.fit_predict(df[['Latitude', 'Longitude']])
    return df, kmeans.cluster_centers_

# Function to visualize clusters on a Folium map
def visualize_clusters(df, centers):
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    map = folium.Map(location=map_center, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(map)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            icon=folium.Icon(icon='record', color='red'),
        ).add_to(marker_cluster)

    for center in centers:
        folium.Marker(
            location=center,
            icon=folium.Icon(icon='star', color='blue'),
            popup='Patrol Center'
        ).add_to(map)

    return map

# Main function to display the patrolling map
def patrolling_main():
    data_frames = load_data()
    data = data_frames['FIR_Details_Data.csv']
    st.title('Patrolling Map')
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    df = data.drop_duplicates(subset=['Latitude', 'Longitude', 'CrimeHead_Name'])
    clusters = st.slider('Select number of clusters', min_value=3, max_value=20, value=10, step=1)
    df, centers = apply_kmeans(df, clusters)
    crime_map = visualize_clusters(df, centers)
    folium_static(crime_map)


    
@st.cache_data
def load_data():
    bucket_name = 'new-trail01'
    file_keys = 'FIR_Details_Data.csv'
    return read_files_from_s3(bucket_name, file_keys)
    

    
