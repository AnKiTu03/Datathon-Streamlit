import streamlit as st
import streamlit.components.v1 as components

def embed_iframe(url, height=800, width=1200):
    components.iframe(url, height=height, width=width, scrolling=True)

st.set_page_config(page_title="Basic Iframe Test", page_icon=":chart_with_upwards_trend:", layout="wide")

# Embed a well-known URL to test iframe functionality
embed_iframe("https://www.example.com", height=800, width=1200)
