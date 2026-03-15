import json

def extract_points(json_file_path, output_file_path=None):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    points = []


    entries = data if isinstance(data, list) else data.get("semanticSegments", data.get("timelineObjects", []))

    for entry in entries:
        for path_point in entry.get("timelinePath", []):
            point = path_point.get("point")
            time  = path_point.get("time")
            if point:
                lat, lng = point.split(',')
                lat = lat.rstrip('°')
                lng = lng.rstrip('°')
                points.append({"lat": float(lat), "lng": float(lng), "time": time})

    print(f"Total points extracted: {len(points)}")
    for p in points[:5]:
        print(p)

    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            pass
        print("file cleared")
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.truncate(0)
            json.dump(points, f, indent=2)
        print(f"\nSaved to {output_file_path}, {len(points)} points.")

    return points

points = extract_points("Timeline_15_03_26.json", output_file_path="points_output.json")