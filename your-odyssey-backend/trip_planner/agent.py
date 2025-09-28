import os
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv
# Note: Flask imports and app instance were moved to `flask_app.py` so this
# module can be used as a library by the Flask server and other code without
# side effects on import.

# Load environment variables
load_dotenv()

# Note: Flask app and CORS are provided by `flask_app.py` so this module
# exposes only the agent implementation and the `travel_agent` instance.

# Configuration - Only need Gemini API key to start
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


@dataclass
class TransportationInfo:
    departure_location: str
    arrival_location: str
    transport_type: str
    duration: str
    estimated_cost: str
    booking_info: Optional[str] = None
    tips: Optional[str] = None


@dataclass
class Activity:
    name: str
    description: str
    location: str
    address: str
    duration: str
    estimated_cost: str
    category: str
    rating: Optional[float] = None
    opening_hours: Optional[str] = None
    tips: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None


@dataclass
class DayPlan:
    day: int
    date: str
    theme: str
    activities: List[Activity]
    total_estimated_cost: str
    transportation_notes: Optional[str] = None


@dataclass
class TravelItinerary:
    destination: str
    duration: int
    outbound_transport: TransportationInfo
    return_transport: TransportationInfo
    days: List[DayPlan]
    destination_info: Dict
    practical_info: Dict


class SimplifiedTravelAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_itinerary(self, destination: str, duration: int, preferences: str, budget: str,
                           departure_location: str = "") -> TravelItinerary:
        """Generate itinerary using Gemini directly"""

        prompt = f"""
        Create a detailed {duration}-day vacation itinerary for {destination}.

        Trip Requirements:
        - Destination: {destination}
        - Departure Location: {departure_location if departure_location else "Major city or international location"}
        - Duration: {duration} days
        - Traveler Preferences: {preferences}
        - Budget Range: {budget}

        Please create a comprehensive itinerary that includes:
        1. TRANSPORTATION TO AND FROM DESTINATION with specific details
        2. Popular attractions and must-see places with EXACT ADDRESSES
        3. Local restaurants and food experiences with FULL ADDRESSES
        4. Cultural activities and experiences with SPECIFIC LOCATIONS
        5. Transportation suggestions between locations
        6. Practical tips and advice
        7. Estimated costs for activities and transportation

        IMPORTANT: 
        - Provide detailed transportation from {departure_location if departure_location else "a major departure city"} to {destination} and back
        - Include flight/train/bus options with estimated costs and duration
        - For each activity, provide the complete street address
        - Include booking websites and tips for transportation

        Format your response as a JSON object with this exact structure:

        {{
            "destination_info": {{
                "name": "{destination}",
                "best_time_to_visit": "season/months",
                "currency": "local currency",
                "language": "primary language",
                "cultural_tips": ["tip1", "tip2", "tip3"]
            }},
            "outbound_transport": {{
                "departure_location": "{departure_location if departure_location else 'Major departure city'}",
                "arrival_location": "{destination}",
                "transport_type": "Flight/Train/Bus/Car",
                "duration": "X hours",
                "estimated_cost": "$XXX-XXX USD",
                "booking_info": "Booking websites or tips",
                "tips": "Travel tips for this route"
            }},
            "return_transport": {{
                "departure_location": "{destination}",
                "arrival_location": "{departure_location if departure_location else 'Major departure city'}",
                "transport_type": "Flight/Train/Bus/Car",
                "duration": "X hours", 
                "estimated_cost": "$XXX-XXX USD",
                "booking_info": "Booking websites or tips",
                "tips": "Return travel tips"
            }},
            "days": [
                {{
                    "day": 1,
                    "date": "Day 1",
                    "theme": "Arrival and City Introduction", 
                    "activities": [
                        {{
                            "name": "Activity Name",
                            "description": "Detailed description",
                            "location": "General area or neighborhood",
                            "address": "Complete street address with postal code",
                            "duration": "2-3 hours",
                            "estimated_cost": "$20-30 USD",
                            "category": "sightseeing",
                            "rating": 4.5,
                            "opening_hours": "9:00 AM - 6:00 PM",
                            "tips": "Practical tips for this activity",
                            "phone": "+1-234-567-8900 (if available)",
                            "website": "https://example.com (if known)"
                        }}
                    ],
                    "total_estimated_cost": "$80-120 USD",
                    "transportation_notes": "How to get around this day"
                }}
            ],
            "practical_info": {{
                "total_estimated_budget": "total budget range including transportation",
                "packing_suggestions": ["item1", "item2", "item3"],
                "important_phrases": {{"hello": "local greeting", "thank you": "local thanks"}},
                "emergency_info": "important emergency contacts or numbers",
                "local_transportation": "How to get around the destination city"
            }}
        }}

        Provide realistic, well-researched information based on your knowledge. Include 3-4 activities per day, balancing different types of experiences. Consider travel time between activities and provide practical advice.

        For transportation, research common routes and provide realistic costs and durations. Include multiple options when available (budget vs premium).

        Respond with ONLY the JSON structure, no other text.
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text

            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start != -1 and json_end != -1:
                json_str = response_text[json_start:json_end]
                try:
                    data = json.loads(json_str)
                    return self._parse_full_itinerary(data)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error: {e}")
                    return self._create_fallback_full_itinerary(destination, duration, preferences, budget,
                                                                departure_location)
            else:
                print("No JSON found in response")
                return self._create_fallback_full_itinerary(destination, duration, preferences, budget,
                                                            departure_location)

        except Exception as e:
            print(f"Error generating itinerary: {e}")
            return self._create_fallback_full_itinerary(destination, duration, preferences, budget, departure_location)

    def _parse_full_itinerary(self, data: Dict) -> TravelItinerary:
        """Parse AI-generated itinerary data into TravelItinerary object"""
        # Parse transportation
        outbound_data = data.get('outbound_transport', {})
        outbound_transport = TransportationInfo(
            departure_location=outbound_data.get('departure_location', 'Unknown'),
            arrival_location=outbound_data.get('arrival_location', 'Unknown'),
            transport_type=outbound_data.get('transport_type', 'Flight'),
            duration=outbound_data.get('duration', 'Unknown'),
            estimated_cost=outbound_data.get('estimated_cost', 'N/A'),
            booking_info=outbound_data.get('booking_info'),
            tips=outbound_data.get('tips')
        )

        return_data = data.get('return_transport', {})
        return_transport = TransportationInfo(
            departure_location=return_data.get('departure_location', 'Unknown'),
            arrival_location=return_data.get('arrival_location', 'Unknown'),
            transport_type=return_data.get('transport_type', 'Flight'),
            duration=return_data.get('duration', 'Unknown'),
            estimated_cost=return_data.get('estimated_cost', 'N/A'),
            booking_info=return_data.get('booking_info'),
            tips=return_data.get('tips')
        )

        # Parse days (reuse existing logic)
        day_plans = self._parse_itinerary_data(data)

        return TravelItinerary(
            destination=data.get('destination_info', {}).get('name', 'Unknown'),
            duration=len(day_plans),
            outbound_transport=outbound_transport,
            return_transport=return_transport,
            days=day_plans,
            destination_info=data.get('destination_info', {}),
            practical_info=data.get('practical_info', {})
        )

    def ask_question(self, question: str) -> str:
        """Ask the AI a travel-related question"""
        try:
            prompt = f"""
            You are a knowledgeable travel advisor. Answer this travel question with helpful, detailed, and practical information:

            Question: {question}

            Provide a comprehensive answer that includes:
            - Direct answer to the question
            - Practical tips and advice
            - Current general knowledge (as of your training)
            - Suggestions for further research if needed

            Be conversational but informative.
            """

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question: {str(e)}"

    def _parse_itinerary_data(self, data: Dict) -> List[DayPlan]:
        """Parse AI-generated itinerary data into DayPlan objects"""
        day_plans = []

        for day_data in data.get('days', []):
            activities = []
            for activity_data in day_data.get('activities', []):
                activity = Activity(
                    name=activity_data.get('name', 'Unknown Activity'),
                    description=activity_data.get('description', 'No description available'),
                    location=activity_data.get('location', 'Unknown location'),
                    address=activity_data.get('address', 'Address not available'),
                    duration=activity_data.get('duration', '1 hour'),
                    estimated_cost=activity_data.get('estimated_cost', 'Free'),
                    category=activity_data.get('category', 'general'),
                    rating=activity_data.get('rating'),
                    opening_hours=activity_data.get('opening_hours'),
                    tips=activity_data.get('tips'),
                    phone=activity_data.get('phone'),
                    website=activity_data.get('website')
                )
                activities.append(activity)

            day_plan = DayPlan(
                day=day_data.get('day', 1),
                date=day_data.get('date', f"Day {day_data.get('day', 1)}"),
                theme=day_data.get('theme', 'Exploration'),
                activities=activities,
                total_estimated_cost=day_data.get('total_estimated_cost', 'N/A'),
                transportation_notes=day_data.get('transportation_notes')
            )
            day_plans.append(day_plan)

        return day_plans

    def _create_fallback_full_itinerary(self, destination: str, duration: int, preferences: str, budget: str,
                                        departure_location: str = "") -> TravelItinerary:
        """Create a basic fallback itinerary with transportation if AI generation fails"""
        day_plans = self._create_fallback_itinerary(destination, duration, preferences, budget)

        # Create basic transportation info
        outbound_transport = TransportationInfo(
            departure_location=departure_location or "Your location",
            arrival_location=destination,
            transport_type="Flight",
            duration="2-8 hours (varies by location)",
            estimated_cost="$200-800 USD",
            booking_info="Check airline websites or travel booking sites",
            tips="Book in advance for better prices"
        )

        return_transport = TransportationInfo(
            departure_location=destination,
            arrival_location=departure_location or "Your location",
            transport_type="Flight",
            duration="2-8 hours (varies by location)",
            estimated_cost="$200-800 USD",
            booking_info="Check airline websites or travel booking sites",
            tips="Consider flexible dates for better prices"
        )

        return TravelItinerary(
            destination=destination,
            duration=duration,
            outbound_transport=outbound_transport,
            return_transport=return_transport,
            days=day_plans,
            destination_info={
                "name": destination,
                "best_time_to_visit": "Year-round",
                "currency": "Local currency",
                "language": "Local language"
            },
            practical_info={
                "total_estimated_budget": f"${duration * 100}-{duration * 200} USD plus transportation",
                "packing_suggestions": ["Comfortable shoes", "Weather-appropriate clothing", "Travel documents"]
            }
        )

    def _create_fallback_itinerary(self, destination: str, duration: int, preferences: str, budget: str) -> List[
        DayPlan]:
        """Create a basic fallback itinerary if AI generation fails"""
        day_plans = []

        for day in range(1, duration + 1):
            activities = [
                Activity(
                    name=f"Explore {destination}",
                    description=f"Discover the main attractions and highlights of {destination}",
                    location=f"Central {destination}",
                    address=f"City Center, {destination}",
                    duration="3-4 hours",
                    estimated_cost="$30-50",
                    category="sightseeing",
                    tips="Start early to avoid crowds"
                ),
                Activity(
                    name="Local Dining Experience",
                    description="Try authentic local cuisine at a recommended restaurant",
                    location=f"{destination} local restaurant",
                    address=f"Main Street District, {destination}",
                    duration="1-2 hours",
                    estimated_cost="$25-40",
                    category="dining",
                    tips="Ask locals for recommendations"
                ),
                Activity(
                    name="Cultural Experience",
                    description="Visit a local museum, market, or cultural site",
                    location=f"{destination} cultural district",
                    address=f"Cultural Quarter, {destination}",
                    duration="2-3 hours",
                    estimated_cost="$15-25",
                    category="culture",
                    tips="Check opening hours in advance"
                )
            ]

            day_plan = DayPlan(
                day=day,
                date=f"Day {day}",
                theme=f"Discover {destination}" if day == 1 else f"Explore {destination}",
                activities=activities,
                total_estimated_cost="$70-115",
                transportation_notes="Use public transport or walk when possible"
            )
            day_plans.append(day_plan)

        return day_plans


# Initialize the agent
travel_agent = SimplifiedTravelAgent()
# Flask routes were intentionally removed from this module. See
# `flask_app.py` at the repository root for the webserver entrypoint and
# route implementations that import `travel_agent` from this file.