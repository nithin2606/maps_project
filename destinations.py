import json

def extract_places(json_file_path, output_file_path=None):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    places = []

    # Handle both list (array) and dict wrapper
    entries = data if isinstance(data, list) else data.get("semanticSegments", data.get("timelineObjects", []))

    for entry in entries:
        visit = entry.get("visit", {})
        top_candidate = visit.get("topCandidate", {})
        place_location = top_candidate.get("placeLocation", {})
        lat_lang = place_location.get("latLng","")
        if lat_lang:
            lat, lng = lat_lang.split(',')
            lat = lat.rstrip('°')
            lng = lng.rstrip('°')

            if {"lat": float(lat), "lng": float(lng)} not in places:
                places.append({"lat": float(lat), "lng": float(lng)})


    print(f"Total destinations extracted: {len(places)}")
    for p in places[:5]:  # Preview first 5
        print(p)

    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(places, f, indent=2)
        print(f"\nSaved to {output_file_path}")

    return places


places = extract_places("Timeline_15_03_26.json", output_file_path="destinations_output.json")