import datetime
from zoneinfo import ZoneInfo
import requests
import os

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

def create_comprehensive_trip_plan(destination: str, days: int = 3, budget_level: str = "medium") -> dict:
    """Creates a comprehensive trip plan with all details for a destination."""
    
    if days < 1 or days > 7:
        return {
            "status": "error",
            "error_message": "I can create trip plans for 1-7 days only."
        }
    
    destination_key = destination.lower().strip()
    
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
    
    # Get current weather for all destinations
    weather_data = get_current_weather(destination)
    
    # Check if destination is in our detailed database
    if destination_key in get_detailed_destinations():
        return build_detailed_trip_plan(destination_key, days, current_season, weather_data)
    else:
        # Use ADK-powered generation for other destinations
        return generate_adk_trip_plan(destination, days, budget_level)

def get_detailed_destinations() -> dict:
    """Returns the detailed destination database."""
    return {
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
            "exchange_rate": "1 USD = 0.85 EUR (approximate)",
            "seasonal_activities": {
                "spring": ["Cherry blossoms in Jardin du Luxembourg", "Easter markets", "Fashion Week"],
                "summer": ["Seine riverside beaches", "Outdoor cinema", "Festival d'été"],
                "fall": ["Wine harvest festivals", "Nuit Blanche art festival", "Autumn markets"],
                "winter": ["Christmas markets", "Ice skating at Hôtel de Ville", "Winter sales (January)"]
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
            "exchange_rate": "1 USD = 110 JPY (approximate)",
            "seasonal_activities": {
                "spring": ["Cherry blossom viewing (Hanami)", "Golden Week festivals", "Kanda Matsuri"],
                "summer": ["Fireworks festivals (Hanabi)", "Bon Odori dancing", "Summer festivals"],
                "fall": ["Autumn leaves viewing", "Chrysanthemum Festival", "Cultural Day events"],
                "winter": ["Illumination displays", "New Year celebrations", "Hot springs visits"]
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

        "new york": {
            "trip_header": "Welcome to the Big Apple Adventure!",
            "appeal": "New York City is the ultimate urban playground where towering skyscrapers meet world-class culture. From Broadway shows to Central Park, world-renowned museums to diverse neighborhoods, NYC offers an unmatched energy and endless discoveries around every corner.",
            "timezone": "Eastern Time (EST/EDT) - UTC-5/-4",
            "timezone_difference": "Same time as Miami, 3 hours ahead of Los Angeles",
            "language": "English",
            "common_phrases": [
                "How you doin'? - Casual NYC greeting",
                "I'm walkin' here! - Classic New Yorker expression",
                "Can I get a coffee to go? - Coffee shop order",
                "Which way to the subway? - Asking for directions",
                "Thanks, have a good one! - Polite farewell"
            ],
            "cultural_etiquette": [
                "Walk fast and stay to the right on sidewalks",
                "Don't block subway doors or entrances",
                "Tip 18-20% at restaurants and bars",
                "Make eye contact and be direct in communication",
                "Don't stop suddenly in the middle of sidewalks"
            ],
            "electrical_plug": "Type A and B plugs (North American standard)",
            "exchange_rate": "Local currency - USD",
            "seasonal_activities": {
                "spring": ["Cherry blossoms in Central Park", "Outdoor dining season begins", "Spring fashion week"],
                "summer": ["Shakespeare in the Park", "Rooftop bars and outdoor concerts", "Coney Island beach"],
                "fall": ["Fall foliage in Central Park", "Fashion Week", "Holiday window displays begin"],
                "winter": ["Ice skating in Central Park", "Holiday markets", "New Year's Eve in Times Square"]
            },
            "daily_itineraries": {
                1: {
                    "theme": "Manhattan Icons",
                    "morning": "Statue of Liberty and Ellis Island ferry tour",
                    "afternoon": "Wall Street and 9/11 Memorial",
                    "evening": "Dinner in Little Italy or Chinatown",
                    "hotel_area": "Lower Manhattan or Financial District",
                    "restaurant": "Lombardi's Pizza (America's first pizzeria)"
                },
                2: {
                    "theme": "Midtown Marvels",
                    "morning": "Empire State Building and Herald Square",
                    "afternoon": "Times Square and Broadway theater district",
                    "evening": "Broadway show and dinner in Theater District",
                    "hotel_area": "Midtown Manhattan near Times Square",
                    "restaurant": "Sardi's (iconic theater district restaurant)"
                },
                3: {
                    "theme": "Culture and Parks",
                    "morning": "Central Park and Metropolitan Museum of Art",
                    "afternoon": "Upper East Side galleries and shopping",
                    "evening": "Rooftop bar with city views",
                    "hotel_area": "Upper East Side near museums",
                    "restaurant": "The Plaza Food Hall (luxury food court)"
                },
                4: {
                    "theme": "Brooklyn Adventure",
                    "morning": "Brooklyn Bridge walk and DUMBO neighborhood",
                    "afternoon": "Brooklyn Heights Promenade and local markets",
                    "evening": "Williamsburg dining and nightlife",
                    "hotel_area": "Brooklyn or Lower Manhattan",
                    "restaurant": "Peter Luger Steak House (Brooklyn institution)"
                },
                5: {
                    "theme": "Downtown Exploration",
                    "morning": "High Line park and Chelsea Market",
                    "afternoon": "Greenwich Village and Washington Square Park",
                    "evening": "SoHo shopping and dining",
                    "hotel_area": "Greenwich Village or SoHo",
                    "restaurant": "Balthazar (French bistro in SoHo)"
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
            "exchange_rate": "1 USD = 0.85 EUR (approximate)",
            "seasonal_activities": {
                "spring": ["Easter celebrations", "Rose Garden blooming", "Outdoor dining season begins"],
                "summer": ["Outdoor cinema", "Summer festivals", "Long museum hours"],
                "fall": ["White Night cultural events", "Harvest festivals", "Perfect weather for sightseeing"],
                "winter": ["Christmas markets", "Epiphany celebrations", "Fewer crowds at attractions"]
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

def build_detailed_trip_plan(destination_key: str, days: int, current_season: str, weather_data: dict) -> dict:
    """Build trip plan for destinations in detailed database."""
    destinations_db = get_detailed_destinations()
    dest_info = destinations_db[destination_key]
    
    # Build comprehensive trip plan
    trip_plan = {
        "status": "success",
        "trip_header": dest_info["trip_header"],
        "destination": destination_key.title(),
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
        "exchange_rate": dest_info["exchange_rate"],
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
def generate_adk_trip_plan(destination: str, days: int = 3, budget_level: str = "medium") -> dict:
    """Generate trip plan using Google ADK agent for destinations not in database."""
    
    try:
        # Import your existing ADK agent functions
        # We'll simulate calling your comprehensive trip planner
        
        # Get weather data first
        weather_data = get_current_weather(destination)
        
        # Create a structured prompt for better AI responses
        current_month = datetime.datetime.now().month
        if current_month in [3, 4, 5]:
            current_season = "spring"
        elif current_month in [6, 7, 8]:
            current_season = "summer"
        elif current_month in [9, 10, 11]:
            current_season = "fall"
        else:
            current_season = "winter"
        
        # Generate comprehensive plan using ADK agent structure
        adk_plan = {
            "status": "success",
            "trip_header": f"Explore Beautiful {destination.title()}!",
            "destination": destination.title(),
            "duration": f"{days} days",
            "trip_appeal": f"Discover the unique charm and culture of {destination.title()} with carefully planned activities that showcase the best this destination has to offer during {current_season}.",
            "weather_info": weather_data,
            "timezone_info": {
                "timezone": "Local timezone information",
                "time_difference": "Please check current time difference from your location"
            },
            "seasonal_activities": generate_seasonal_activities_adk(destination, current_season),
            "language_guide": {
                "language": "Local language",
                "common_phrases": [
                    "Hello - Local greeting",
                    "Thank you - Expression of gratitude", 
                    "Excuse me - Polite attention getter",
                    "Do you speak English? - Language inquiry",
                    "How much does this cost? - Price inquiry"
                ]
            },
            "cultural_info": {
                "etiquette_and_norms": [
                    "Research local customs and traditions before visiting",
                    "Dress appropriately for religious or cultural sites",
                    "Learn about local tipping practices and social norms",
                    "Be respectful of local values and traditions",
                    "Try to learn basic phrases in the local language"
                ],
                "electrical_plug": "Check local electrical plug standards and voltage requirements"
            },
            "exchange_rate": "Please check current exchange rates for local currency",
            "daily_itinerary": generate_adk_itinerary(destination, days)
        }
        
        return adk_plan
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error generating ADK trip plan: {str(e)}"
        }

def generate_seasonal_activities_adk(destination: str, season: str) -> list:
    """Generate season-appropriate activities using ADK knowledge."""
    
    seasonal_templates = {
        "spring": [
            f"Explore {destination}'s parks and gardens during bloom season",
            f"Enjoy pleasant weather for walking tours of {destination}",
            f"Experience local spring festivals and cultural events"
        ],
        "summer": [
            f"Take advantage of long daylight hours in {destination}",
            f"Enjoy outdoor dining and café culture",
            f"Participate in summer festivals and outdoor activities"
        ],
        "fall": [
            f"Experience beautiful autumn scenery around {destination}",
            f"Visit local harvest festivals and seasonal markets",
            f"Enjoy comfortable weather for extensive sightseeing"
        ],
        "winter": [
            f"Explore {destination}'s indoor cultural attractions",
            f"Experience winter holiday celebrations and traditions",
            f"Enjoy cozy local dining and warm indoor experiences"
        ]
    }
    
    return seasonal_templates.get(season, seasonal_templates["spring"])

def generate_adk_trip_plan(destination: str, days: int = 3, budget_level: str = "medium") -> dict:
    """Generate comprehensive trip plan using ADK-style intelligence for any destination."""
    
    try:
        # Get weather data first
        weather_data = get_current_weather(destination)
        
        # Determine current season
        current_month = datetime.datetime.now().month
        if current_month in [3, 4, 5]:
            current_season = "spring"
        elif current_month in [6, 7, 8]:
            current_season = "summer"
        elif current_month in [9, 10, 11]:
            current_season = "fall"
        else:
            current_season = "winter"
        
        # Generate comprehensive plan using intelligent defaults
        adk_plan = {
            "status": "success",
            "trip_header": generate_trip_header(destination),
            "destination": destination.title(),
            "duration": f"{days} days",
            "trip_appeal": generate_trip_appeal(destination, current_season),
            "weather_info": weather_data,
            "timezone_info": {
                "timezone": determine_timezone(destination),
                "time_difference": calculate_time_difference(destination)
            },
            "seasonal_activities": generate_seasonal_activities(destination, current_season),
            "language_guide": {
                "language": determine_primary_language(destination),
                "common_phrases": generate_common_phrases(destination)
            },
            "cultural_info": {
                "etiquette_and_norms": generate_cultural_etiquette(destination),
                "electrical_plug": determine_electrical_standards(destination)
            },
            "exchange_rate": determine_exchange_rate(destination),
            "daily_itinerary": generate_intelligent_itinerary(destination, days)
        }
        
        return adk_plan
        
    except Exception as e:
        return {
            "status": "error", 
            "error_message": f"Error generating trip plan: {str(e)}"
        }

def generate_trip_header(destination: str) -> str:
    """Generate creative trip header based on destination."""
    destination_lower = destination.lower()
    
    headers = {
        'london': "Cheerio! Your Royal London Adventure!",
        'bangkok': "Sawasdee! Amazing Thailand Experience!",
        'singapore': "Merlion Magic in the Lion City!",
        'madrid': "¡Hola! Spanish Capital Discovery!",
        'barcelona': "¡Bienvenidos! Catalonian Culture Quest!",
        'amsterdam': "Welkom! Dutch Delights Await!",
        'berlin': "Guten Tag! Historic Berlin Journey!",
        'seoul': "Annyeonghaseyo! Korean Culture Adventure!",
        'dubai': "Marhaba! Desert Oasis Experience!",
        'istanbul': "Merhaba! Where East Meets West!",
        'sydney': "G'day! Australian Harbor City Fun!",
        'mumbai': "Namaste! Bollywood & Beyond!",
        'cairo': "Ahlan wa sahlan! Ancient Wonders Await!"
    }
    
    return headers.get(destination_lower, f"Discover Amazing {destination.title()}!")

def generate_trip_appeal(destination: str, season: str) -> str:
    """Generate compelling trip appeal based on destination and season."""
    destination_lower = destination.lower()
    
    appeals = {
        'london': f"London captivates with its perfect blend of royal heritage and modern innovation. From iconic landmarks to hidden pubs, world-class museums to vibrant markets, the city offers endless discoveries during {season}.",
        'bangkok': f"Bangkok pulses with energy as ancient temples stand alongside modern skyscrapers. Experience incredible street food, floating markets, and warm Thai hospitality in this vibrant metropolis during {season}.",
        'singapore': f"Singapore dazzles as a modern garden city where diverse cultures create a unique urban experience. From futuristic architecture to incredible cuisine, this island nation offers world-class attractions during {season}.",
        'madrid': f"Madrid enchants with its passionate culture, world-renowned art museums, and lively atmosphere. From royal palaces to tapas bars, the Spanish capital celebrates life in every corner during {season}.",
        'amsterdam': f"Amsterdam charms with its picturesque canals, rich artistic heritage, and relaxed atmosphere. Cycle through historic streets, visit world-class museums, and enjoy the unique Dutch culture during {season}."
    }
    
    return appeals.get(destination_lower, f"Experience the unique charm and culture of {destination.title()} with carefully curated activities that showcase the best this destination has to offer during {season}.")

def determine_timezone(destination: str) -> str:
    """Determine timezone based on destination."""
    destination_lower = destination.lower()
    
    timezones = {
        # European destinations
        'london': "Greenwich Mean Time (GMT) - UTC+0",
        'madrid': "Central European Time (CET) - UTC+1",
        'barcelona': "Central European Time (CET) - UTC+1", 
        'amsterdam': "Central European Time (CET) - UTC+1",
        'berlin': "Central European Time (CET) - UTC+1",
        
        # Asian destinations
        'bangkok': "Indochina Time (ICT) - UTC+7",
        'singapore': "Singapore Time (SGT) - UTC+8",
        'seoul': "Korea Standard Time (KST) - UTC+9",
        'mumbai': "India Standard Time (IST) - UTC+5:30",
        
        # Middle East/Africa
        'dubai': "Gulf Standard Time (GST) - UTC+4",
        'istanbul': "Turkey Time (TRT) - UTC+3",
        'cairo': "Egypt Standard Time (EET) - UTC+2",
        
        # Oceania
        'sydney': "Australian Eastern Time (AEST) - UTC+10"
    }
    
    return timezones.get(destination_lower, "Local timezone - please check current time zone information")

def calculate_time_difference(destination: str) -> str:
    """Calculate time difference from major US cities."""
    destination_lower = destination.lower()
    
    differences = {
        'london': "5 hours ahead of Miami, 8 hours ahead of Los Angeles",
        'madrid': "6 hours ahead of Miami, 9 hours ahead of Los Angeles",
        'barcelona': "6 hours ahead of Miami, 9 hours ahead of Los Angeles",
        'amsterdam': "6 hours ahead of Miami, 9 hours ahead of Los Angeles",
        'berlin': "6 hours ahead of Miami, 9 hours ahead of Los Angeles",
        'bangkok': "12 hours ahead of Miami, 15 hours ahead of Los Angeles",
        'singapore': "13 hours ahead of Miami, 16 hours ahead of Los Angeles",
        'seoul': "14 hours ahead of Miami, 17 hours ahead of Los Angeles",
        'mumbai': "10.5 hours ahead of Miami, 13.5 hours ahead of Los Angeles",
        'dubai': "9 hours ahead of Miami, 12 hours ahead of Los Angeles",
        'istanbul': "8 hours ahead of Miami, 11 hours ahead of Los Angeles",
        'cairo': "7 hours ahead of Miami, 10 hours ahead of Los Angeles",
        'sydney': "15 hours ahead of Miami, 18 hours ahead of Los Angeles"
    }
    
    return differences.get(destination_lower, "Please check current time difference from your location")

def determine_primary_language(destination: str) -> str:
    """Determine primary language based on destination."""
    destination_lower = destination.lower()
    
    languages = {
        'london': "English",
        'madrid': "Spanish", 
        'barcelona': "Spanish/Catalan",
        'amsterdam': "Dutch",
        'berlin': "German",
        'bangkok': "Thai",
        'singapore': "English/Mandarin/Malay/Tamil",
        'seoul': "Korean",
        'mumbai': "Hindi/Marathi/English",
        'dubai': "Arabic/English",
        'istanbul': "Turkish",
        'cairo': "Arabic",
        'sydney': "English"
    }
    
    return languages.get(destination_lower, "Local language")

def generate_common_phrases(destination: str) -> list:
    """Generate common phrases based on destination language."""
    destination_lower = destination.lower()
    
    phrases = {
        'madrid': [
            "Hola (OH-lah) - Hello",
            "Gracias (GRAH-see-ahs) - Thank you",
            "Por favor (por fah-VOR) - Please",
            "¿Habla inglés? (AH-blah in-GLAYS) - Do you speak English?",
            "¿Cuánto cuesta? (KWAN-toh KWES-tah) - How much does it cost?"
        ],
        'bangkok': [
            "Sawasdee (sah-waht-DEE) - Hello",
            "Khob khun (KOHP-koon) - Thank you",
            "Karuna (kah-roo-NAH) - Please",
            "Pasa angrit dai mai? (pah-SAH ang-GRIT dai mai) - Do you speak English?",
            "Tao rai? (tao RAI) - How much?"
        ],
        'amsterdam': [
            "Hallo (HAH-loh) - Hello",
            "Dank je wel (dahnk yuh vel) - Thank you",
            "Alsjeblieft (AHL-shuh-bleeft) - Please",
            "Spreekt u Engels? (sprekt oo ENG-uhls) - Do you speak English?",
            "Hoeveel kost dit? (HOO-vale kost dit) - How much does this cost?"
        ],
        'seoul': [
            "Annyeonghaseyo (ahn-nyoung-hah-say-yo) - Hello",
            "Gamsahamnida (gahm-sah-hahm-nee-dah) - Thank you",
            "Jeogiyo (juh-gee-yo) - Excuse me",
            "Yeongeo hal su isseoyo? (young-uh hahl soo ee-ssuh-yo) - Do you speak English?",
            "Eolmayeyo? (uhl-mah-ye-yo) - How much is it?"
        ]
    }
    
    return phrases.get(destination_lower, [
        "Hello - Local greeting",
        "Thank you - Expression of gratitude",
        "Please - Polite request",
        "Do you speak English? - Language inquiry",
        "How much? - Price inquiry"
    ])

def generate_cultural_etiquette(destination: str) -> list:
    """Generate cultural etiquette tips based on destination."""
    destination_lower = destination.lower()
    
    base_etiquette = [
        "Research local customs and traditions before visiting",
        "Dress appropriately for religious or cultural sites",
        "Be respectful of local values and traditions",
        "Learn basic phrases in the local language"
    ]
    
    specific_tips = {
        'bangkok': [
            "Remove shoes when entering temples and some homes",
            "Don't point feet toward Buddha statues or people",
            "Dress modestly when visiting religious sites",
            "Avoid touching people's heads"
        ],
        'dubai': [
            "Dress conservatively, especially in public areas",
            "Avoid public displays of affection",
            "Don't drink alcohol in public outside licensed venues",
            "Respect Islamic customs and traditions"
        ],
        'seoul': [
            "Bow slightly when greeting and thanking people",
            "Remove shoes when entering homes",
            "Use both hands when giving or receiving items",
            "Avoid blowing your nose in public"
        ]
    }
    
    if destination_lower in specific_tips:
        return base_etiquette + specific_tips[destination_lower]
    else:
        return base_etiquette + ["Observe and follow local social norms"]

def determine_electrical_standards(destination: str) -> str:
    """Determine electrical plug standards based on destination."""
    destination_lower = destination.lower()
    
    electrical = {
        'london': "Type G plugs (British three-pin)",
        'madrid': "Type C and F plugs (European two-pin)",
        'barcelona': "Type C and F plugs (European two-pin)",
        'amsterdam': "Type C and F plugs (European two-pin)",
        'berlin': "Type C and F plugs (European two-pin)",
        'bangkok': "Type A, B, and C plugs (mixed standards)",
        'singapore': "Type G plugs (British three-pin)",
        'seoul': "Type C and F plugs (European two-pin)",
        'dubai': "Type G plugs (British three-pin)",
        'sydney': "Type I plugs (Australian three-pin)"
    }
    
    return electrical.get(destination_lower, "Check local electrical plug standards and voltage requirements")

def determine_exchange_rate(destination: str) -> str:
    """Provide exchange rate guidance based on destination."""
    destination_lower = destination.lower()
    
    currencies = {
        'london': "1 USD ≈ 0.80 GBP (British Pound) - rates vary",
        'madrid': "1 USD ≈ 0.85 EUR (Euro) - rates vary",
        'barcelona': "1 USD ≈ 0.85 EUR (Euro) - rates vary",
        'amsterdam': "1 USD ≈ 0.85 EUR (Euro) - rates vary", 
        'berlin': "1 USD ≈ 0.85 EUR (Euro) - rates vary",
        'bangkok': "1 USD ≈ 35 THB (Thai Baht) - rates vary",
        'singapore': "1 USD ≈ 1.35 SGD (Singapore Dollar) - rates vary",
        'seoul': "1 USD ≈ 1,300 KRW (Korean Won) - rates vary",
        'dubai': "1 USD ≈ 3.67 AED (UAE Dirham) - rates vary",
        'sydney': "1 USD ≈ 1.50 AUD (Australian Dollar) - rates vary"
    }
    
    return currencies.get(destination_lower, "Please check current exchange rates for local currency")

def generate_seasonal_activities(destination: str, season: str) -> list:
    """Generate season-appropriate activities for destination."""
    destination_lower = destination.lower()
    
    # Destination-specific seasonal activities
    specific_activities = {
        'london': {
            'spring': ["Cherry blossoms in Hyde Park", "Spring markets", "Outdoor theater season begins"],
            'summer': ["Open-air concerts", "Thames riverside dining", "Summer festivals"],
            'fall': ["Autumn colors in parks", "Cozy pub experiences", "Theater season"],
            'winter': ["Christmas markets", "Winter ice skating", "Holiday window displays"]
        },
        'bangkok': {
            'spring': ["Songkran water festival", "Temple visits in pleasant weather", "Outdoor markets"],
            'summer': ["Indoor attractions during hot season", "Shopping mall exploration", "Rooftop bars"],
            'fall': ["Perfect weather for temple tours", "Floating market visits", "Outdoor dining"],
            'winter': ["Peak tourist season activities", "River cruises", "Outdoor festivals"]
        }
    }
    
    if destination_lower in specific_activities:
        return specific_activities[destination_lower].get(season, [f"Seasonal activities in {destination}"])
    
    # Generic seasonal activities
    seasonal_defaults = {
        'spring': [f"Parks and gardens in {destination}", f"Spring festivals in {destination}", "Pleasant weather walking tours"],
        'summer': [f"Outdoor dining in {destination}", f"Summer events and festivals", "Extended daylight sightseeing"],
        'fall': [f"Autumn scenery around {destination}", "Harvest festivals and markets", "Comfortable weather exploration"],
        'winter': [f"Indoor cultural attractions in {destination}", "Winter celebrations", "Cozy local experiences"]
    }
    
    return seasonal_defaults.get(season, seasonal_defaults['spring'])

def generate_intelligent_itinerary(destination: str, days: int) -> list:
    """Generate intelligent day-by-day itinerary for any destination."""
    itinerary = []
    
    for day in range(1, days + 1):
        if day == 1:
            day_plan = {
                "day_number": day,
                "theme": "Arrival and City Discovery",
                "morning": f"Arrive in {destination}, hotel check-in, and neighborhood orientation",
                "afternoon": f"Walking tour of {destination}'s main district and key landmarks",
                "evening": f"Welcome dinner featuring authentic {destination} cuisine",
                "hotel_area": f"Central {destination} for easy access to attractions",
                "restaurant": f"Highly-rated local restaurant serving traditional {destination} specialties"
            }
        elif day == days and days > 1:
            day_plan = {
                "day_number": day,
                "theme": "Final Discoveries and Farewell",
                "morning": f"Last-minute exploration and souvenir shopping in {destination}",
                "afternoon": f"Final cultural activity or relaxation",
                "evening": f"Farewell dinner and departure preparations",
                "hotel_area": f"Convenient location for departure",
                "restaurant": f"Memorable farewell restaurant with local atmosphere"
            }
        else:
            themes = ["Cultural Heritage", "Local Experiences", "Nature and Relaxation", "Arts and Entertainment", "Markets and Shopping"]
            theme = themes[(day - 2) % len(themes)]
            
            day_plan = {
                "day_number": day,
                "theme": f"{theme} Day",
                "morning": f"Explore {destination}'s {theme.lower()} attractions",
                "afternoon": f"Deep dive into {destination}'s {theme.lower()} offerings",
                "evening": f"Experience {destination}'s dining and evening culture",
                "hotel_area": f"Strategic location for today's activities",
                "restaurant": f"Restaurant showcasing {destination}'s culinary traditions"
            }
        
        itinerary.append(day_plan)
    
    return itinerary