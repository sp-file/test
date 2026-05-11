#!/usr/bin/env python3
"""
Weather Analyzer - A tool to fetch and analyze weather data
This program retrieves weather information and provides insights about conditions,
temperature trends, and recommendations.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class WeatherAnalyzer:
    """Analyzes weather patterns and provides recommendations."""
    
    def __init__(self, city: str = "San Francisco"):
        self.city = city
        self.weather_data = self._generate_weather_data()
    
    def _generate_weather_data(self) -> List[Dict]:
        """Generate realistic weather data for analysis."""
        base_temp = random.randint(55, 85)
        data = []
        
        for day in range(7):
            date = datetime.now() + timedelta(days=day)
            temp_variation = random.randint(-5, 5)
            humidity = random.randint(30, 90)
            conditions = random.choice([
                "Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Windy", "Clear"
            ])
            
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%A"),
                "temperature": base_temp + temp_variation,
                "humidity": humidity,
                "condition": conditions,
                "wind_speed": random.randint(5, 25)
            })
        
        return data
    
    def get_average_temperature(self) -> float:
        """Calculate average temperature for the week."""
        temps = [day["temperature"] for day in self.weather_data]
        return round(sum(temps) / len(temps), 1)
    
    def get_recommendation(self) -> str:
        """Provide activity recommendation based on weather."""
        avg_temp = self.get_average_temperature()
        
        if avg_temp < 50:
            return "🧊 Bundle up! Perfect weather for winter sports or indoor activities."
        elif avg_temp < 65:
            return "🧥 Mild weather - great for hiking or light outdoor activities."
        elif avg_temp < 80:
            return "☀️ Beautiful weather! Ideal for outdoor adventures and picnics."
        else:
            return "🌡️ Hot days ahead - stay hydrated and seek shade when possible."
    
    def find_best_day(self) -> Dict:
        """Find the best day for outdoor activities."""
        best_day = max(
            self.weather_data,
            key=lambda x: (
                x["temperature"],
                -x["humidity"],
                1 if x["condition"] in ["Sunny", "Clear"] else 0
            )
        )
        return best_day
    
    def display_forecast(self) -> None:
        """Display the 7-day forecast."""
        print(f"\n{'='*60}")
        print(f"📍 Weather Forecast for {self.city}")
        print(f"{'='*60}\n")
        
        for day in self.weather_data:
            print(f"📅 {day['day']} ({day['date']})")
            print(f"   🌡️  Temperature: {day['temperature']}°F")
            print(f"   💧 Humidity: {day['humidity']}%")
            print(f"   🌤️  Condition: {day['condition']}")
            print(f"   💨 Wind: {day['wind_speed']} mph")
            print()
    
    def run_analysis(self) -> None:
        """Run complete weather analysis."""
        self.display_forecast()
        
        print(f"{'='*60}")
        print("📊 ANALYSIS & RECOMMENDATIONS")
        print(f"{'='*60}\n")
        
        avg_temp = self.get_average_temperature()
        print(f"📈 Average Temperature: {avg_temp}°F")
        print(f"💡 Recommendation: {self.get_recommendation()}\n")
        
        best_day = self.find_best_day()
        print(f"✨ Best Day for Activities: {best_day['day']} ({best_day['date']})")
        print(f"   Conditions: {best_day['condition']}, {best_day['temperature']}°F")
        print(f"\n{'='*60}\n")


def main():
    """Main entry point."""
    print("\n🌍 Welcome to Weather Analyzer!\n")
    
    # Create analyzer for different cities
    cities = ["San Francisco", "New York", "Miami", "Seattle", "Denver"]
    city = random.choice(cities)
    
    analyzer = WeatherAnalyzer(city=city)
    analyzer.run_analysis()
    
    print("✅ Analysis complete!")


if __name__ == "__main__":
    main()
