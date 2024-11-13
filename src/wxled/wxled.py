import requests
import time
from gpiozero import RGBLED
import json
from datetime import datetime

class WxLED:
    def __init__(self, red_pin=17, green_pin=27, blue_pin=22):
        """Initialize the RGB LED and API settings."""
        # Initialize the RGB LED
        self.led = RGBLED(red=red_pin, green=green_pin, blue=blue_pin)
        
        # NWS API base URL
        self.base_url = "https://api.weather.gov"
        # Set a proper user agent as required by NWS API
        self.headers = {
            "User-Agent": "(WeatherLED, your@email.com)",
            "Accept": "application/json"
        }

    def get_weather_color(self, condition, temperature=None):
        """Convert weather conditions to RGB values (0-1 for RGBLED)."""
        weather_colors = {
            "clear": (1, 0.8, 0),        # Bright yellow
            "sunny": (1, 0.8, 0),        # Bright yellow
            "mostly clear": (0.8, 0.6, 0),  # Slightly dimmed yellow
            "partly cloudy": (0.8, 0.8, 0.8),  # Light grey
            "mostly cloudy": (0.5, 0.5, 0.5),  # Grey
            "cloudy": (0.4, 0.4, 0.4),   # Darker grey
            "rain": (0, 0.4, 1),         # Blue
            "snow": (0.8, 0.8, 1),       # Pale blue-white
            "thunderstorm": (1, 0, 1),   # Purple
            "fog": (0.7, 0.7, 0.7),      # Misty grey
            "wind": (0, 1, 0.4),         # Blue-green
        }
        
        # Get base color, default to off if condition not found
        base_color = list(weather_colors.get(condition.lower(), (0, 0, 0)))
        
        # Adjust for temperature if provided
        if temperature is not None:
            if temperature > 30:  # Hot
                base_color[0] = min(1, base_color[0] + 0.2)  # Add red
            elif temperature < 0:  # Cold
                base_color[2] = min(1, base_color[2] + 0.2)  # Add blue
                
        return tuple(base_color)

    def get_coordinates(self, zip_code):
        """Convert ZIP code to coordinates using NWS API."""
        try:
            # You might want to use a geocoding service here
            # For demo, returning example coordinates
            # Replace with actual geocoding service
            return (37.7749, -122.4194)  # Example coordinates
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None

    def get_forecast_url(self, lat, lon):
        """Get the forecast URL for the given coordinates."""
        try:
            points_url = f"{self.base_url}/points/{lat},{lon}"
            response = requests.get(points_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data['properties']['forecast']
        except Exception as e:
            print(f"Error getting forecast URL: {e}")
            return None

    def get_current_weather(self, forecast_url):
        """Get current weather from NWS API."""
        try:
            response = requests.get(forecast_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Get the current period's forecast
            current_period = data['properties']['periods'][0]
            
            return {
                'condition': current_period['shortForecast'],
                'temperature': current_period['temperature']
            }
        except Exception as e:
            print(f"Error getting weather: {e}")
            return None

    def update_led(self, weather_data):
        """Update LED colors based on weather data."""
        if weather_data:
            rgb = self.get_weather_color(
                weather_data['condition'],
                weather_data['temperature']
            )
            self.led.color = rgb
            print(f"LED updated - Condition: {weather_data['condition']}, "
                  f"Temperature: {weather_data['temperature']}°F, RGB: {rgb}")
        else:
            # Error indication - blink red
            self.led.color = (1, 0, 0)
            time.sleep(0.5)
            self.led.color = (0, 0, 0)
            time.sleep(0.5)

    def run(self, zip_code, update_interval=300):
        """Main loop to continuously update the LED."""
        print(f"Starting Weather LED for ZIP code {zip_code}")
        
        # Get coordinates for the ZIP code
        coords = self.get_coordinates(zip_code)
        if not coords:
            print("Failed to get coordinates")
            return
            
        # Get the forecast URL for the location
        forecast_url = self.get_forecast_url(*coords)
        if not forecast_url:
            print("Failed to get forecast URL")
            return

        while True:
            try:
                # Get current weather
                weather_data = self.get_current_weather(forecast_url)
                
                # Update the LED
                self.update_led(weather_data)
                
                # Wait for next update
                time.sleep(update_interval)
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.led.close()
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    # Initialize and run the weather LED
    # Adjust these pins according to your wiring
    weather_led = WxLED(red_pin=17, green_pin=27, blue_pin=22)
    weather_led.run(zip_code="94105", update_interval=300)  # Updates every 5 minutes