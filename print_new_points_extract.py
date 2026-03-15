import folium
from destinations import extract_places




def plot_points(places, output_html="map.html"):


    m = folium.Map()

    for p in places:
        folium.CircleMarker(
            location=[p["lat"], p["lng"]],
            radius=3,
            color="#3388ff",
            fill=True,
            fill_opacity=0.7,
        ).add_to(m)

    m.save(output_html)
    print(f"✅ {len(places)} places plotted → {output_html}")

plot_points(extract_places("Timeline_15_03_26.json", output_file_path="points_output.json")[0], output_html="map.html")