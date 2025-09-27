# YourOdyssey

Full-stack web application with React frontend and Django backend.

## Project Structure

- `/your-odyssey-frontend/`: React frontend using Vite
- `/your-odyssey-backend/`: Django backend

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/gagenotar/YourOdyssey.git
   cd YourOdyssey
   ```

2. Set up the backend:
   ```bash
   # Create and activate virtual environment
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install backend dependencies
   cd your-odyssey-backend
   pip install -r requirements.txt
   python manage.py migrate
   ```

3. Set up the frontend:
   ```bash
   cd ../your-odyssey-frontend
   npm install
   ```

4. Start both servers:
   
   In one terminal (backend):
   ```bash
   cd your-odyssey-backend
   source ../.venv/bin/activate  # On Windows: ..\.venv\Scripts\activate
   python manage.py runserver
   ```

   In another terminal (frontend):
   ```bash
   cd your-odyssey-frontend
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/

## Development

See individual README files in each directory for specific setup and development instructions:
- [Frontend README](your-odyssey-frontend/README.md)
- [Backend README](your-odyssey-backend/README.md)