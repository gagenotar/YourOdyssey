import datetime
from zoneinfo import ZoneInfo
import requests
import os

from google.adk import Agent


def get_current_weather(city: str) -> dict:
    """Gets current weather information for a city using WeatherAPI.com."""
    api_key = os.getenv('WEATHERAPI_KEY')
    if not api_key:
        return {
            "status": "error",
            "error_message": "Weather API key not configured."
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


def smart_destination_info(destination: str, search_online: bool = False) -> dict:
    """Provides comprehensive destination information using database and AI knowledge.

    Args:
        destination (str): The name of the destination city or country.
        search_online (bool): If True, indicates user wants current/online information.

    Returns:
        dict: status and comprehensive destination information.
    """

    # Core destination database
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
        "new york": {
            "status": "success",
            "source": "database",
            "info": {
                "best_time_to_visit": "April-June, September-November",
                "top_attractions": ["Statue of Liberty", "Central Park", "Times Square", "Brooklyn Bridge"],
                "budget_estimate": "$250-500 per day",
                "climate": "Humid continental climate",
                "local_currency": "US Dollar (USD)",
                "language": "English",
                "travel_tips": "Use the subway system, tip 18-20% at restaurants, book Broadway shows in advance"
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

    # Check if it's in our database
    if destination_key in destinations:
        result = destinations[destination_key]
        if search_online:
            result[
                "search_suggestion"] = f"For the most current information about {destination}, including recent events, updated prices, or COVID restrictions, I recommend using a web search or checking official tourism websites."
        return result

    # For destinations not in database, provide AI-generated information
    expanded_destinations = {
        "london": {
            "best_time_to_visit": "May-September",
            "top_attractions": ["Big Ben", "Tower of London", "British Museum", "London Eye"],
            "budget_estimate": "$200-350 per day",
            "climate": "Temperate oceanic climate",
            "local_currency": "British Pound (GBP)",
            "language": "English",
            "travel_tips": "Get an Oyster Card for public transport, always carry an umbrella, book theater shows in advance"
        },
        "barcelona": {
            "best_time_to_visit": "April-June, September-October",
            "top_attractions": ["Sagrada Familia", "Park Güell", "Las Ramblas", "Gothic Quarter"],
            "budget_estimate": "$130-250 per day",
            "climate": "Mediterranean climate",
            "local_currency": "Euro (EUR)",
            "language": "Spanish/Catalan",
            "travel_tips": "Learn basic Spanish, siesta hours are 2-5pm, watch for pickpockets in tourist areas"
        },
        "bali": {
            "best_time_to_visit": "April-October (dry season)",
            "top_attractions": ["Ubud Rice Terraces", "Tanah Lot Temple", "Mount Batur", "Seminyak Beach"],
            "budget_estimate": "$50-150 per day",
            "climate": "Tropical climate",
            "local_currency": "Indonesian Rupiah (IDR)",
            "language": "Indonesian/Balinese",
            "travel_tips": "Rent a scooter for transportation, respect temple dress codes, bargain at markets"
        },
        "bangkok": {
            "best_time_to_visit": "November-March (cool season)",
            "top_attractions": ["Grand Palace", "Wat Pho", "Chatuchak Market", "Khao San Road"],
            "budget_estimate": "$40-120 per day",
            "climate": "Tropical savanna climate",
            "local_currency": "Thai Baht (THB)",
            "language": "Thai",
            "travel_tips": "Use BTS/MRT for transport, try street food, remove shoes in temples"
        }
    }

    if destination_key in expanded_destinations:
        return {
            "status": "success",
            "source": "ai_knowledge",
            "info": expanded_destinations[destination_key],
            "note": f"This information is based on general knowledge. For current conditions, events, or restrictions in {destination}, consider checking recent sources online."
        }

    # For completely unknown destinations, provide helpful guidance
    return {
        "status": "partial",
        "source": "general_guidance",
        "message": f"I don't have specific detailed information for '{destination}' in my database.",
        "general_advice": {
            "research_suggestions": [
                f"Check official tourism websites for {destination}",
                "Look up current weather and seasonal information",
                "Research visa requirements for your nationality",
                "Check travel advisories and safety information",
                "Look for recent travel blogs and reviews"
            ],
            "planning_tips": [
                "Book accommodations in advance for popular destinations",
                "Learn basic phrases in the local language",
                "Research local customs and etiquette",
                "Check if any special events coincide with your visit",
                "Consider travel insurance"
            ]
        },
        "search_suggestion": f"For detailed, current information about {destination}, I recommend using web search tools or consulting recent travel guides."
    }


def enhanced_search_info(query: str, search_type: str = "general") -> dict:
    """Simulates search functionality by providing guidance on what to search for.

    Args:
        query (str): The search query about travel/destinations.
        search_type (str): Type of search - "current_events", "prices", "weather", "general".

    Returns:
        dict: Search guidance and suggestions.
    """

    search_suggestions = {
        "current_events": {
            "suggested_queries": [
                f"current events {query} 2024",
                f"travel restrictions {query}",
                f"festivals events {query} 2024",
                f"COVID requirements {query}"
            ],
            "sources_to_check": ["Official tourism boards", "Government travel sites", "Recent news articles",
                                 "Travel forums"]
        },
        "prices": {
            "suggested_queries": [
                f"hotel prices {query} 2024",
                f"flight costs to {query}",
                f"restaurant prices {query}",
                f"attraction tickets {query}"
            ],
            "sources_to_check": ["Booking.com", "Expedia", "TripAdvisor", "Local tourism sites"]
        },
        "weather": {
            "suggested_queries": [
                f"current weather {query}",
                f"weather forecast {query}",
                f"best time to visit {query}",
                f"seasonal weather {query}"
            ],
            "sources_to_check": ["Weather.com", "AccuWeather", "Local weather services"]
        },
        "general": {
            "suggested_queries": [
                f"travel guide {query}",
                f"things to do {query}",
                f"travel tips {query}",
                f"best attractions {query}"
            ],
            "sources_to_check": ["Lonely Planet", "TripAdvisor", "Travel blogs", "Official tourism sites"]
        }
    }

    return {
        "status": "search_guidance",
        "query": query,
        "search_type": search_type,
        "guidance": search_suggestions.get(search_type, search_suggestions["general"]),
        "note": "Since I can't perform live web searches in this configuration, here are the best search strategies and sources for current information."
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
            3: ["Versailles day trip", "Palace and gardens tour", "Return to Paris for dinner"],
            4: ["Montmartre and Sacré-Cœur", "Artist studios visit", "Moulin Rouge show"],
            5: ["Champs-Élysées shopping", "Arc de Triomphe", "Café culture experience"],
            6: ["Marais district exploration", "Jewish quarter", "Vintage shopping"],
            7: ["Day trip to Loire Valley", "Castle visits", "Wine tasting"]
        },
        "tokyo": {
            1: ["Sensoji Temple", "Asakusa district", "Traditional dinner"],
            2: ["Tokyo Skytree", "Sumida River area", "Robot Restaurant show"],
            3: ["Meiji Shrine", "Harajuku fashion district", "Shibuya crossing"],
            4: ["Tsukiji Fish Market", "Sushi breakfast", "Imperial Palace gardens"],
            5: ["Day trip to Mount Fuji", "Hakone hot springs", "Lake views"],
            6: ["Akihabara electronics", "Anime culture", "Gaming centers"],
            7: ["Traditional ryokan stay", "Tea ceremony", "Zen meditation"]
        },
        "london": {
            1: ["Tower of London", "Tower Bridge", "Borough Market lunch"],
            2: ["British Museum", "Covent Garden", "West End show"],
            3: ["Westminster Abbey", "Big Ben", "Thames river cruise"],
            4: ["Tate Modern", "Shakespeare's Globe", "South Bank walk"],
            5: ["Day trip to Windsor Castle", "Royal gardens", "Return to London"],
            6: ["Camden Market", "Regent's Park", "London Zoo"],
            7: ["Greenwich Observatory", "Maritime Museum", "Greenwich Park"]
        },
        "barcelona": {
            1: ["Sagrada Familia", "Park Güell", "Gothic Quarter evening"],
            2: ["Las Ramblas", "Boqueria Market", "Picasso Museum"],
            3: ["Casa Batlló", "Casa Milà", "Passeig de Gràcia shopping"],
            4: ["Barceloneta Beach", "Seafood lunch", "Olympic Port"],
            5: ["Montjuïc Hill", "Magic Fountain", "Poble Espanyol"],
            6: ["Day trip to Montserrat", "Monastery visit", "Mountain hiking"],
            7: ["El Raval district", "MACBA museum", "Tapas tour"]
        }
    }

    destination_key = destination.lower().strip()

    if destination_key in itineraries:
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

    # For destinations not in our itinerary database, provide framework
    return {
        "status": "framework",
        "destination": destination.title(),
        "duration": f"{days} days",
        "message": f"I don't have a pre-built itinerary for {destination}, but I can provide a general framework:",
        "framework": {
            "Day 1": ["Arrival and city orientation", "Visit main landmark", "Local dinner"],
            "Day 2": ["Major museum or cultural site", "Historic district exploration", "Traditional cuisine"],
            "Day 3": ["Day trip or nature activity", "Local markets", "Evening entertainment"],
            "Days 4-7": ["Mix of remaining attractions", "Local experiences", "Shopping and relaxation"]
        },
        "suggestion": f"For a detailed {days}-day itinerary for {destination}, I recommend searching for recent travel guides or consulting local tourism websites."
    }


def get_travel_budget(destination: str, days: int, budget_level: str = "medium") -> dict:
    """Estimates travel budget for a vacation."""
    if days < 1:
        return {
            "status": "error",
            "error_message": "Duration must be at least 1 day."
        }

    budget_multipliers = {"low": 0.7, "medium": 1.0, "high": 1.5}

    if budget_level.lower() not in budget_multipliers:
        return {
            "status": "error",
            "error_message": "Budget level must be 'low', 'medium', or 'high'."
        }

    base_costs = {
        "paris": {"daily": 225, "flight": 800, "accommodation": 120},
        "tokyo": {"daily": 300, "flight": 1200, "accommodation": 150},
        "new york": {"daily": 375, "flight": 600, "accommodation": 200},
        "rome": {"daily": 185, "flight": 700, "accommodation": 100},
        "london": {"daily": 250, "flight": 750, "accommodation": 140},
        "barcelona": {"daily": 180, "flight": 650, "accommodation": 90},
        "bali": {"daily": 75, "flight": 1100, "accommodation": 40},
        "bangkok": {"daily": 65, "flight": 900, "accommodation": 30}
    }

    destination_key = destination.lower().strip()

    if destination_key in base_costs:
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
            "daily_average": f"${daily_cost}",
            "note": "Prices are estimates and may vary based on current market conditions."
        }

    return {
        "status": "estimate",
        "destination": destination.title(),
        "message": f"I don't have specific budget data for {destination}.",
        "general_guidance": {
            "research_tips": [
                "Check hotel booking sites for accommodation prices",
                "Look up average meal costs on travel forums",
                "Research local transportation options and costs",
                "Find attraction prices on official websites"
            ],
            "budget_factors": [
                "Season and peak times affect prices significantly",
                "Accommodation location impacts daily transport costs",
                "Eating local vs. tourist restaurants makes a big difference",
                "Free attractions and walking tours can reduce costs"
            ]
        }
    }

def create_comprehensive_trip_plan(destination: str, days: int = 3, budget_level: str = "medium") -> dict:
    """Creates a comprehensive trip plan with all details for a destination.

    Args:
        destination (str): The destination city or country.
        days (int): Number of days for the trip (1-7).
        budget_level (str): Budget level - "low", "medium", or "high".

    Returns:
        dict: Complete trip planning information.
    """

    if days < 1 or days > 7:
        return {
            "status": "error",
            "error_message": "I can create trip plans for 1-7 days only."
        }

    destination_key = destination.lower().strip()

    # Comprehensive destination database
    destinations_db = {
        "paris": {
            "trip_header": "Bonjour, City of Light Adventure!",
            "appeal": "Paris enchants with its timeless elegance, world-class museums, charming cafés, and romantic atmosphere. From the iconic Eiffel Tower to hidden neighborhood bistros, every corner tells a story of art, culture, and joie de vivre.",
            "timezone": "Central European Time (CET) - UTC+1",
            "timezone_difference": "6 hours ahead of Miami, 9 hours ahead of Los Angeles",
            "language": "French",
            "common_phrases": [
                "Bonjour (bon-ZHOOR) - Hello/Good morning",
                "Merci (mer-SEE) - Thank you",
                "Excusez-moi (ex-kew-zay-MWAH) - Excuse me",
                "Parlez-vous anglais? (par-lay voo ahn-GLAY) - Do you speak English?",
                "L'addition, s'il vous plaît (lah-dee-see-OHN seel voo PLAY) - The check, please"
            ],
            "cultural_etiquette": [
                "Always greet shopkeepers when entering stores",
                "Keep your voice down in restaurants and public transport",
                "Dress more formally - avoid shorts and flip-flops in the city",
                "Learn basic French phrases - locals appreciate the effort",
                "Tipping 10% is standard, service charge often included"
            ],
            "electrical_plug": "Type C and E plugs (European two-pin)",
            "seasonal_activities": {
                "spring": ["Cherry blossoms in Jardin du Luxembourg", "Easter markets", "Fashion Week"],
                "summer": ["Seine riverside beaches", "Outdoor cinema", "Festival d'été"],
                "fall": ["Wine harvest festivals", "Nuit Blanche art festival", "Autumn markets"],
                "winter": ["Christmas markets", "Ice skating at Hôtel de Ville", "Winter sales (January)"]
            },
            "hotels": {
                "luxury": ["Le Bristol Paris", "The Ritz Paris", "Hotel Plaza Athénée"],
                "mid_range": ["Hotel des Grands Boulevards", "Hotel Malte Opera", "Hotel National Des Arts et Métiers"],
                "budget": ["Hotel Jeanne d'Arc", "MIJE hostels", "Generator Paris"]
            },
            "restaurants": {
                "fine_dining": ["L'Ambroisie", "Guy Savoy", "Alain Ducasse"],
                "casual": ["L'As du Fallafel", "Breizh Café", "Pink Mamma"],
                "local_favorites": ["Bistrot Paul Bert", "Le Comptoir du Relais", "Café de Flore"]
            },
            "daily_itineraries": {
                1: {
                    "theme": "Classic Paris Icons",
                    "morning": "Eiffel Tower visit and Trocadéro photos",
                    "afternoon": "Seine River cruise and Île de la Cité",
                    "evening": "Dinner in Latin Quarter",
                    "hotel_area": "7th arrondissement (near Eiffel Tower)",
                    "restaurant": "Le Comptoir du 7ème (traditional French bistro)"
                },
                2: {
                    "theme": "Art and Culture Day",
                    "morning": "Louvre Museum (pre-booked tickets)",
                    "afternoon": "Tuileries Garden and Place Vendôme",
                    "evening": "Montmartre and Sacré-Cœur sunset",
                    "hotel_area": "1st arrondissement (Louvre area)",
                    "restaurant": "L'Ami Jean (modern bistro cuisine)"
                },
                3: {
                    "theme": "Royal Splendor",
                    "morning": "Versailles Palace day trip",
                    "afternoon": "Palace gardens and Marie Antoinette's estate",
                    "evening": "Return to Paris, dinner at local brasserie",
                    "hotel_area": "Stay near train station for easy Versailles access",
                    "restaurant": "Brasserie Lipp (historic Parisian brasserie)"
                }
            }
        },

        "tokyo": {
            "trip_header": "Konnichiwa, Land of the Rising Sun Experience!",
            "appeal": "Tokyo blends ancient traditions with cutting-edge innovation, offering everything from serene temples to bustling neon districts. Experience incredible cuisine, unique culture, and the famous Japanese hospitality in this fascinating metropolis.",
            "timezone": "Japan Standard Time (JST) - UTC+9",
            "timezone_difference": "14 hours ahead of Miami, 17 hours ahead of Los Angeles",
            "language": "Japanese",
            "common_phrases": [
                "Konnichiwa (kon-nee-chee-wah) - Hello",
                "Arigatou gozaimasu (ah-ree-gah-toh go-zah-ee-mahs) - Thank you very much",
                "Sumimasen (soo-mee-mah-sen) - Excuse me/Sorry",
                "Eigo ga wakarimasu ka? (ay-go gah wah-kah-ree-mahs kah) - Do you understand English?",
                "Oishii desu (oh-ee-shee dess) - It's delicious"
            ],
            "cultural_etiquette": [
                "Bow slightly when greeting people",
                "Remove shoes when entering homes, temples, some restaurants",
                "Don't tip - it's not customary and can be offensive",
                "Eat quietly and don't stick chopsticks upright in rice",
                "Be quiet on public transportation"
            ],
            "electrical_plug": "Type A and B plugs (North American style)",
            "seasonal_activities": {
                "spring": ["Cherry blossom viewing (Hanami)", "Golden Week festivals", "Kanda Matsuri"],
                "summer": ["Fireworks festivals (Hanabi)", "Bon Odori dancing", "Summer festivals"],
                "fall": ["Autumn leaves viewing", "Chrysanthemum Festival", "Cultural Day events"],
                "winter": ["Illumination displays", "New Year celebrations", "Hot springs visits"]
            },
            "hotels": {
                "luxury": ["The Ritz-Carlton Tokyo", "Aman Tokyo", "Imperial Hotel"],
                "mid_range": ["Hotel Gracery Shinjuku", "Shibuya Excel Hotel", "Richmond Hotel"],
                "budget": ["Capsule hotels", "Hostel world locations", "Business hotels"]
            },
            "restaurants": {
                "fine_dining": ["Sukiyabashi Jiro", "Narisawa", "Kozasa"],
                "casual": ["Ichiran Ramen", "Genki Sushi", "Ippudo"],
                "local_favorites": ["Tsukiji Market stalls", "Yakitori alleys", "Department store food courts"]
            },
            "daily_itineraries": {
                1: {
                    "theme": "Traditional Tokyo",
                    "morning": "Sensoji Temple and Asakusa district",
                    "afternoon": "Imperial Palace East Gardens",
                    "evening": "Traditional dinner and cultural show",
                    "hotel_area": "Asakusa (traditional area)",
                    "restaurant": "Daikokuya (traditional tempura, established 1887)"
                },
                2: {
                    "theme": "Modern Tokyo",
                    "morning": "Tokyo Skytree and Sumida River area",
                    "afternoon": "Harajuku and youth culture",
                    "evening": "Shibuya crossing and Robot Restaurant",
                    "hotel_area": "Shibuya (modern entertainment district)",
                    "restaurant": "Gonpachi (famous 'Kill Bill' restaurant)"
                },
                3: {
                    "theme": "Nature and Tradition",
                    "morning": "Day trip to Mount Fuji area",
                    "afternoon": "Hakone hot springs",
                    "evening": "Return to Tokyo, quiet dinner",
                    "hotel_area": "Near transportation hub for easy day trip access",
                    "restaurant": "Kozasa (Michelin-starred kaiseki)"
                }
            }
        },

        "rome": {
            "trip_header": "Ciao, Eternal City Adventure!",
            "appeal": "Rome is a living museum where ancient history meets vibrant modern life. Walk through 2,000 years of civilization, from the Colosseum to Vatican treasures, while enjoying incredible food, warm hospitality, and la dolce vita lifestyle.",
            "timezone": "Central European Time (CET) - UTC+1",
            "timezone_difference": "6 hours ahead of Miami, 9 hours ahead of Los Angeles",
            "language": "Italian",
            "common_phrases": [
                "Ciao (chow) - Hello/Goodbye (informal)",
                "Grazie (GRAH-tsee-eh) - Thank you",
                "Scusi (SKOO-zee) - Excuse me",
                "Parla inglese? (PAR-lah in-GLAY-zeh) - Do you speak English?",
                "Dov'è il bagno? (doh-VEH eel BAHN-yoh) - Where is the bathroom?"
            ],
            "cultural_etiquette": [
                "Dress modestly when visiting churches (cover shoulders/knees)",
                "Lunch is typically 1-3pm, dinner after 8pm",
                "Stand at the bar for cheaper coffee",
                "Don't ask for cappuccino after 11am",
                "Tipping 10% is appreciated but not mandatory"
            ],
            "electrical_plug": "Type C, F, and L plugs (European style)",
            "seasonal_activities": {
                "spring": ["Easter celebrations", "Rose Garden blooming", "Outdoor dining season begins"],
                "summer": ["Outdoor cinema", "Summer festivals", "Long museum hours"],
                "fall": ["White Night cultural events", "Harvest festivals", "Perfect weather for sightseeing"],
                "winter": ["Christmas markets", "Epiphany celebrations", "Fewer crowds at attractions"]
            },
            "hotels": {
                "luxury": ["Hotel de Russie", "The First Roma", "Villa Spalletti Trivelli"],
                "mid_range": ["Hotel Artemide", "Hotel Sonya", "The RomeHello"],
                "budget": ["The Beehive", "Alessandro Palace", "Generator Rome"]
            },
            "restaurants": {
                "fine_dining": ["La Pergola", "Il Pagliaccio", "Metamorfosi"],
                "casual": ["Da Enzo", "Trattoria Monti", "Armando al Pantheon"],
                "local_favorites": ["Checchino dal 1887", "Flavio al Velavevodetto", "Piperno"]
            },
            "daily_itineraries": {
                1: {
                    "theme": "Ancient Rome",
                    "morning": "Colosseum and Roman Forum tour",
                    "afternoon": "Palatine Hill exploration",
                    "evening": "Traditional Roman dinner in Trastevere",
                    "hotel_area": "Near Colosseum or historic center",
                    "restaurant": "Checchino dal 1887 (traditional Roman cuisine)"
                },
                2: {
                    "theme": "Vatican and Spiritual Rome",
                    "morning": "Vatican Museums and Sistine Chapel",
                    "afternoon": "St. Peter's Basilica and climb the dome",
                    "evening": "Aperitivo and dinner near Vatican",
                    "hotel_area": "Vatican area or city center",
                    "restaurant": "Da Enzo al 29 (authentic local trattoria)"
                },
                3: {
                    "theme": "Baroque Beauty",
                    "morning": "Trevi Fountain and Spanish Steps",
                    "afternoon": "Pantheon and Piazza Navona",
                    "evening": "Villa Borghese gardens and gallery",
                    "hotel_area": "Spanish Steps or Pantheon area",
                    "restaurant": "Armando al Pantheon (family-run since 1961)"
                }
            }
        }
    }

    # Get current season for activities
    current_month = datetime.datetime.now().month
    if current_month in [3, 4, 5]:
        current_season = "spring"
    elif current_month in [6, 7, 8]:
        current_season = "summer"
    elif current_month in [9, 10, 11]:
        current_season = "fall"
    else:
        current_season = "winter"

    if destination_key in destinations_db:
        dest_info = destinations_db[destination_key]

        # Get current weather
        weather_data = get_current_weather(destination)

        # Get exchange rate (simplified - you could integrate a real API)
        exchange_rates = {
            "paris": "1 USD = 0.85 EUR (approximate)",
            "tokyo": "1 USD = 110 JPY (approximate)",
            "rome": "1 USD = 0.85 EUR (approximate)"
        }

        # Build comprehensive trip plan
        trip_plan = {
            "status": "success",
            "trip_header": dest_info["trip_header"],
            "destination": destination.title(),
            "duration": f"{days} days",
            "trip_appeal": dest_info["appeal"],
            "weather_info": weather_data,
            "timezone_info": {
                "timezone": dest_info["timezone"],
                "time_difference": dest_info["timezone_difference"]
            },
            "seasonal_activities": dest_info["seasonal_activities"][current_season],
            "language_guide": {
                "language": dest_info["language"],
                "common_phrases": dest_info["common_phrases"]
            },
            "cultural_info": {
                "etiquette_and_norms": dest_info["cultural_etiquette"],
                "electrical_plug": dest_info["electrical_plug"]
            },
            "exchange_rate": exchange_rates.get(destination_key, "Please check current exchange rates"),
            "accommodation_options": dest_info["hotels"],
            "dining_recommendations": dest_info["restaurants"],
            "daily_itinerary": []
        }

        # Generate daily itinerary
        for day in range(1, days + 1):
            if day <= len(dest_info["daily_itineraries"]):
                day_plan = dest_info["daily_itineraries"][day].copy()
                day_plan["day_number"] = day
                trip_plan["daily_itinerary"].append(day_plan)
            else:
                # Generate flexible days for longer trips
                trip_plan["daily_itinerary"].append({
                    "day_number": day,
                    "theme": "Free Exploration Day",
                    "morning": "Revisit favorite locations or explore new neighborhoods",
                    "afternoon": "Shopping or museum visits",
                    "evening": "Local dining experience",
                    "hotel_area": "Same accommodation area",
                    "restaurant": "Explore local recommendations"
                })

        return trip_plan

    else:
        # For destinations not in detailed database
        return {
            "status": "basic_plan",
            "trip_header": f"Adventure Awaits in {destination.title()}!",
            "destination": destination.title(),
            "message": f"I don't have comprehensive data for {destination} yet, but I can help you plan!",
            "suggestions": [
                "Research local customs and etiquette",
                "Check visa requirements for your nationality",
                "Look up current weather and seasonal activities",
                "Find recommended hotels and restaurants",
                "Learn basic phrases in the local language",
                "Check electrical plug types and voltage",
                "Research current exchange rates"
            ],
            "weather_info": get_current_weather(destination)
        }

root_agent = Agent(
    name="master_vacation_planner",
    model="gemini-2.0-flash",
    description=(
        "Comprehensive vacation planning agent with destination information, itineraries, "
        "budgets, weather data, and search guidance for current information."
    ),
    instruction=(
        "Make sure you start the conversation.\n"
        "You are an expert vacation planning agent with multiple capabilities:\n"
        "1. Provide detailed destination information from your database and AI knowledge\n"
        "2. Create day-by-day itineraries for popular destinations\n"
        "3. Calculate travel budgets with cost breakdowns\n"
        "4. Get current weather information via API\n"
        "5. Guide users on how to search for current information when needed\n\n"
        "When users ask about destinations not in your database, provide general guidance "
        "and suggest specific search strategies. Always be enthusiastic about travel and "
        "provide practical, actionable advice."
    ),
    tools=[smart_destination_info, create_itinerary, get_travel_budget, get_current_weather, enhanced_search_info],
)
