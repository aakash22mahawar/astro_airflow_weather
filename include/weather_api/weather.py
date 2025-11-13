import requests
from datetime import datetime as dt
from logging_config import setup_logger

# Initialize the logger
logger = setup_logger()

# API configuration
API_KEY = "xxxxxxx"
BASE_URL = "https://api.weatherstack.com/current"


def fetch_weather():
    """Fetch current weather data for a given city."""
    params = {
        "access_key": API_KEY,
        "query": "New Delhi"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:

            data = response.json()
            location = data.get("location", {})
            current = data.get("current", {})
            astro = current.get("astro", {})

            weather_data = {
                'city': location.get('name'),
                'country': location.get('country'),
                'timezone': location.get('timezone_id'),
                'observed_time': dt.strptime(location.get('localtime'), '%Y-%m-%d %H:%M').strftime('%d-%m-%Y %H:%M'),
                'temperature': current.get('temperature'),
                'sunrise': astro.get('sunrise'),
                'sunset': astro.get('sunset'),
                'moonrise': astro.get('moonrise'),
                'moonset': astro.get('moonset'),
                'moonphase': astro.get('moon_phase')
            }
            logger.info(f'Weather info has been fetched successfully : {response.status_code}')
            return weather_data

    except Exception as e:
        logger.error(f"Error processing data: {e}")


# # Example usage
# if __name__ == "__main__":
#     city_name = "New Delhi"
#     fetch_weather()


