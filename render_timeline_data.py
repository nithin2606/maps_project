import json
import re
import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(page_title="Google Timeline Viewer", layout="wide")
st.title("🗺️ Google Maps Timeline Viewer")

# ── Helpers ──────────────────────────────────────────────────────────────────

def parse_point(point_str: str):
    """Parse '10.2432693°, 76.3727963°' → (lat, lng) floats."""
    nums = re.findall(r"[-\d.]+", point_str)
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    return None, None


def load_points(data) -> pd.DataFrame:
    """Extract all points from the timeline JSON (list or dict wrapper)."""
    entries = (
        data
        if isinstance(data, list)
        else data.get("semanticSegments", data.get("timelineObjects", []))
    )
    rows = []
    for entry in entries:
        for p in entry.get("timelinePath", []):
            point_str = p.get("point", "")
            time_str  = p.get("time", "")
            lat, lng  = parse_point(point_str)
            if lat is not None:
                rows.append({"lat": lat, "lng": lng, "time": time_str, "point": point_str})
    return pd.DataFrame(rows)


# ── Sidebar / Upload ──────────────────────────────────────────────────────────

with st.sidebar:
    st.header("📂 Upload Timeline")
    uploaded = st.file_uploader("Select your timeline.json", type="json")

    st.markdown("---")
    st.header("⚙️ Map Options")
    map_type = st.radio(
        "View",
        ["Dots (Markers)", "Connected Path", "Heatmap", "Clustered Markers"],
    )
    tile = st.selectbox(
        "Basemap",
        ["OpenStreetMap", "CartoDB positron", "CartoDB dark_matter", "Stamen Terrain"],
    )


# ── Load Data ─────────────────────────────────────────────────────────────────

if uploaded:
    raw = json.load(uploaded)
    df  = load_points(raw)

    if df.empty:
        st.error("No `timelinePath` points found in this file.")
        st.stop()

    st.sidebar.success(f"✅ {len(df):,} points loaded")

    # Optional time filter
    if "time" in df.columns and df["time"].notna().any():
        st.sidebar.markdown("---")
        st.sidebar.header("🗓️ Filter by Date")
        df["date"] = pd.to_datetime(df["time"], errors="coerce").dt.date
        dates = sorted(df["date"].dropna().unique())
        if len(dates) > 1:
            sel = st.sidebar.select_slider(
                "Date range",
                options=dates,
                value=(dates[0], dates[-1]),
            )
            df = df[(df["date"] >= sel[0]) & (df["date"] <= sel[1])]

    # ── Build Map ─────────────────────────────────────────────────────────────

    center = [df["lat"].mean(), df["lng"].mean()]
    m = folium.Map(location=center, zoom_start=10, tiles=tile)

    if map_type == "Dots (Markers)":
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["lng"]],
                radius=4,
                color="#3388ff",
                fill=True,
                fill_color="#3388ff",
                fill_opacity=0.7,
                tooltip=row.get("time", ""),
            ).add_to(m)

    elif map_type == "Connected Path":
        coords = df[["lat", "lng"]].values.tolist()
        folium.PolyLine(coords, color="#e74c3c", weight=2.5, opacity=0.8).add_to(m)
        # Start / end markers
        folium.Marker(coords[0],  icon=folium.Icon(color="green", icon="play"),  tooltip="Start").add_to(m)
        folium.Marker(coords[-1], icon=folium.Icon(color="red",   icon="stop"),  tooltip="End").add_to(m)

    elif map_type == "Heatmap":
        heat_data = df[["lat", "lng"]].values.tolist()
        HeatMap(heat_data, radius=12, blur=15, min_opacity=0.4).add_to(m)

    elif map_type == "Clustered Markers":
        cluster = MarkerCluster().add_to(m)
        for _, row in df.iterrows():
            folium.Marker(
                location=[row["lat"], row["lng"]],
                tooltip=row.get("time", ""),
            ).add_to(cluster)

    # ── Render ────────────────────────────────────────────────────────────────

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Points", f"{len(df):,}")
    col2.metric("Lat Range", f"{df['lat'].min():.4f} → {df['lat'].max():.4f}")
    col3.metric("Lng Range", f"{df['lng'].min():.4f} → {df['lng'].max():.4f}")

    st_folium(m, width="100%", height=620)

    # Raw data expander
    with st.expander("📋 Raw point data"):
        st.dataframe(df.reset_index(drop=True), use_container_width=True)

else:
    st.info("👈 Upload your `timeline.json` file from the sidebar to get started.")
    st.markdown(
        """
        **Export your file from Google Maps:**
        1. Go to [Google Takeout](https://takeout.google.com)
        2. Select **Location History (Timeline)** → **JSON format**
        3. Download and upload the file here
        """
    )