import datetime
from zoneinfo import ZoneInfo
import requests
import os

from django.shortcuts import render
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def home(request):
    """Main page with trip planning form."""
    return render(request, 'trip_planner/home.html')

def plan_trip(request):
    """Handle basic trip planning requests."""
    if request.method == 'POST':
        return JsonResponse({'success': True, 'message': 'Plan trip endpoint working'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_weather(request):
    """Get weather for a specific city."""
    if request.method == 'POST':
        return JsonResponse({'success': True, 'message': 'Weather endpoint working'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def comprehensive_plan(request):
    """Get comprehensive trip plan."""
    if request.method == 'POST':
        return JsonResponse({'success': True, 'message': 'Comprehensive plan endpoint working'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_current_weather(city: str) -> dict:
    """Gets current weather information for a city using WeatherAPI.com."""
    api_key = os.getenv('WEATHERAPI_KEY')
    if not api_key:
        return {
            "status": "error",
            "error_message": "Weather API key not configured. Please set WEATHERAPI_KEY in your .env file."
        }

    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': city.strip(),
        'aqi': 'no'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        current = weather_data['current']
        location_data = weather_data['location']

        return {
            "status": "success",
            "location": f"{location_data['name']}, {location_data['region']}, {location_data['country']}",
            "current_weather": {
                "temperature": f"{current['temp_c']}°C ({current['temp_f']}°F)",
                "feels_like": f"{current['feelslike_c']}°C ({current['feelslike_f']}°F)",
                "description": current['condition']['text'],
                "humidity": f"{current['humidity']}%",
                "wind_speed": f"{current['wind_kph']} km/h ({current['wind_mph']} mph)",
                "visibility": f"{current['vis_km']} km",
                "uv_index": current['uv'],
                "pressure": f"{current['pressure_mb']} mb"
            },
            "local_time": location_data['localtime']
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Could not get weather for '{city}': {str(e)}"
        }


def smart_destination_info(destination: str, search_online: bool = False) -> dict:
    """Provides comprehensive destination information using database and AI knowledge."""

    destinations = {
        "paris": {
            "status": "success",
            "source": "database",
            "info": {
                "best_time_to_visit": "April-June, September-October",
                "top_attractions": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Champs-Élysées"],
                "budget_estimate": "$150-300 per day",
                "climate": "Temperate oceanic climate",
                "local_currency": "Euro (EUR)",
                "language": "French",
                "travel_tips": "Book museum tickets in advance, learn basic French phrases, wear comfortable walking shoes"
            }
        },
        "tokyo": {
            "status": "success",
            "source": "database",
            "info": {
                "best_time_to_visit": "March-May, September-November",
                "top_attractions": ["Tokyo Skytree", "Senso-ji Temple", "Shibuya Crossing", "Meiji Shrine"],
                "budget_estimate": "$200-400 per day",
                "climate": "Humid subtropical climate",
                "local_currency": "Japanese Yen (JPY)",
                "language": "Japanese",
                "travel_tips": "Get a JR Pass for trains, carry cash, bow slightly when greeting, remove shoes indoors"
            }
        },
        "rome": {
            "status": "success",
            "source": "database",
            "info": {
                "best_time_to_visit": "April-June, September-October",
                "top_attractions": ["Colosseum", "Vatican City", "Trevi Fountain", "Roman Forum"],
                "budget_estimate": "$120-250 per day",
                "climate": "Mediterranean climate",
                "local_currency": "Euro (EUR)",
                "language": "Italian",
                "travel_tips": "Validate train tickets, dress modestly for churches, eat lunch late (1-3pm)"
            }
        }
    }

    destination_key = destination.lower().strip()

    if destination_key in destinations:
        return destinations[destination_key]
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have detailed information for '{destination}'. I currently have info for Paris, Tokyo, and Rome."
        }


def create_itinerary(destination: str, days: int) -> dict:
    """Creates a sample vacation itinerary for a destination."""
    if days < 1 or days > 7:
        return {
            "status": "error",
            "error_message": "I can create itineraries for 1-7 days only."
        }

    itineraries = {
        "paris": {
            1: ["Visit Eiffel Tower", "Walk along Seine River", "Dinner in Latin Quarter"],
            2: ["Louvre Museum", "Notre-Dame Cathedral", "Evening river cruise"],
            3: ["Versailles day trip", "Palace and gardens tour", "Return to Paris for dinner"]
        },
        "tokyo": {
            1: ["Sensoji Temple", "Asakusa district", "Traditional dinner"],
            2: ["Tokyo Skytree", "Sumida River area", "Robot Restaurant show"],
            3: ["Meiji Shrine", "Harajuku fashion district", "Shibuya crossing"]
        },
        "rome": {
            1: ["Colosseum tour", "Roman Forum", "Palatine Hill"],
            2: ["Vatican City", "Sistine Chapel", "St. Peter's Basilica"],
            3: ["Trevi Fountain", "Spanish Steps", "Pantheon visit"]
        }
    }

    destination_key = destination.lower().strip()

    if destination_key not in itineraries:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have itineraries for '{destination}'. Available destinations: Paris, Tokyo, Rome."
        }

    itinerary = []
    for day in range(1, days + 1):
        if day <= len(itineraries[destination_key]):
            itinerary.append({
                f"Day {day}": itineraries[destination_key][day]
            })
        else:
            itinerary.append({
                f"Day {day}": ["Free day", "Explore at your own pace", "Local experiences"]
            })

    return {
        "status": "success",
        "destination": destination.title(),
        "duration": f"{days} days",
        "itinerary": itinerary
    }


def get_travel_budget(destination: str, days: int, budget_level: str = "medium") -> dict:
    """Estimates travel budget for a vacation."""
    if days < 1:
        return {
            "status": "error",
            "error_message": "Duration must be at least 1 day."
        }

    budget_multipliers = {
        "low": 0.7,
        "medium": 1.0,
        "high": 1.5
    }

    if budget_level.lower() not in budget_multipliers:
        return {
            "status": "error",
            "error_message": "Budget level must be 'low', 'medium', or 'high'."
        }

    base_costs = {
        "paris": {"daily": 225, "flight": 800, "accommodation": 120},
        "tokyo": {"daily": 300, "flight": 1200, "accommodation": 150},
        "rome": {"daily": 185, "flight": 700, "accommodation": 100}
    }

    destination_key = destination.lower().strip()
    if destination_key not in base_costs:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have budget information for '{destination}'."
        }

    multiplier = budget_multipliers[budget_level.lower()]
    costs = base_costs[destination_key]

    daily_cost = int(costs["daily"] * multiplier)
    flight_cost = int(costs["flight"] * multiplier)
    accommodation_cost = int(costs["accommodation"] * multiplier * days)
    food_entertainment = int(daily_cost * days * 0.6)
    transportation = int(daily_cost * days * 0.2)
    activities = int(daily_cost * days * 0.2)

    total_cost = flight_cost + accommodation_cost + food_entertainment + transportation + activities

    return {
        "status": "success",
        "destination": destination.title(),
        "duration": f"{days} days",
        "budget_level": budget_level.title(),
        "breakdown": {
            "flights": f"${flight_cost}",
            "accommodation": f"${accommodation_cost}",
            "food_and_entertainment": f"${food_entertainment}",
            "local_transportation": f"${transportation}",
            "activities_and_tours": f"${activities}",
            "total_estimated_cost": f"${total_cost}"
        },
        "daily_average": f"${daily_cost}"
    }


def create_comprehensive_trip_plan(destination: str, days: int = 3, budget_level: str = "medium") -> dict:
    """Creates a comprehensive trip plan with all details for a destination."""

    # For now, return basic plan - you can expand this later
    dest_info = smart_destination_info(destination)
    itinerary = create_itinerary(destination, days)
    budget = get_travel_budget(destination, days, budget_level)
    weather = get_current_weather(destination)

    return {
        "status": "success",
        "trip_header": f"Amazing {destination.title()} Adventure!",
        "trip_appeal": f"Discover the wonders of {destination.title()} in this carefully planned {days}-day journey.",
        "weather_info": weather,
        "destination_info": dest_info,
        "itinerary": itinerary,
        "budget": budget
    }