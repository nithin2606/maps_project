import json
import folium
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from streamlit_folium import st_folium
from destinations import extract_places
from collections import Counter


st.set_page_config(layout = "wide")

@st.cache_data
def load_places():
    return extract_places("Timeline_15_03_26.json")

places, dup_places, places_id, dup_places_id = load_places()


with st.sidebar:
    st.title("Timeline Viewer")
    st.markdown("""
    This map visualises all the unique places extracted from my Google Maps Timeline data collected since 2016.
    
    Each dot represents a location I visited.
    """)
    st.divider()
    st.markdown("**Data Source**")
    st.caption("Google Maps Timeline exported from timeline")

    st.markdown("**Total destinations Extracted:**")
    st.caption(f"{len(places)} unique places")

    all_years = sorted(set(p["year"] for p in places if p["year"]))
    year_range = st.select_slider("Filter by Year", options = all_years, value = (all_years[0], all_years[-1]))

    st.divider()
    st.markdown("**Note**")
    st.caption("The extract seems to have some missing data in 2016 and 2017, needs further investigation")


filtered_places = [p for p in places if year_range[0] <= p["year"] <= year_range[1]]


m = folium.Map()

if filtered_places:
    lats = [p["lat"] for p in filtered_places]
    lngs = [p["lng"] for p in filtered_places]
    m.fit_bounds([[min(lats), min(lngs)], [max(lats), max(lngs)]])

# freq = Counter((p["lat"], p["lng"]) for p in dup_places)
# max_freq = max(freq.values())

# print(max_freq)

# def freq_to_size(count, max_count, min_size=1, max_size=15):
#     return min_size + (max_size - min_size) * (count / max_count)


for p in filtered_places:

    # count = freq.get((p["lat"], p["lng"]), 1)
    # size = freq_to_size(count, max_freq)

    folium.CircleMarker(
        location=[p["lat"], p["lng"]],
        radius=2,
        color="#3388ff",
        fill=True,
        fill_opacity=0.3,
    ).add_to(m)

col_map, col_chart = st.columns([2, 1])

with col_map:
    st.markdown(
    f"<p style='text-align:center; color:gray; font-size:20px'>"
    f"<b style='color:#3388ff; font-size:24px'>{len(filtered_places)}</b>"
    f" places visited from "
    f"<b>{year_range[0]}</b> to <b>{year_range[1]}</b>"
    f"</p>",
    unsafe_allow_html=True
    )

    st_folium(m, use_container_width=True, height=750)

with col_chart:

    df_dup_places_id = pd.DataFrame(places_id)

    df_yearly = (
        df_dup_places_id
        .groupby("year")["place_id"]
        .nunique()
        .reset_index(name="visits")
        .sort_values("year")
        .set_index("year")
    )

    values = df_yearly["visits"].values
    norm = mcolors.Normalize(vmin=values.min(), vmax=values.max())
    colors = [cm.rainbow_r(norm(value)) for value in values]


    fig, ax = plt.subplots(figsize=(4, 6))
    ax.bar(df_yearly.index, df_yearly["visits"], color=colors)
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Visits")
    ax.set_title("Places Visited Per Year")
    ax.tick_params(axis='x', rotation=90)

    fig.tight_layout()

    st.pyplot(fig, width='stretch')