# YourOdyssey Backend

This is the Django backend for the YourOdyssey project.
````markdown
# YourOdyssey Backend (Flask)

This repo runs a small Flask backend that provides the travel AI endpoints used by the frontend.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

## Setup & Run (local)

1. Create and activate a virtual environment:
   ```bash
   cd /path/to/YourOdyssey
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   cd your-odyssey-backend
   pip install -r requirements.txt
   ```

3. Provide your Gemini API key in a `.env` file at the backend root:
   ```ini
   GEMINI_API_KEY=your_api_key_here
   ```

4. Start the Flask server:
   ```bash
   # Development
   python flask_app.py
   ```

The server will start at http://localhost:5000 by default.

## API Endpoints (matching the frontend client)

- `POST /generate_itinerary` — body: { destination, duration, preferences, budget, departure_location }
- `POST /ask_question` — body: { question }
- `GET /health` — returns basic health info

## Docker

The project's `Dockerfile` runs `flask_app.py` by default. Build and run as you normally would for a Python service.

## Notes

- Django files were removed to simplify this hackathon backend. The travel AI logic is in `trip_planner/agent.py` and the webserver entrypoint is `flask_app.py`.

````
## API Endpoints
