import json
import folium
import streamlit as st
from streamlit_folium import st_folium
from destinations import extract_places
from collections import Counter

st.set_page_config(layout = "wide", page_title="Google Timeline Destinations")

@st.cache_data
def load_places():
    return extract_places("Timeline_15_03_26.json")

places, dup_places, places_id, dup_places_id = load_places()

with st.sidebar:
    st.title("Timeline Viewer")
    st.markdown("""
    This map visualises all the unique places extracted from your Google Maps Timeline.
    
    Each dot represents a location I visited.
    """)
    st.divider()
    st.markdown("**Data Source**")
    st.caption("Google Maps Timeline exported from timeline")

    st.markdown("**Total destinations Extracted:**")
    st.caption(f"{len(places)} unique places")



m = folium.Map()

if places:
    lats = [p["lat"] for p in places]
    lngs = [p["lng"] for p in places]
    m.fit_bounds([[min(lats), min(lngs)], [max(lats), max(lngs)]])

freq = Counter((p["lat"], p["lng"]) for p in dup_places)
max_freq = max(freq.values())

# print(max_freq)

def freq_to_bar(lat, lng, count, max_count, max_height=100):
    height = max(3, int(max_height * (count / max_count)))
    bar_html = f"""
        <div style="
            width: 4px;
            height: {height}px;
            background: #3388ff;
            opacity: 0.7;
            border-radius: 2px 2px 0 0;
        "></div>
    """
    return folium.Marker(
        location=[lat, lng],
        icon=folium.DivIcon(
            html=bar_html,
            icon_size=(4, height),
            icon_anchor=(2, height),
        )
    )

for p in places:
    count = freq.get((p["lat"], p["lng"]), 1)
    freq_to_bar(p["lat"], p["lng"], count, max_freq).add_to(m)

st_folium(m, use_container_width=True, height=750)