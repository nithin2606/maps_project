import json
import folium
import streamlit as st
from streamlit_folium import st_folium
from destinations import extract_places

st.title("Google Timeline Destinations Map")


@st.cache_data
def load_places():
    return extract_places("Timeline_15_03_26.json", output_file_path="points_output.json")

places = load_places()

st.write(f"Total destinations extracted: {len(places)}")

m = folium.Map()

for p in places:
    folium.CircleMarker(
        location=[p["lat"], p["lng"]],
        radius=3,
        color="#0a29f3",
        fill=True,
        fill_opacity=1,
    ).add_to(m)

st_folium(m, width=700, height=500)