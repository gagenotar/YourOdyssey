Auth0 quick setup for YourOdyssey backend

This file explains the minimal steps to configure Auth0 for local development and how to test protected endpoints.

1) Create an Auth0 API
   - In the Auth0 dashboard, create an API (e.g., `yourodyssey-api`).
   - Note the API Identifier (this is the `AUTH0_AUDIENCE`).

2) Create an Auth0 Application for the frontend
   - Create a Single Page Application or Regular Web Application.
   - Set Allowed Callback URLs to `http://localhost:5173/callback` (or your app URL).
   - Allowed Logout URLs: `http://localhost:5173`.
   - Allowed Web Origins: `http://localhost:5173`.

3) Configure environment variables
   - In `trip_planner/.env` or your environment, set:
     AUTH0_DOMAIN=your-auth0-domain.auth0.com
     AUTH0_AUDIENCE=your-api-audience-or-client-id

4) Install dependencies and run backend
   - From `your-odyssey-backend/`:
     pip install -r requirements.txt
     python flask_app.py

5) Which endpoints require authentication
    - Public (no authentication required):
       - POST /generate_itinerary — anyone can generate an itinerary.
       - POST /ask_question — anyone can ask travel-related questions.

    - Protected (requires a valid Auth0 access token in Authorization: Bearer <token>):
       - POST /saved_trips — save an itinerary (logged-in users only).
       - GET /saved_trips — list saved itineraries for the current user.
       - GET /me — returns basic user claims for the logged-in user.

6) Test protected endpoints
    - Obtain an access token (from the frontend `getAccessTokenSilently()` or Auth0 dashboard "API Explorer").
    - Example using `curl` to list saved trips:

       curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://localhost:5000/saved_trips

    - Example: anonymous request (no Authorization header) will return 401 or a JSON error:

          curl http://localhost:5000/saved_trips

       Expected: 401 Unauthorized or JSON {"error": "Authorization header is expected"}

Notes
- The backend uses the `python-jose` package and a small helper `trip_planner/auth0.py` to fetch the JWKS and verify RS256 tokens.
- If you get "Unable to find appropriate key", confirm that the token's `kid` matches a key in the JWKS for your Auth0 tenant.
- For local development you can also use Auth0's OAuth2 playground to mint test tokens.
