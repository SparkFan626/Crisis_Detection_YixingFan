import pandas as pd
import spacy
from collections import Counter
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium
from folium.plugins import HeatMap

# ========== Step 1: Load the CSV ==========
print("📥 Reading CSV...")
df = pd.read_csv("output/task1_filtered_reddit_posts.csv")  # Adjusted to your output folder
nlp = spacy.load("en_core_web_sm")

# ========== Step 2: Extract location entities using spaCy ==========
print("📍 Extracting location entities...")
locations = []
for doc in nlp.pipe(df["content"].astype(str), disable=["tagger", "parser", "textcat"]):
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            locations.append(ent.text.strip().lower())

# ========== Step 3: Filter out false positives (non-geographic terms) ==========
banlist = {"netflix", "phobia", "backgrounda", "us", "america", "china", "earth"}
filtered_locations = [loc for loc in locations if loc not in banlist]

# ========== Step 4: Geocode North America-based locations ==========
print("\n🗺️ Geocoding locations (North America only)...")
geolocator = Nominatim(user_agent="gsoc_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

geo_points = []  # For heatmap
na_location_counts = Counter()  # For frequency stats
top_markers = []  # For top 5 markers

for loc, count in Counter(filtered_locations).items():
    try:
        geo = geocode(loc)
        if geo and any(country in geo.address.lower() for country in ["united states", "canada", "mexico"]):
            geo_points.append([geo.latitude, geo.longitude, count])
            na_location_counts[loc] = count
        # else:
        #     print(f"🚫 Skipped (not in North America): {loc}")
    except Exception as e:
        print(f"❌ Error geocoding {loc}: {e}")

# ========== Step 5: Display top 5 locations in North America ==========
top_na_locations = na_location_counts.most_common(5)
print("\n🌎 Top 5 North American Locations:")
for name, count in top_na_locations:
    print(f"{name.title()} — {count} mentions")

# Add top 5 markers
for name, count in top_na_locations:
    geo = geocode(name)
    if geo:
        top_markers.append((name.title(), geo.latitude, geo.longitude, count))
        print(f"✅ Geocoded Top Location: {name.title()} -> ({geo.latitude}, {geo.longitude})")

# ========== Step 6: Create and save the heatmap ==========
print("\n🧪 Generating map...")
m = folium.Map(location=[39.5, -98.35], zoom_start=4)

# Add heatmap layer
HeatMap(geo_points, radius=20, blur=15).add_to(m)

# Add marker layer for top 5
for name, lat, lon, count in top_markers:
    folium.Marker(
        location=[lat, lon],
        popup=f"{name}: {count} posts",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Save as HTML
m.save("output/task3_crisis_heatmap.html")
print("\n✅ Map saved as output/task3_crisis_heatmap.html")
