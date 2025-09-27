# YourOdyssey Frontend

The frontend application for YourOdyssey, built with React, TypeScript, and Vite.

## Tech Stack

- ⚛️ React 18
- 🏗️ TypeScript
- ⚡️ Vite for fast development and building
- �️ React Router for navigation
- � TailwindCSS for styling
- � Fetch API for backend communication

## Getting Started

## Getting Started

### Prerequisites

- Node.js 16.x or higher
- npm 7.x or higher
- Backend server running (see ../your-odyssey-backend/README.md)

### Installation

1. Clone the repository (if you haven't already):
   ```bash
   git clone https://github.com/gagenotar/YourOdyssey.git
   cd YourOdyssey/your-odyssey-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Development

1. Start the development server:
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:5173`

2. Make sure the backend server is running at `http://localhost:8000`

### Building for Production

1. Create a production build:
   ```bash
   npm run build
   ```
   This will generate optimized files in the `dist` directory.

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t your-odyssey-frontend .
   ```

2. Run the container:
   ```bash
   docker run -p 5173:5173 your-odyssey-frontend
   ```

## Project Structure

```
your-odyssey-frontend/
├── app/                    # Application source code
│   ├── utils/             # Utility functions and API calls
│   ├── welcome/           # Welcome page component
│   ├── routes/            # Route components
│   ├── app.css           # Global styles
│   ├── root.tsx          # Root component
│   └── routes.ts         # Route definitions
├── public/                # Static files
├── package.json          # Project dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── vite.config.ts        # Vite configuration
└── Dockerfile            # Docker configuration
```

## Development Guidelines

1. **TypeScript**: Use TypeScript for all new files
2. **Styling**: Use TailwindCSS classes for styling
3. **API Calls**: Place all API-related functions in `app/utils/api.ts`
4. **Components**: Create new components in feature-specific directories under `app/`

```bash
docker build -t my-app .

# Run the container
docker run -p 3000:3000 my-app
```

The containerized application can be deployed to any platform that supports Docker, including:

- AWS ECS
- Google Cloud Run
- Azure Container Apps
- Digital Ocean App Platform
- Fly.io
- Railway

### DIY Deployment

If you're familiar with deploying Node applications, the built-in app server is production-ready.

Make sure to deploy the output of `npm run build`

```
├── package.json
├── package-lock.json (or pnpm-lock.yaml, or bun.lockb)
├── build/
│   ├── client/    # Static assets
│   └── server/    # Server-side code
```

## Styling

This template comes with [Tailwind CSS](https://tailwindcss.com/) already configured for a simple default starting experience. You can use whatever CSS framework you prefer.

---

Built with ❤️ using React Router.
