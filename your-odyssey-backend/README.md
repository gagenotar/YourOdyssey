# YourOdyssey Backend

This is the Django backend for the YourOdyssey project.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

## Setup Instructions

1. Create a virtual environment:
   ```bash
   # Navigate to the project root
   cd YourOdyssey

   # Create virtual environment
   python3 -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Linux/macOS
   source .venv/bin/activate

   # On Windows
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   # Navigate to the backend directory
   cd your-odyssey-backend

   # Install required packages
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

The server will start at http://localhost:8000

## Development

- The API will be available at http://localhost:8000/api/
- Admin interface is available at http://localhost:8000/admin/
- Health check endpoint: http://localhost:8000/api/health/

## API Endpoints

- `GET /api/health/`: Check if the backend is running

## CORS Configuration

The backend is configured to accept requests from:
- http://localhost:5173 (Vite default dev server)
- http://localhost:5174 (Alternative Vite port)

## Common Issues

1. **ModuleNotFoundError: No module named 'django'**
   - Make sure you've activated the virtual environment
   - Try reinstalling dependencies: `pip install -r requirements.txt`

2. **Port already in use**
   - You can use a different port: `python manage.py runserver 8001`

## Maintaining Dependencies

When adding new Python packages:
1. Install them with pip while virtual environment is active
2. Update requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```
