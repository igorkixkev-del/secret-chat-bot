"""
Weather Dashboard - Main Application
Fetches and displays weather data from OpenWeatherMap API
"""
import os
import sys
from datetime import datetime
from typing import Optional, Dict, List

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


class WeatherAPI:
    """Handles interactions with OpenWeatherMap API"""
    
    def __init__(self, api_key: str):
        """Initialize with API key"""
        if not api_key:
            raise ValueError("OPENWEATHERMAP_API_KEY is not set")
        self.api_key = api_key
    
    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        """
        Get current weather for a city
        
        Args:
            city: City name (e.g., "London", "New York")
            units: Temperature unit (metric, imperial)
            
        Returns:
            Weather data dictionary or None if error
        """
        try:
            url = f"{BASE_URL}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_forecast(self, city: str, units: str = "metric") -> Optional[Dict]:
        """
        Get 5-day forecast for a city
        
        Args:
            city: City name
            units: Temperature unit (metric, imperial)
            
        Returns:
            Forecast data dictionary or None if error
        """
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units,
                "cnt": 40  # 5 days * 8 (3-hour intervals)
            }
            response = requests.get(FORECAST_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None
    
    def get_weather_by_coordinates(
        self, 
        lat: float, 
        lon: float, 
        units: str = "metric"
    ) -> Optional[Dict]:
        """
        Get weather by latitude and longitude
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature unit (metric, imperial)
            
        Returns:
            Weather data dictionary or None if error
        """
        try:
            url = f"{BASE_URL}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": units
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None


class WeatherFormatter:
    """Formats weather data for display"""
    
    WEATHER_ICONS = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Smoke": "💨",
        "Haze": "🌫️",
        "Dust": "🌪️",
        "Fog": "🌫️",
        "Sand": "🌪️",
        "Ash": "💨",
        "Squall": "💨",
        "Tornado": "🌪️"
    }
    
    @staticmethod
    def get_icon(weather_main: str) -> str:
        """Get emoji icon for weather type"""
        return WeatherFormatter.WEATHER_ICONS.get(weather_main, "🌍")
    
    @staticmethod
    def format_current_weather(data: Dict, units: str = "metric") -> str:
        """
        Format current weather data for display
        
        Args:
            data: Weather data from API
            units: Temperature unit
            
        Returns:
            Formatted weather string
        """
        if not data or "main" not in data:
            return "No weather data available"
        
        city = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data["main"].get("temp", "N/A")
        feels_like = data["main"].get("feels_like", "N/A")
        humidity = data["main"].get("humidity", "N/A")
        pressure = data["main"].get("pressure", "N/A")
        wind_speed = data["wind"].get("speed", "N/A")
        wind_deg = data["wind"].get("deg", 0)
        clouds = data.get("clouds", {}).get("all", "N/A")
        description = data["weather"][0].get("main", "")
        icon = WeatherFormatter.get_icon(description)
        
        temp_unit = "°C" if units == "metric" else "°F"
        wind_unit = "m/s" if units == "metric" else "mph"
        
        output = f"""
╔══════════════════════════════════════════════════════════╗
║ {icon} WEATHER DASHBOARD - {city}, {country} {icon}
╠══════════════════════════════════════════════════════════╣
║ Current Conditions: {description}
║ Temperature: {temp}{temp_unit} (Feels like {feels_like}{temp_unit})
║ Humidity: {humidity}%
║ Pressure: {pressure} hPa
║ Wind Speed: {wind_speed} {wind_unit} (Direction: {wind_deg}°)
║ Cloud Coverage: {clouds}%
╚══════════════════════════════════════════════════════════╝
"""
        return output
    
    @staticmethod
    def format_forecast(data: Dict, units: str = "metric") -> str:
        """
        Format 5-day forecast for display
        
        Args:
            data: Forecast data from API
            units: Temperature unit
            
        Returns:
            Formatted forecast string
        """
        if not data or "list" not in data:
            return "No forecast data available"
        
        city = data.get("city", {}).get("name", "Unknown")
        country = data.get("city", {}).get("country", "")
        
        temp_unit = "°C" if units == "metric" else "°F"
        
        output = f"\n╔══════════════════════════════════════════════════════════╗\n"
        output += f"║ 5-DAY FORECAST - {city}, {country}\n"
        output += f"╠══════════════════════════════════════════════════════════╣\n"
        
        current_day = None
        for forecast in data["list"]:
            dt = datetime.fromtimestamp(forecast["dt"])
            day = dt.strftime("%A, %b %d")
            time = dt.strftime("%H:%M")
            
            if day != current_day:
                if current_day is not None:
                    output += f"╠══════════════════════════════════════════════════════════╣\n"
                current_day = day
                output += f"║ {day}\n"
                output += f"╠──────────────────────────────────────────────────────────╣\n"
            
            temp = forecast["main"]["temp"]
            feels_like = forecast["main"]["feels_like"]
            humidity = forecast["main"]["humidity"]
            description = forecast["weather"][0]["main"]
            icon = WeatherFormatter.get_icon(description)
            wind_speed = forecast["wind"]["speed"]
            rain_prob = forecast.get("pop", 0) * 100
            
            output += f"║ {time} - {icon} {description}\n"
            output += f"║   Temp: {temp}{temp_unit} (feels {feels_like}{temp_unit}) | Humidity: {humidity}%\n"
            output += f"║   Wind: {wind_speed} m/s | Rain Probability: {rain_prob:.0f}%\n"
        
        output += f"╚══════════════════════════════════════════════════════════╝\n"
        return output


class WeatherDashboard:
    """Main weather dashboard application"""
    
    def __init__(self, api_key: str):
        """Initialize dashboard"""
        self.api = WeatherAPI(api_key)
        self.formatter = WeatherFormatter()
    
    def display_current_weather(self, city: str, units: str = "metric") -> None:
        """Display current weather"""
        print(f"\n📍 Fetching current weather for {city}...")
        data = self.api.get_current_weather(city, units)
        if data:
            print(self.formatter.format_current_weather(data, units))
        else:
            print(f"❌ Could not fetch weather for {city}")
    
    def display_forecast(self, city: str, units: str = "metric") -> None:
        """Display 5-day forecast"""
        print(f"\n📍 Fetching 5-day forecast for {city}...")
        data = self.api.get_forecast(city, units)
        if data:
            print(self.formatter.format_forecast(data, units))
        else:
            print(f"❌ Could not fetch forecast for {city}")
    
    def display_multiple_cities(
        self, 
        cities: List[str], 
        units: str = "metric"
    ) -> None:
        """Display weather for multiple cities"""
        print(f"\n{'='*60}")
        print(f"{'WEATHER DASHBOARD - MULTIPLE CITIES':^60}")
        print(f"{'='*60}\n")
        
        for city in cities:
            self.display_current_weather(city, units)


def main():
    """Main application entry point"""
    if not API_KEY:
        print("❌ Error: OPENWEATHER_API_KEY is not set in .env file")
        print("Please get an API key from https://openweathermap.org/api")
        sys.exit(1)
    
    dashboard = WeatherDashboard(API_KEY)
    
    # Example usage
    print("\n" + "="*60)
    print("🌤️  WEATHER DASHBOARD".center(60))
    print("="*60)
    
    # Display weather for multiple cities
    cities = ["London", "New York", "Tokyo", "Sydney", "Paris"]
    dashboard.display_multiple_cities(cities)
    
    # Display detailed forecast
    print("\n" + "="*60)
    print("📊 DETAILED 5-DAY FORECAST".center(60))
    print("="*60)
    dashboard.display_forecast("London")


if __name__ == "__main__":
    main()
