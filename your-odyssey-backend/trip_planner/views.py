
from django.shortcuts import render
from django.http import JsonResponse
import json
import os
from dotenv import load_dotenv
from .agent_functions import get_current_weather, create_comprehensive_trip_plan


# Load environment variables
load_dotenv()

def home(request):
    """Main page with trip planning form."""
    return render(request, 'trip_planner/home.html')

def plan_trip(request):
    """Handle basic trip planning requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            destination = data.get('destination', '')
            days = int(data.get('days', 3))
            budget_level = data.get('budget_level', 'medium')
            
            # Get weather
            weather = get_current_weather(destination)
            
            # Basic itinerary (you can expand this)
            basic_itinerary = {
                "status": "success",
                "destination": destination.title(),
                "duration": f"{days} days",
                "itinerary": [
                    {"Day 1": ["Arrival and city orientation", "Visit main landmark", "Local dinner"]},
                    {"Day 2": ["Major museum or cultural site", "Historic district exploration", "Traditional cuisine"]},
                    {"Day 3": ["Day trip or nature activity", "Local markets", "Evening entertainment"]}
                ][:days]
            }
            
            # Basic budget (simplified)
            budget = {
                "status": "success",
                "destination": destination.title(),
                "duration": f"{days} days",
                "budget_level": budget_level.title(),
                "breakdown": {
                    "flights": "$800",
                    "accommodation": f"${120 * days}",
                    "food_and_entertainment": f"${100 * days}",
                    "local_transportation": f"${30 * days}",
                    "activities_and_tours": f"${80 * days}",
                    "total_estimated_cost": f"${800 + 330 * days}"
                }
            }
            
            return JsonResponse({
                'success': True,
                'weather': weather,
                'itinerary': basic_itinerary,
                'budget': budget
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_weather(request):
    """Get weather for a specific city."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city = data.get('city', '')
            
            weather_data = get_current_weather(city)
            
            return JsonResponse({
                'success': True,
                'weather': weather_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from .agent_functions import get_current_weather, create_comprehensive_trip_plan

def comprehensive_plan(request):
    """Get comprehensive trip plan with all details."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            destination = data.get('destination', '')
            days = int(data.get('days', 3))
            budget_level = data.get('budget_level', 'medium')
            
            comprehensive_data = create_comprehensive_trip_plan(destination, days, budget_level)
            
            return JsonResponse({
                'success': True,
                'plan': comprehensive_data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def generate_ai_trip_plan(destination: str, days: int = 3, budget_level: str = "medium") -> dict:
    """Generate comprehensive trip plan using AI for any destination."""
    
    # This is a template for how you could integrate with an AI service
    # You could use your Google API key to call Gemini API directly
    
    try:
        # For now, let's create a smart template-based system
        # In a real implementation, you'd call the Gemini API here
        
        current_month = datetime.datetime.now().month
        if current_month in [3, 4, 5]:
            current_season = "spring"
        elif current_month in [6, 7, 8]:
            current_season = "summer"
        elif current_month in [9, 10, 11]:
            current_season = "fall"
        else:
            current_season = "winter"
        
        # Get weather data
        weather_data = get_current_weather(destination)
        
        # Generate AI-style comprehensive plan
        ai_plan = {
            "status": "success",
            "trip_header": f"Discover Amazing {destination.title()}!",
            "destination": destination.title(),
            "duration": f"{days} days",
            "trip_appeal": f"Experience the unique charm and culture of {destination.title()} with carefully curated activities that showcase the best this destination has to offer.",
            "weather_info": weather_data,
            "timezone_info": {
                "timezone": "Local timezone information",
                "time_difference": "Please check current time difference"
            },
            "seasonal_activities": generate_seasonal_activities(destination, current_season),
            "language_guide": generate_language_guide(destination),
            "cultural_info": generate_cultural_info(destination),
            "exchange_rate": "Please check current exchange rates",
            "daily_itinerary": generate_ai_itinerary(destination, days)
        }
        
        return ai_plan
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating trip plan: {str(e)}"
        }

def generate_seasonal_activities(destination: str, season: str) -> list:
    """Generate season-appropriate activities for any destination."""
    
    # Template activities based on season and destination type
    base_activities = {
        "spring": [
            f"Explore {destination}'s parks and gardens in bloom",
            f"Outdoor walking tours of {destination}",
            f"Local spring festivals and events in {destination}"
        ],
        "summer": [
            f"Outdoor dining and café culture in {destination}",
            f"Summer festivals and concerts in {destination}",
            f"Early morning or evening sightseeing to avoid heat"
        ],
        "fall": [
            f"Autumn scenery and foliage tours in {destination}",
            f"Harvest festivals and seasonal markets in {destination}",
            f"Perfect weather for extensive walking tours"
        ],
        "winter": [
            f"Indoor cultural attractions in {destination}",
            f"Winter holiday celebrations and markets",
            f"Cozy local dining experiences"
        ]
    }
    
    return base_activities.get(season, base_activities["spring"])

def generate_language_guide(destination: str) -> dict:
    """Generate basic language information for destination."""
    
    # This is where you could integrate with a language API or database
    # For now, providing general guidance
    
    return {
        "language": "Local language",
        "common_phrases": [
            "Hello - Local greeting",
            "Thank you - Expression of gratitude",
            "Excuse me - Polite attention getter",
            "Do you speak English? - Language inquiry",
            "Where is...? - Asking for directions"
        ]
    }

def generate_cultural_info(destination: str) -> dict:
    """Generate cultural etiquette and practical info."""
    
    return {
        "etiquette_and_norms": [
            "Research local customs before visiting",
            "Dress appropriately for religious or cultural sites",
            "Learn about local tipping practices",
            "Be respectful of local traditions and values",
            "Try to learn basic phrases in the local language"
        ],
        "electrical_plug": "Check local electrical standards for your devices"
    }

def generate_ai_itinerary(destination: str, days: int) -> list:
    """Generate AI-style itinerary for any destination."""
    
    itinerary = []
    
    themes = [
        "Arrival and Exploration",
        "Cultural Immersion", 
        "Local Experiences",
        "Historical Discovery",
        "Nature and Relaxation",
        "Shopping and Dining",
        "Hidden Gems"
    ]
    
    for day in range(1, days + 1):
        theme = themes[(day - 1) % len(themes)]
        
        day_plan = {
            "day_number": day,
            "theme": f"{theme} Day",
            "morning": f"Explore {destination}'s main attractions and landmarks",
            "afternoon": f"Visit local markets, museums, or cultural sites in {destination}",
            "evening": f"Experience {destination}'s dining scene and nightlife",
            "hotel_area": f"Central area of {destination} for easy access to attractions",
            "restaurant": f"Highly-rated local restaurant featuring {destination}'s cuisine"
        }
        
        # Customize based on day number
        if day == 1:
            day_plan["morning"] = f"Arrival in {destination} and hotel check-in"
            day_plan["afternoon"] = f"Walking tour of {destination}'s main district"
            day_plan["evening"] = f"Welcome dinner featuring local specialties"
        elif day == days:
            day_plan["morning"] = f"Last-minute shopping or revisit favorite spots in {destination}"
            day_plan["afternoon"] = f"Departure preparations and final sightseeing"
            day_plan["evening"] = f"Farewell dinner and departure"
        
        itinerary.append(day_plan)
    
    return itinerary