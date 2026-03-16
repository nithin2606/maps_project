import json

def extract_places(json_file_path, output_file_path=None):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    places = []
    dup_places = []
    places_id = []
    dup_places_id = []

    # Handle both list (array) and dict wrapper
    entries = data if isinstance(data, list) else data.get("semanticSegments", data.get("timelineObjects", []))

    for entry in entries:
        year = entry.get("startTime", "")[:4]  # Extract year from startTime
        visit = entry.get("visit", {})
        top_candidate = visit.get("topCandidate", {})
        place_id = top_candidate.get("placeId", "")
        place_location = top_candidate.get("placeLocation", {})
        lat_lang = place_location.get("latLng","")
        if lat_lang:
            lat, lng = lat_lang.split(',')
            lat = lat.rstrip('°')
            lng = lng.rstrip('°')

            if {"lat": lat, "lng": lng} not in [{"lat": p["lat"], "lng": p["lng"]} for p in places]:
                places.append({"lat": lat, "lng": lng, "year": year})

            dup_places.append({"lat": lat, "lng": lng, "year": year})

        if place_id:
            dup_places_id.append({"place_id": place_id, "year": year})
            if place_id not in places_id:
                places_id.append({"place_id": place_id, "year": year})



    # print(f"Total destinations extracted: {len(places)}")
    # for p in places[:5]:  # Preview first 5
    #     print(p)

    # if output_file_path:
    #     with open(output_file_path, 'w', encoding='utf-8') as f:
    #         json.dump(places, f, indent=2)
    #     print(f"\nSaved to {output_file_path}")

    return places, dup_places, places_id, dup_places_id

