import folium

def create_map():
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)

    folium.Marker(
        location=[12.9716, 77.5946],
        popup="Bangalore",
        tooltip="Click me"
    ).add_to(m)
    return m
