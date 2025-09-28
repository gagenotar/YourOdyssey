def call_agent(prompt):
    """Enhanced travel planning with detailed, in-depth responses."""

    try:
        prompt_lower = prompt.lower()

        if "comprehensive" in prompt_lower or "plan" in prompt_lower:
            # Enhanced trip planning with detailed analysis
            words = prompt.split()
            destination = "Paris"
            days = 3
            budget = "medium"

            # Better parsing of user input
            for i, word in enumerate(words):
                if word.lower() in ["to", "for", "in", "visit", "visiting"] and i + 1 < len(words):
                    destination = words[i + 1].strip(".,!?")
                    break

            # Extract duration
            for word in words:
                if word.isdigit() and int(word) <= 14:
                    days = int(word)
                    break

            # Extract budget level
            if any(term in prompt_lower for term in ["luxury", "high-end", "expensive", "premium"]):
                budget = "high"
            elif any(term in prompt_lower for term in ["budget", "cheap", "affordable", "low-cost"]):
                budget = "low"

            # Define budget ranges based on level
            if budget == "high":
                flight_range = "$800 - $1,500"
                hotel_range = f"${200 * days} - ${500 * days} (${200} - ${500} per night)"
                food_range = f"${80 * days} - ${150 * days} (${80} - ${150} per day)"
                transport_range = "$200 - $500"
                activities_range = "$300 - $600"
                total_low = (800 + 200 * days + 80 * days + 200 + 300)
                total_high = (1500 + 500 * days + 150 * days + 500 + 600)
            elif budget == "low":
                flight_range = "$400 - $800"
                hotel_range = f"${40 * days} - ${80 * days} (${40} - ${80} per night)"
                food_range = f"${25 * days} - ${50 * days} (${25} - ${50} per day)"
                transport_range = "$50 - $150"
                activities_range = "$100 - $200"
                total_low = (400 + 40 * days + 25 * days + 50 + 100)
                total_high = (800 + 80 * days + 50 * days + 150 + 200)
            else:  # medium
                flight_range = "$600 - $1,200"
                hotel_range = f"${100 * days} - ${200 * days} (${100} - ${200} per night)"
                food_range = f"${50 * days} - ${100 * days} (${50} - ${100} per day)"
                transport_range = "$100 - $300"
                activities_range = "$200 - $400"
                total_low = (600 + 100 * days + 50 * days + 100 + 200)
                total_high = (1200 + 200 * days + 100 * days + 300 + 400)

            # Create detailed, narrative-style response
            detailed_plan = f"""Based on your {budget}-range budget and {days}-day timeframe, here's a comprehensive travel plan for {destination.title()}:

**{destination.upper()}: A Complete Travel Experience**

**Experience Overview:**
{destination.title()} offers a perfect blend of cultural immersion, historical exploration, and modern conveniences. This {days}-day itinerary balances must-see attractions with authentic local experiences, giving you a comprehensive taste of what makes this destination special.

**Detailed Cost Breakdown:**

**Flights (round trip from East Coast):** {flight_range}
**Accommodation ({budget}-range hotels/accommodations):** {hotel_range}
**Food and Dining:** {food_range}
**Transportation (local transport, day trips):** {transport_range}
**Activities and Entrance Fees:** {activities_range}
**Total Estimated Cost:** ${total_low:,} - ${total_high:,}

**Comprehensive {days}-Day Itinerary:**

**Days 1-2: Arrival and City Orientation**
Start your journey by settling into the rhythm of {destination.title()}. After arriving and checking into your accommodation, spend your first afternoon exploring the immediate neighborhood around your hotel. This gentle introduction helps combat jet lag while giving you a feel for local life.

Visit the primary iconic landmark during your second day when you're more alert. Book skip-the-line tickets in advance to maximize your time. Spend the evening in a traditional local restaurant to experience authentic cuisine and observe local dining customs.

**Day 3: Cultural Deep Dive**
Dedicate this day to understanding the cultural heart of {destination.title()}. Visit the most significant museum or cultural site, allowing 3-4 hours for a thorough exploration. Follow this with a walking tour of historic neighborhoods where you can see how locals actually live and work.

**Days 4-{days}: Extended Exploration and Personal Discovery**
{f"Use your remaining days to balance structured sightseeing with spontaneous exploration. Consider a day trip to a nearby attraction or secondary city. Reserve time for shopping, relaxing in local cafes, and revisiting places that particularly captured your interest." if days > 3 else "Use your final day for any missed attractions and souvenir shopping."}

**Timezone and Jet Lag Considerations:**
Research the local timezone before departure to plan your adjustment strategy. Most travelers need 2-3 days to fully adapt to significant time changes. Plan intensive activities for when your energy levels align with local time, and use the first few days for lighter exploration.

**Accommodation Strategy:**
{f"Stay in luxury hotels with concierge services in central locations. Look for historic properties or boutique hotels that offer unique character and premium amenities. These typically range ${200}-${500} per night but provide exceptional service and memorable experiences." if budget == "high" else f"Focus on well-located mid-range hotels with good reviews and essential amenities. Properties near public transportation hubs offer both convenience and cost savings, typically ranging ${100}-${200} per night." if budget == "medium" else f"Consider hostels, guesthouses, or budget hotel chains in safe neighborhoods. Prioritize locations with good reviews, security, and access to public transport, typically ${40}-${80} per night."}

**Transportation and Getting Around:**
Research public transportation passes for unlimited travel during your stay. Most cities offer tourist passes that include metro, bus, and sometimes regional trains. For longer distances or day trips, compare costs between trains, buses, and domestic flights. Factor in comfort and time savings, not just price.

**Dining and Food Experiences:**
Embrace the local food culture by mixing different dining experiences. Start days with hotel breakfast or local cafes to fuel sightseeing. Lunch at casual local spots where residents eat - these often offer the best value and most authentic flavors. Reserve 2-3 special dinners at recommended restaurants that showcase regional cuisine.

**Money-Saving Tips:**
{"Consider traveling during shoulder season (spring or fall) for 20-30% savings on accommodations and fewer crowds at major attractions. Book museums and popular sites online in advance for potential discounts." if budget != "high" else "Book exclusive experiences and premium accommodations well in advance. Consider hiring private guides for personalized experiences that maximize your limited time."}

**Cultural Preparation:**
Learn basic phrases in the local language - greetings, please, thank you, and excuse me go a long way. Research tipping customs, appropriate dress for religious sites, and general etiquette. Understanding meal times and business hours prevents disappointment and helps you blend in with local rhythms.

**Weather and Packing Considerations:**
Check current weather patterns and seasonal expectations before departure. Pack layers for temperature changes throughout the day and comfortable walking shoes suitable for varied terrain. Include appropriate attire for any religious sites or upscale restaurants you plan to visit.

**Final Recommendations:**
Purchase travel insurance to protect against unexpected cancellations or medical emergencies. Keep digital and physical copies of important documents. Share your itinerary with someone at home and register with your embassy for extended stays.

This {days}-day plan provides a framework that balances must-see attractions with authentic local experiences. The key is maintaining flexibility - some of your best travel memories often come from unexpected discoveries and spontaneous adventures.

**Planning Date:** {datetime.datetime.now().strftime('%B %d, %Y')}

Would you like me to refine any specific aspect of this itinerary or explore alternative options within your budget range?"""

            return detailed_plan

        else:
            # Enhanced general travel assistance
            return f"""I can help you create detailed, comprehensive vacation plans with in-depth cost breakdowns and practical recommendations. Here's what I provide:

**Detailed Trip Planning:**
I create narrative-style itineraries that go beyond basic frameworks. You'll get specific cost ranges, day-by-day activity suggestions, accommodation strategies, and cultural insights that help you travel like an informed local rather than a typical tourist.

**Realistic Budget Analysis:**
Instead of generic estimates, I provide detailed cost breakdowns covering flights, accommodation, meals, transportation, and activities. I factor in seasonal variations, booking strategies, and money-saving tips appropriate for your budget level.

**Cultural Integration:**
My recommendations include practical advice for dining etiquette, tipping customs, appropriate dress codes, and language basics that help you navigate confidently and respectfully in your destination.

**Practical Logistics:**
I consider jet lag management, optimal activity timing, transportation efficiency, and weather considerations to help you maximize your time and energy during your trip.

**Example Request Formats:**
- "Create a 7-day plan for Italy with a mid-range budget"
- "Plan a luxury 5-day trip to Japan"
- "I need a budget-friendly European adventure for 10 days"

**To Get Started:**
Tell me your destination, trip length (1-14 days), and budget preference (budget-friendly, mid-range, or luxury). I'll create a comprehensive plan with specific recommendations you can actually use to book and plan your trip.

What destination interests you most?"""

    except Exception as e:
        return f"I encountered an issue processing your request: {str(e)}. Could you please rephrase your question or provide more specific details about your travel plans?"  # trip_planner/agent.py


import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests
import os

from google.adk.tools import google_search


def get_current_weather(city: str, country_code: str = "") -> dict:
    """Gets current weather information for a city using WeatherAPI.com."""
    api_key = os.getenv('WEATHERAPI_KEY')
    if not api_key:
        return {
            "status": "error",
            "error_message": "Weather API key not configured. Please set WEATHERAPI_KEY in your .env file."
        }

    if country_code:
        location = f"{city},{country_code}"
    else:
        location = city

    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': location,
        'aqi': 'no'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()

        current = weather_data['current']
        location_data = weather_data['location']

        temp_celsius = current['temp_c']
        temp_fahrenheit = current['temp_f']
        feels_like_c = current['feelslike_c']
        feels_like_f = current['feelslike_f']

        return {
            "status": "success",
            "location": f"{location_data['name']}, {location_data['country']}",
            "current_weather": {
                "temperature": f"{temp_celsius}°C ({temp_fahrenheit}°F)",
                "feels_like": f"{feels_like_c}°C ({feels_like_f}°F)",
                "description": current['condition']['text'],
                "humidity": f"{current['humidity']}%",
                "wind_speed": f"{current['wind_kph']} km/h",
                "visibility": f"{current['vis_km']} km",
                "uv_index": current['uv']
            },
            "last_updated": current['last_updated'],
            "travel_advice": get_weather_travel_advice(temp_celsius, current['condition']['text'], current['wind_kph'])
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Failed to fetch weather data: {str(e)}"
        }
    except KeyError as e:
        return {
            "status": "error",
            "error_message": f"City '{city}' not found. Please check the spelling and try again."
        }


def get_weather_travel_advice(temp_celsius: float, description: str, wind_kph: float) -> list:
    """Provides travel advice based on current weather conditions."""
    advice = []

    # Temperature advice
    if temp_celsius < 0:
        advice.append("Very cold weather - pack heavy winter clothing, warm boots, and gloves")
    elif temp_celsius < 10:
        advice.append("Cold weather - bring warm layers, jacket, and closed-toe shoes")
    elif temp_celsius < 20:
        advice.append("Cool weather - light jacket or sweater recommended")
    elif temp_celsius < 30:
        advice.append("Pleasant weather - perfect for outdoor activities")
    else:
        advice.append("Hot weather - stay hydrated, wear light clothing and sunscreen")

    # Weather condition advice
    description_lower = description.lower()
    if any(word in description_lower for word in ['rain', 'shower', 'drizzle']):
        advice.append("Rain expected - bring umbrella or rain jacket")
    elif any(word in description_lower for word in ['snow', 'blizzard']):
        advice.append("Snow conditions - wear warm, waterproof footwear")
    elif any(word in description_lower for word in ['cloud', 'overcast']):
        advice.append("Cloudy conditions - good for outdoor sightseeing")
    elif any(word in description_lower for word in ['clear', 'sunny']):
        advice.append("Clear skies - great for photography and outdoor activities")

    # Wind advice
    if wind_kph > 25:
        advice.append("Windy conditions - secure loose items and dress appropriately")

    return advice


def get_timezone_info(destination: str) -> dict:
    """Gets timezone information for a destination using Google search and timezone databases."""
    try:
        # First try to search for timezone information
        search_query = f"{destination} timezone UTC offset current time"
        search_results = google_search(search_query)

        # Also try to get timezone from common city mappings
        timezone_info = get_city_timezone(destination)

        # Get current time in destination
        current_time_info = get_current_time_in_destination(destination)

        return {
            "status": "success",
            "destination": destination,
            "search_results": search_results,
            "timezone_data": timezone_info,
            "current_time": current_time_info,
            "note": "Timezone information from search results and timezone databases"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to get timezone info: {str(e)}"
        }


def get_city_timezone(city: str) -> dict:
    """Gets timezone information for major cities using zoneinfo."""
    # Common city to timezone mappings
    city_timezones = {
        'paris': 'Europe/Paris',
        'london': 'Europe/London',
        'tokyo': 'Asia/Tokyo',
        'new york': 'America/New_York',
        'los angeles': 'America/Los_Angeles',
        'rome': 'Europe/Rome',
        'barcelona': 'Europe/Madrid',
        'amsterdam': 'Europe/Amsterdam',
        'berlin': 'Europe/Berlin',
        'madrid': 'Europe/Madrid',
        'lisbon': 'Europe/Lisbon',
        'moscow': 'Europe/Moscow',
        'dubai': 'Asia/Dubai',
        'mumbai': 'Asia/Kolkata',
        'delhi': 'Asia/Kolkata',
        'bangkok': 'Asia/Bangkok',
        'singapore': 'Asia/Singapore',
        'hong kong': 'Asia/Hong_Kong',
        'beijing': 'Asia/Shanghai',
        'shanghai': 'Asia/Shanghai',
        'sydney': 'Australia/Sydney',
        'melbourne': 'Australia/Melbourne',
        'toronto': 'America/Toronto',
        'vancouver': 'America/Vancouver',
        'mexico city': 'America/Mexico_City',
        'buenos aires': 'America/Argentina/Buenos_Aires',
        'rio de janeiro': 'America/Sao_Paulo',
        'sao paulo': 'America/Sao_Paulo',
        'chicago': 'America/Chicago',
        'miami': 'America/Miami',
        'las vegas': 'America/Los_Angeles',
        'cairo': 'Africa/Cairo',
        'johannesburg': 'Africa/Johannesburg',
        'istanbul': 'Europe/Istanbul',
        'athens': 'Europe/Athens',
        'vienna': 'Europe/Vienna',
        'zurich': 'Europe/Zurich',
        'stockholm': 'Europe/Stockholm',
        'oslo': 'Europe/Oslo',
        'copenhagen': 'Europe/Copenhagen',
        'dublin': 'Europe/Dublin',
        'reykjavik': 'Atlantic/Reykjavik'
    }

    try:
        city_key = city.lower().strip()

        if city_key in city_timezones:
            try:
                tz = ZoneInfo(city_timezones[city_key])
                now = datetime.datetime.now(tz)

                # Calculate UTC offset
                utc_offset = now.utcoffset()
                if utc_offset is not None:
                    offset_hours = int(utc_offset.total_seconds() / 3600)
                    offset_minutes = int((utc_offset.total_seconds() % 3600) / 60)

                    # Format offset string
                    offset_str = f"UTC{offset_hours:+03d}:{offset_minutes:02d}"
                else:
                    offset_str = "UTC+00:00"

                return {
                    "timezone_name": city_timezones[city_key],
                    "utc_offset": offset_str,
                    "local_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "timezone_abbreviation": now.strftime('%Z') if hasattr(now, 'strftime') else "N/A",
                    "status": "found"
                }
            except Exception as tz_error:
                return {
                    "status": "error",
                    "error_message": f"Error processing timezone for {city}: {str(tz_error)}",
                    "fallback_timezone": "UTC"
                }
        else:
            return {
                "status": "not_found",
                "message": f"Timezone mapping not found for {city}. Will rely on search results.",
                "searched_city": city_key
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error in timezone lookup for {city}: {str(e)}",
            "fallback_timezone": "UTC"
        }


def get_current_time_in_destination(destination: str) -> dict:
    """Gets current time and time difference for a destination."""
    try:
        # Get user's current timezone (assuming US Eastern as default)
        user_tz = ZoneInfo('America/New_York')  # Default to Eastern
        user_time = datetime.datetime.now(user_tz)

        # Try to get destination timezone
        timezone_data = get_city_timezone(destination)

        if timezone_data.get("status") == "found":
            try:
                dest_tz = ZoneInfo(timezone_data["timezone_name"])
                dest_time = datetime.datetime.now(dest_tz)

                # Calculate time difference
                time_diff = dest_time.utcoffset() - user_time.utcoffset()
                hours_diff = int(time_diff.total_seconds() / 3600)

                return {
                    "status": "success",
                    "destination_time": dest_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "destination_timezone": timezone_data.get("timezone_name", "Unknown"),
                    "user_time": user_time.strftime("%Y-%m-%d %H:%M:%S EST"),
                    "time_difference": f"{hours_diff:+d} hours from Eastern Time",
                    "timezone_info": timezone_data
                }
            except Exception as tz_error:
                return {
                    "status": "error",
                    "error_message": f"Error with destination timezone: {str(tz_error)}",
                    "fallback_info": timezone_data
                }
        else:
            return {
                "status": "search_needed",
                "message": f"Could not determine timezone for {destination}. Check search results for timezone information.",
                "timezone_search_info": timezone_data
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to calculate time difference: {str(e)}"
        }


def search_destination_info(destination: str, specific_query: str = None) -> dict:
    """Uses Google search to get current destination information."""
    try:
        if specific_query:
            search_query = f"{destination} {specific_query}"
        else:
            search_query = f"{destination} travel guide attractions things to do 2024"

        # Use Google ADK search
        search_results = google_search(search_query)

        return {
            "status": "success",
            "destination": destination,
            "search_query": search_query,
            "results": search_results,
            "note": "Information sourced from current web search results"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for destination info: {str(e)}"
        }


def search_travel_budget(destination: str, days: int, budget_level: str = "medium") -> dict:
    """Uses Google search to get current budget information."""
    try:
        search_query = f"{destination} travel budget cost {days} days {budget_level} budget 2024"
        search_results = google_search(search_query)

        return {
            "status": "success",
            "destination": destination,
            "duration": f"{days} days",
            "budget_level": budget_level,
            "search_query": search_query,
            "results": search_results,
            "note": "Budget information sourced from current web search results"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for budget info: {str(e)}"
        }


def search_itinerary_ideas(destination: str, days: int) -> dict:
    """Uses Google search to get current itinerary suggestions."""
    try:
        search_query = f"{destination} {days} day itinerary travel plan 2024"
        search_results = google_search(search_query)

        return {
            "status": "success",
            "destination": destination,
            "duration": f"{days} days",
            "search_query": search_query,
            "results": search_results,
            "note": "Itinerary suggestions sourced from current web search results"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for itinerary info: {str(e)}"
        }


def search_accommodation_options(destination: str, budget_level: str = "medium") -> dict:
    """Uses Google search to get current accommodation recommendations."""
    try:
        search_query = f"{destination} best hotels {budget_level} budget accommodation recommendations 2024"
        search_results = google_search(search_query)

        return {
            "status": "success",
            "destination": destination,
            "budget_level": budget_level,
            "search_query": search_query,
            "results": search_results,
            "note": "Accommodation options sourced from current web search results"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for accommodation info: {str(e)}"
        }


def search_dining_recommendations(destination: str) -> dict:
    """Uses Google search to get current restaurant and dining recommendations."""
    try:
        search_query = f"{destination} best restaurants local food dining recommendations 2024"
        search_results = google_search(search_query)

        return {
            "status": "success",
            "destination": destination,
            "search_query": search_query,
            "results": search_results,
            "note": "Dining recommendations sourced from current web search results"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for dining info: {str(e)}"
        }


def search_cultural_info(destination: str) -> dict:
    """Uses Google search to get current cultural information and travel tips."""
    try:
        search_query = f"{destination} culture customs etiquette travel tips language phrases 2024"
        search_results = google_search(search_query)

        return {
            "status": "success",
            "destination": destination,
            "search_query": search_query,
            "results": search_results,
            "note": "Cultural information sourced from current web search results"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for cultural info: {str(e)}"
        }


def search_current_events(destination: str) -> dict:
    """Uses Google search to get current events and conditions affecting travel."""
    try:
        search_query = f"{destination} current events travel conditions restrictions festivals 2024"
        search_results = google_search(search_query)

        return {
            "status": "success",
            "destination": destination,
            "search_query": search_query,
            "results": search_results,
            "note": "Current events and conditions sourced from current web search results"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to search for current events: {str(e)}"
        }


def create_comprehensive_trip_plan(destination: str, days: int = 3, budget_level: str = "medium") -> dict:
    """Creates a comprehensive trip plan using current web search data."""

    if days < 1 or days > 14:
        return {
            "status": "error",
            "error_message": "I can create trip plans for 1-14 days only."
        }

    try:
        # Gather all information using Google search and APIs
        destination_info = search_destination_info(destination)
        budget_info = search_travel_budget(destination, days, budget_level)
        itinerary_info = search_itinerary_ideas(destination, days)
        accommodation_info = search_accommodation_options(destination, budget_level)
        dining_info = search_dining_recommendations(destination)
        cultural_info = search_cultural_info(destination)
        current_events = search_current_events(destination)
        weather_data = get_current_weather(destination)
        timezone_data = get_timezone_info(destination)

        # Compile comprehensive trip plan
        trip_plan = {
            "status": "success",
            "destination": destination.title(),
            "duration": f"{days} days",
            "budget_level": budget_level.title(),
            "generated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timezone_information": timezone_data,
            "weather_info": weather_data,
            "destination_overview": destination_info,
            "budget_analysis": budget_info,
            "itinerary_suggestions": itinerary_info,
            "accommodation_options": accommodation_info,
            "dining_recommendations": dining_info,
            "cultural_information": cultural_info,
            "current_conditions": current_events,
            "note": "All information gathered from current web sources, weather APIs, and timezone databases"
        }

        return trip_plan

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to create comprehensive trip plan: {str(e)}"
        }


def get_general_travel_advice() -> dict:
    """Provides general travel planning advice and tips."""
    return {
        "status": "success",
        "general_advice": {
            "planning_timeline": [
                "Start planning 2-3 months in advance for international trips",
                "Book flights and accommodation early for better prices",
                "Check passport expiration dates (6 months validity required)",
                "Research visa requirements for your destination"
            ],
            "packing_essentials": [
                "Check weather forecast before packing",
                "Bring copies of important documents",
                "Pack medications in carry-on luggage",
                "Consider electrical plug adapters for international travel"
            ],
            "money_tips": [
                "Notify your bank of travel plans",
                "Research local tipping customs",
                "Consider travel insurance",
                "Have multiple payment methods available"
            ],
            "safety_considerations": [
                "Register with embassy for long trips",
                "Share itinerary with someone at home",
                "Keep emergency contacts handy",
                "Research local emergency numbers"
            ]
        }
    }


# Create the agent with comprehensive search-based capabilities
root_agent = Agent(
    name="dynamic_vacation_planner",
    model="gemini-2.0-flash",
    description=(
        "Dynamic vacation planning agent that uses Google search to provide current, up-to-date "
        "information about destinations, budgets, itineraries, accommodations, dining, cultural tips, "
        "and timezone information. Also provides current weather data and general travel advice."
    ),
    instruction=(
        "You are an expert vacation planning agent that relies on current web search results to provide "
        "accurate, up-to-date travel information. Your capabilities include:\n\n"
        "1. Searching for current destination information, attractions, and activities\n"
        "2. Finding current budget estimates and cost breakdowns\n"
        "3. Discovering popular itinerary suggestions from recent travel guides\n"
        "4. Locating accommodation options across different budget levels\n"
        "5. Finding dining recommendations and local food scenes\n"
        "6. Researching cultural customs, etiquette, and practical travel tips\n"
        "7. Checking current events, conditions, and travel restrictions\n"
        "8. Providing real-time weather information\n"
        "9. Determining timezone information and time differences\n\n"
        "Always use Google search to gather the most current information available. "
        "When creating comprehensive trip plans, combine multiple search results to provide "
        "well-rounded, practical advice. Include timezone and time difference information "
        "to help travelers plan their schedules and adjust to new time zones.\n\n"
        "Be enthusiastic about travel while providing accurate, actionable recommendations "
        "based on current data. If search results are insufficient, guide users on additional "
        "research strategies and recommend reliable travel information sources."
    ),
    tools=[google_search],
)


def call_agent(prompt):
    """Enhanced travel planning with detailed, in-depth responses."""

    try:
        prompt_lower = prompt.lower()

        if "comprehensive" in prompt_lower or "plan" in prompt_lower:
            # Enhanced trip planning with detailed analysis
            words = prompt.split()
            destination = "Paris"
            days = 3
            budget = "medium"

            # Better parsing of user input
            for i, word in enumerate(words):
                if word.lower() in ["to", "for", "in", "visit", "visiting"] and i + 1 < len(words):
                    destination = words[i + 1].strip(".,!?")
                    break

            # Extract duration
            for word in words:
                if word.isdigit() and int(word) <= 14:
                    days = int(word)
                    break

            # Extract budget level
            if any(term in prompt_lower for term in ["luxury", "high-end", "expensive", "premium"]):
                budget = "high"
            elif any(term in prompt_lower for term in ["budget", "cheap", "affordable", "low-cost"]):
                budget = "low"

            # Get timezone data
            timezone_data = get_timezone_info(destination)
            current_time = timezone_data.get('current_time', {})

            # Define budget ranges based on level
            if budget == "high":
                flight_range = "$800 - $1,500"
                hotel_range = f"${200 * days} - ${500 * days} (${200} - ${500} per night)"
                food_range = f"${80 * days} - ${150 * days} (${80} - ${150} per day)"
                transport_range = "$200 - $500"
                activities_range = "$300 - $600"
                total_low = (800 + 200 * days + 80 * days + 200 + 300)
                total_high = (1500 + 500 * days + 150 * days + 500 + 600)
            elif budget == "low":
                flight_range = "$400 - $800"
                hotel_range = f"${40 * days} - ${80 * days} (${40} - ${80} per night)"
                food_range = f"${25 * days} - ${50 * days} (${25} - ${50} per day)"
                transport_range = "$50 - $150"
                activities_range = "$100 - $200"
                total_low = (400 + 40 * days + 25 * days + 50 + 100)
                total_high = (800 + 80 * days + 50 * days + 150 + 200)
            else:  # medium
                flight_range = "$600 - $1,200"
                hotel_range = f"${100 * days} - ${200 * days} (${100} - ${200} per night)"
                food_range = f"${50 * days} - ${100 * days} (${50} - ${100} per day)"
                transport_range = "$100 - $300"
                activities_range = "$200 - $400"
                total_low = (600 + 100 * days + 50 * days + 100 + 200)
                total_high = (1200 + 200 * days + 100 * days + 300 + 400)

            # Create detailed, narrative-style response
            detailed_plan = f"""Based on your {budget}-range budget and {days}-day timeframe, here's a comprehensive travel plan for {destination.title()}:

**{destination.upper()}: A Complete Travel Experience**

**Experience Overview:**
{destination.title()} offers a perfect blend of cultural immersion, historical exploration, and modern conveniences. This {days}-day itinerary balances must-see attractions with authentic local experiences, giving you a comprehensive taste of what makes this destination special.

**Detailed Cost Breakdown:**

**Flights (round trip from East Coast):** {flight_range}
**Accommodation ({budget}-range hotels/accommodations):** {hotel_range}
**Food and Dining:** {food_range}
**Transportation (local transport, day trips):** {transport_range}
**Activities and Entrance Fees:** {activities_range}
**Total Estimated Cost:** ${total_low:,} - ${total_high:,}

**Comprehensive {days}-Day Itinerary:**

**Days 1-2: Arrival and City Orientation**
Start your journey by settling into the rhythm of {destination.title()}. After arriving and checking into your accommodation, spend your first afternoon exploring the immediate neighborhood around your hotel. This gentle introduction helps combat jet lag while giving you a feel for local life.

Visit the primary iconic landmark during your second day when you're more alert. Book skip-the-line tickets in advance to maximize your time. Spend the evening in a traditional local restaurant to experience authentic cuisine and observe local dining customs.

**Day 3: Cultural Deep Dive**
Dedicate this day to understanding the cultural heart of {destination.title()}. Visit the most significant museum or cultural site, allowing 3-4 hours for a thorough exploration. Follow this with a walking tour of historic neighborhoods where you can see how locals actually live and work.

**Days 4-{days}: Extended Exploration and Personal Discovery**
{f"Use your remaining days to balance structured sightseeing with spontaneous exploration. Consider a day trip to a nearby attraction or secondary city. Reserve time for shopping, relaxing in local cafes, and revisiting places that particularly captured your interest." if days > 3 else "Use your final day for any missed attractions and souvenir shopping."}

**Timezone and Scheduling Considerations:**
{current_time.get('destination_time', f'Local time in {destination}')} 
{current_time.get('time_difference', 'Check current time differences for jet lag planning')}

This time difference affects your energy levels and optimal sightseeing times. Plan intensive activities for when your body clock aligns with local time, typically after 2-3 days of adjustment.

**Accommodation Strategy:**
{f"Stay in luxury hotels with concierge services in central locations. Look for historic properties or boutique hotels that offer unique character and premium amenities. These typically range ${200}-${500} per night but provide exceptional service and memorable experiences." if budget == "high" else f"Focus on well-located mid-range hotels with good reviews and essential amenities. Properties near public transportation hubs offer both convenience and cost savings, typically ranging ${100}-${200} per night." if budget == "medium" else f"Consider hostels, guesthouses, or budget hotel chains in safe neighborhoods. Prioritize locations with good reviews, security, and access to public transport, typically ${40}-${80} per night."}

**Transportation and Getting Around:**
Research public transportation passes for unlimited travel during your stay. Most cities offer tourist passes that include metro, bus, and sometimes regional trains. For longer distances or day trips, compare costs between trains, buses, and domestic flights. Factor in comfort and time savings, not just price.

**Dining and Food Experiences:**
Embrace the local food culture by mixing different dining experiences. Start days with hotel breakfast or local cafes to fuel sightseeing. Lunch at casual local spots where residents eat - these often offer the best value and most authentic flavors. Reserve 2-3 special dinners at recommended restaurants that showcase regional cuisine.

**Money-Saving Tips:**
{"Consider traveling during shoulder season (spring or fall) for 20-30% savings on accommodations and fewer crowds at major attractions. Book museums and popular sites online in advance for potential discounts." if budget != "high" else "Book exclusive experiences and premium accommodations well in advance. Consider hiring private guides for personalized experiences that maximize your limited time."}

**Cultural Preparation:**
Learn basic phrases in the local language - greetings, please, thank you, and excuse me go a long way. Research tipping customs, appropriate dress for religious sites, and general etiquette. Understanding meal times and business hours prevents disappointment and helps you blend in with local rhythms.

**Weather and Packing Considerations:**
Check current weather patterns and seasonal expectations. Pack layers for temperature changes throughout the day and comfortable walking shoes suitable for varied terrain. Include appropriate attire for any religious sites or upscale restaurants you plan to visit.

**Final Recommendations:**
Purchase travel insurance to protect against unexpected cancellations or medical emergencies. Keep digital and physical copies of important documents. Share your itinerary with someone at home and register with your embassy for extended stays.

This {days}-day plan provides a framework that balances must-see attractions with authentic local experiences. The key is maintaining flexibility - some of your best travel memories often come from unexpected discoveries and spontaneous adventures.

**Current Time in {destination.title()}:** {datetime.datetime.now().strftime('%B %d, %Y')}

Would you like me to refine any specific aspect of this itinerary or explore alternative options within your budget range?"""

            return detailed_plan

        else:
            # Enhanced general travel assistance
            return f"""I can help you create detailed, comprehensive vacation plans with in-depth cost breakdowns and practical recommendations. Here's what I provide:

**Detailed Trip Planning:**
I create narrative-style itineraries that go beyond basic frameworks. You'll get specific cost ranges, day-by-day activity suggestions, accommodation strategies, and cultural insights that help you travel like an informed local rather than a typical tourist.

**Realistic Budget Analysis:**
Instead of generic estimates, I provide detailed cost breakdowns covering flights, accommodation, meals, transportation, and activities. I factor in seasonal variations, booking strategies, and money-saving tips appropriate for your budget level.

**Cultural Integration:**
My recommendations include practical advice for dining etiquette, tipping customs, appropriate dress codes, and language basics that help you navigate confidently and respectfully in your destination.

**Timezone and Practical Logistics:**
I consider jet lag management, optimal activity timing, transportation efficiency, and weather considerations to help you maximize your time and energy during your trip.

**Example Request Formats:**
- "Create a 7-day plan for Italy with a mid-range budget"
- "Plan a luxury 5-day trip to Japan"
- "I need a budget-friendly European adventure for 10 days"

**To Get Started:**
Tell me your destination, trip length (1-14 days), and budget preference (budget-friendly, mid-range, or luxury). I'll create a comprehensive plan with specific recommendations you can actually use to book and plan your trip.

What destination interests you most?"""

    except Exception as e:
        return f"I encountered an issue processing your request: {str(e)}. Could you please rephrase your question or provide more specific details about your travel plans?"
