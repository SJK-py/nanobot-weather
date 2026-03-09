import argparse
import requests
import json
import sys

# WMO Weather interpretation codes
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Drizzle: Light intensity", 53: "Drizzle: Moderate intensity", 55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity", 57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity", 63: "Rain: Moderate intensity", 65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity", 67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity", 73: "Snow fall: Moderate intensity", 75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight", 81: "Rain showers: Moderate", 82: "Rain showers: Violent",
    85: "Snow showers: Slight", 86: "Snow showers: Heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

def get_weather_description(code):
    """Helper to get string for a single code, returning 'Unknown' if not found."""
    return WEATHER_CODES.get(int(code), f"Unknown ({code})")

def translate_weather_codes(data):
    """Recursively searches for 'weather_code' or 'weathercode' and translates them."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ['weather_code', 'weathercode']:
                if isinstance(value, list):
                    data[key] = [get_weather_description(c) for c in value]
                elif isinstance(value, (int, float)):
                    data[key] = get_weather_description(value)
            else:
                translate_weather_codes(value)
    elif isinstance(data, list):
        for item in data:
            translate_weather_codes(item)
    return data

def get_coordinates(location=None):
    """Fetches coordinates from either Nominatim (location) or IP (no location)."""
    if location:
        # Nominatim STRICTLY requires a unique, descriptive User-Agent. 
        headers = {'User-Agent': 'MyCustomAIAgent_WeatherApp/1.0'}
        url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
        response = requests.get(url, headers=headers)
        
        # Check if Nominatim blocked us or returned an error
        if response.status_code != 200:
            raise ValueError(f"Nominatim API Error {response.status_code}: {response.text}")
            
        data = response.json()
        if not data:
            raise ValueError(f"Could not resolve location: {location}")
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
        ip_resp = requests.get("https://api.ipify.org?format=json")
        if ip_resp.status_code != 200:
            raise ValueError(f"IPify API Error {ip_resp.status_code}: {ip_resp.text}")
        ip = ip_resp.json().get('ip')
        
        # Note: IP-API free tier only supports HTTP, not HTTPS
        geo_resp = requests.get(f"http://ip-api.com/json/{ip}")
        if geo_resp.status_code != 200:
            raise ValueError(f"IP-API Error {geo_resp.status_code}: {geo_resp.text}")
            
        geo_data = geo_resp.json()
        if geo_data.get('status') == 'fail':
            raise ValueError(f"Could not resolve IP geocode: {geo_data.get('message')}")
        return float(geo_data['lat']), float(geo_data['lon'])

def get_unit_params(imperial):
    """Returns the unit query string based on the imperial flag."""
    if imperial:
        return "&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"
    return ""

def fetch_and_print_weather(url):
    """Fetches the Open-Meteo URL, translates codes, and prints formatted JSON."""
    response = requests.get(url)
    if response.status_code != 200:
        print(json.dumps({"error": f"API request failed with status {response.status_code}", "details": response.text}))
        return
    
    data = response.json()
    data = translate_weather_codes(data)
    print(json.dumps(data, indent=2))

def today_weather(args):
    """Handles the 'today' command."""
    lat, lon = get_coordinates(args.location)
    params = args.customparam or "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max"
    units = get_unit_params(args.imperial)
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily={params}&forecast_days=1&timezone=auto{units}"
    fetch_and_print_weather(url)

def now_weather(args):
    """Handles the 'now' command."""
    lat, lon = get_coordinates(args.location)
    params = args.customparam or "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m"
    units = get_unit_params(args.imperial)
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current={params}&timezone=auto{units}"
    fetch_and_print_weather(url)

def forecast_weather(args):
    """Handles the 'forecast' command."""
    lat, lon = get_coordinates(args.location)
    units = get_unit_params(args.imperial)
    
    if args.type == 'minutely15':
        params = args.customparam or "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m,wind_direction_10m"
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&minutely_15={params}&timezone=auto&forecast_minutely_15={args.count}{units}"
    
    elif args.type == 'hourly':
        params = args.customparam or "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m"
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly={params}&timezone=auto&forecast_hours={args.count}{units}"
    
    elif args.type == 'daily':
        params = args.customparam or "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max"
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily={params}&forecast_days={args.count}&timezone=auto{units}"
    
    fetch_and_print_weather(url)

def main():
    parser = argparse.ArgumentParser(description="Weather Helper for AI Agent")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # TODAY command
    parser_today = subparsers.add_parser('today', help="Show today's weather")
    parser_today.add_argument('--location', type=str, help="Target location (if omitted, uses IP)")
    parser_today.add_argument('--customparam', type=str, help="Comma-separated custom parameters")
    parser_today.add_argument('--imperial', action='store_true', help="Use Imperial units (mph, fahrenheit, inch)")
    parser_today.set_defaults(func=today_weather)

    # NOW command
    parser_now = subparsers.add_parser('now', help="Show current weather")
    parser_now.add_argument('--location', type=str, help="Target location (if omitted, uses IP)")
    parser_now.add_argument('--customparam', type=str, help="Comma-separated custom parameters")
    parser_now.add_argument('--imperial', action='store_true', help="Use Imperial units (mph, fahrenheit, inch)")
    parser_now.set_defaults(func=now_weather)

    # FORECAST command
    parser_forecast = subparsers.add_parser('forecast', help="Show forecast")
    parser_forecast.add_argument('--location', type=str, help="Target location (if omitted, uses IP)")
    parser_forecast.add_argument('--type', choices=['minutely15', 'hourly', 'daily'], default='hourly', help="Type of forecast")
    parser_forecast.add_argument('--count', type=int, default=4, help="Number of forecasts to retrieve")
    parser_forecast.add_argument('--customparam', type=str, help="Comma-separated custom parameters")
    parser_forecast.add_argument('--imperial', action='store_true', help="Use Imperial units (mph, fahrenheit, inch)")
    parser_forecast.set_defaults(func=forecast_weather)

    args = parser.parse_args()
    
    try:
        args.func(args)
    except Exception as e:
        # Return cleanly formatted JSON errors so the AI agent doesn't crash trying to parse stdout
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
