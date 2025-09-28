import os
import json
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration - Only need Gemini API key to start
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


@dataclass
class Activity:
    name: str
    description: str
    location: str
    duration: str
    estimated_cost: str
    category: str
    rating: Optional[float] = None
    opening_hours: Optional[str] = None
    tips: Optional[str] = None


@dataclass
class DayPlan:
    day: int
    date: str
    theme: str
    activities: List[Activity]
    total_estimated_cost: str
    transportation_notes: Optional[str] = None


class SimplifiedTravelAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_itinerary(self, destination: str, duration: int, preferences: str, budget: str) -> List[DayPlan]:
        """Generate itinerary using Gemini directly"""

        prompt = f"""
        Create a detailed {duration}-day vacation itinerary for {destination}.

        Trip Requirements:
        - Destination: {destination}
        - Duration: {duration} days
        - Traveler Preferences: {preferences}
        - Budget Range: {budget}

        Please create a comprehensive itinerary that includes:
        1. Popular attractions and must-see places
        2. Local restaurants and food experiences
        3. Cultural activities and experiences
        4. Transportation suggestions
        5. Practical tips and advice
        6. Estimated costs for activities

        Format your response as a JSON object with this exact structure:

        {{
            "destination_info": {{
                "name": "{destination}",
                "best_time_to_visit": "season/months",
                "currency": "local currency",
                "language": "primary language",
                "cultural_tips": ["tip1", "tip2", "tip3"]
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
                            "location": "Specific location or area",
                            "duration": "2-3 hours",
                            "estimated_cost": "$20-30 USD",
                            "category": "sightseeing",
                            "rating": 4.5,
                            "opening_hours": "9:00 AM - 6:00 PM",
                            "tips": "Practical tips for this activity"
                        }}
                    ],
                    "total_estimated_cost": "$80-120 USD",
                    "transportation_notes": "How to get around this day"
                }}
            ],
            "practical_info": {{
                "total_estimated_budget": "total budget range",
                "packing_suggestions": ["item1", "item2", "item3"],
                "important_phrases": {{"hello": "local greeting", "thank you": "local thanks"}},
                "emergency_info": "important emergency contacts or numbers"
            }}
        }}

        Provide realistic, well-researched information based on your knowledge. Include 3-4 activities per day, balancing different types of experiences (cultural, food, sightseeing, relaxation). Consider travel time between activities and provide practical advice.

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
                    return self._parse_itinerary_data(data)
                except json.JSONDecodeError as e:
                    print(f"JSON parse error: {e}")
                    return self._create_fallback_itinerary(destination, duration, preferences, budget)
            else:
                print("No JSON found in response")
                return self._create_fallback_itinerary(destination, duration, preferences, budget)

        except Exception as e:
            print(f"Error generating itinerary: {e}")
            return self._create_fallback_itinerary(destination, duration, preferences, budget)

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
                    duration=activity_data.get('duration', '1 hour'),
                    estimated_cost=activity_data.get('estimated_cost', 'Free'),
                    category=activity_data.get('category', 'general'),
                    rating=activity_data.get('rating'),
                    opening_hours=activity_data.get('opening_hours'),
                    tips=activity_data.get('tips')
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
                    duration="3-4 hours",
                    estimated_cost="$30-50",
                    category="sightseeing",
                    tips="Start early to avoid crowds"
                ),
                Activity(
                    name="Local Dining Experience",
                    description="Try authentic local cuisine at a recommended restaurant",
                    location=f"{destination} local restaurant",
                    duration="1-2 hours",
                    estimated_cost="$25-40",
                    category="dining",
                    tips="Ask locals for recommendations"
                ),
                Activity(
                    name="Cultural Experience",
                    description="Visit a local museum, market, or cultural site",
                    location=f"{destination} cultural district",
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


# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.json
        destination = data.get('destination', '').strip()
        duration = int(data.get('duration', 3))
        preferences = data.get('preferences', '').strip()
        budget = data.get('budget', 'moderate').strip()

        if not destination:
            return jsonify({'error': 'Destination is required'}), 400

        if duration < 1 or duration > 14:
            return jsonify({'error': 'Duration must be between 1 and 14 days'}), 400

        # Generate itinerary using Gemini
        itinerary = travel_agent.generate_itinerary(destination, duration, preferences, budget)

        # Convert to dict for JSON response
        itinerary_dict = [asdict(day) for day in itinerary]

        return jsonify({
            'success': True,
            'itinerary': itinerary_dict,
            'destination': destination,
            'duration': duration
        })

    except Exception as e:
        return jsonify({'error': f'Failed to generate itinerary: {str(e)}'}), 500


@app.route('/ask_question', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question', '').strip()

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        answer = travel_agent.ask_question(question)

        return jsonify({
            'success': True,
            'answer': answer
        })

    except Exception as e:
        return jsonify({'error': f'Failed to get answer: {str(e)}'}), 500


@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'model': 'gemini-2.0-flash-exp'})


if __name__ == '__main__':
    print("🚀 Starting Simplified Travel Agent...")
    print("📍 Available at: http://localhost:5000")
    print("🤖 Using Gemini 2.0 Flash")
    print("🔧 API Endpoints:")
    print("   - POST /generate_itinerary")
    print("   - POST /ask_question")
    print("   - GET /health")

    if not GEMINI_API_KEY:
        print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
        print("   Please set your Gemini API key in the .env file")

    app.run(debug=True, host='0.0.0.0', port=5000)