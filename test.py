import json
from destinations import extract_places

json_file_path = "Timeline_15_03_26.json"

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data if isinstance(data, list) else data.get("semanticSegments", data.get("timelineObjects", []))

for entry in entries[:5]:
    year = entry.get("startTime", "")[:4]
    print(f"Year: {year}")

# print(extract_places(json_file_path)[3])