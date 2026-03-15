import matplotlib.pyplot as plt
from destinations import extract_places

places_id = extract_places("Timeline_15_03_26.json")[2]

print(f"Total unique place IDs extracted: {len(places_id)}")

for p in places_id[:10]:
    print(p)

