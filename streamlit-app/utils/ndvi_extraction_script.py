import ee
import json

ee.Initialize(project="vayu-493210")

cities = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Ahmedabad": (23.0225, 72.5714),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Surat": (21.1702, 72.8311),
    "Kanpur": (26.4499, 80.3319),
    "Nagpur": (21.1458, 79.0882),
    "Bhopal": (23.2599, 77.4126),
    "Patna": (25.5941, 85.1376),
}

results = {}

for city, (lat,lon) in cities.items():
    point = ee.Geometry.Point([lon,lat])

    image = (
        ee.ImageCollection("MODIS/061/MOD13Q1").filterDate("2025-12-13", "2026-04-13").mean().select("NDVI")
    )

    # reducing region to 10km radius around city and scaling
    ndvi_raw = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point.buffer(10000),  # 10km radius around city center
        scale=250 # MODIS resolution
    ).getInfo()

    ndvi = ndvi_raw.get("NDVI", None)
    results[city] = round(ndvi * 0.0001, 4) if ndvi else None # MODIS stores as integers, *0.001 converts to original NDVI value, rounded to 4 decimal places
    print(f"{city}: {results[city]}")

with open("city_ndvi.json", "w") as f:
    json.dump(results, f, indent=2)

print("saved to city_ndvi.json") # saves to json