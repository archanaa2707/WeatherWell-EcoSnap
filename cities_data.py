import random
from datetime import datetime

cities = [
    {'name': 'London', 'country': 'UK', 'lat': 51.5074, 'lon': -0.1278},
    {'name': 'New York', 'country': 'USA', 'lat': 40.7128, 'lon': -74.0060},
    {'name': 'Tokyo', 'country': 'Japan', 'lat': 35.6762, 'lon': 139.6503},
    {'name': 'Sydney', 'country': 'Australia', 'lat': -33.8688, 'lon': 151.2093},
    {'name': 'Paris', 'country': 'France', 'lat': 48.8566, 'lon': 2.3522},
    {'name': 'Dubai', 'country': 'UAE', 'lat': 25.2048, 'lon': 55.2708},
    {'name': 'Singapore', 'country': 'Singapore', 'lat': 1.3521, 'lon': 103.8198},
    {'name': 'Toronto', 'country': 'Canada', 'lat': 43.6532, 'lon': -79.3832},
    {'name': 'Berlin', 'country': 'Germany', 'lat': 52.5200, 'lon': 13.4050},
    {'name': 'Mumbai', 'country': 'India', 'lat': 19.0760, 'lon': 72.8777},
    {'name': 'Cape Town', 'country': 'South Africa', 'lat': -33.9249, 'lon': 18.4241},
    {'name': 'Rio de Janeiro', 'country': 'Brazil', 'lat': -22.9068, 'lon': -43.1729},
    {'name': 'Beijing', 'country': 'China', 'lat': 39.9042, 'lon': 116.4074},
    {'name': 'Moscow', 'country': 'Russia', 'lat': 55.7558, 'lon': 37.6173},
    {'name': 'Los Angeles', 'country': 'USA', 'lat': 34.0522, 'lon': -118.2437},
    {'name': 'Barcelona', 'country': 'Spain', 'lat': 41.3851, 'lon': 2.1734},
    {'name': 'Rome', 'country': 'Italy', 'lat': 41.9028, 'lon': 12.4964},
    {'name': 'Amsterdam', 'country': 'Netherlands', 'lat': 52.3676, 'lon': 4.9041},
    {'name': 'Bangkok', 'country': 'Thailand', 'lat': 13.7563, 'lon': 100.5018},
    {'name': 'Seoul', 'country': 'South Korea', 'lat': 37.5665, 'lon': 126.9780},
    {'name': 'Vancouver', 'country': 'Canada', 'lat': 49.2827, 'lon': -123.1207},
    {'name': 'Zurich', 'country': 'Switzerland', 'lat': 47.3769, 'lon': 8.5417},
    {'name': 'Stockholm', 'country': 'Sweden', 'lat': 59.3293, 'lon': 18.0686},
    {'name': 'Auckland', 'country': 'New Zealand', 'lat': -36.8485, 'lon': 174.7633},
    {'name': 'Honolulu', 'country': 'USA', 'lat': 21.3069, 'lon': -157.8583},
    {'name': 'Reykjavik', 'country': 'Iceland', 'lat': 64.1466, 'lon': -21.9426},
    {'name': 'Geneva', 'country': 'Switzerland', 'lat': 46.2044, 'lon': 6.1432},
    {'name': 'Oslo', 'country': 'Norway', 'lat': 59.9139, 'lon': 10.7522},
    {'name': 'Edinburgh', 'country': 'UK', 'lat': 55.9533, 'lon': -3.1883},
    {'name': 'Dublin', 'country': 'Ireland', 'lat': 53.3498, 'lon': -6.2603}
]

def get_weather_data(city_name):
    """Simulate weather data with seasonal variations"""
    city = next((c for c in cities if c['name'] == city_name), None)
    if not city:
        return {}
    
    northern = city['lat'] > 0
    month = datetime.now().month
    if northern:
        if month in [12, 1, 2]: 
            base_temp = random.uniform(-10, 10)
            uv = random.uniform(1, 3)
        elif month in [3, 4, 5]: 
            base_temp = random.uniform(10, 20)
            uv = random.uniform(3, 6)
        elif month in [6, 7, 8]:  
            base_temp = random.uniform(20, 35)
            uv = random.uniform(6, 10)
        else: 
            base_temp = random.uniform(10, 20)
            uv = random.uniform(3, 6)
    else:
        if month in [12, 1, 2]:  
            base_temp = random.uniform(20, 35)
            uv = random.uniform(6, 10)
        elif month in [3, 4, 5]:  
            base_temp = random.uniform(10, 20)
            uv = random.uniform(3, 6)
        elif month in [6, 7, 8]:  
            base_temp = random.uniform(-10, 10)
            uv = random.uniform(1, 3)
        else: 
            base_temp = random.uniform(10, 20)
            uv = random.uniform(3, 6)

    lat_factor = abs(city['lat']) / 90
    temperature = base_temp * (1 - lat_factor * 0.5) + random.uniform(-5, 5)
    humidity = random.uniform(30, 90)
    if city['name'] in ['New York', 'Beijing', 'Mumbai', 'Los Angeles']:
        dust = random.uniform(150, 400)
        smoke = random.uniform(100, 300)
    else:
        dust = random.uniform(20, 150)
        smoke = random.uniform(10, 100)
    
    if (northern and month in [3, 4, 5]) or (not northern and month in [9, 10, 11]):
        pollen = random.uniform(200, 500)
    else:
        pollen = random.uniform(10, 100)
    
    return {
        'temperature': round(temperature, 1),
        'uv_index': round(uv, 1),
        'humidity': round(humidity, 1),
        'dust': round(dust),
        'smoke': round(smoke),
        'pollen': round(pollen)
    }