# Story LLM

A full-stack application to evaluate product ideas using AI agents. Built with FastAPI, React, and MongoDB.

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Database**: MongoDB
- **AI**: Pydantic AI with OpenAI
- **Authentication**: JWT tokens with bcrypt/argon2
- **Observability**: Logfire, Opik, OpenTelemetry

### Frontend
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI primitives)
- **State Management**: React Query (TanStack Query)
- **Routing**: React Router v7
- **Validation**: Zod schemas
- **Notifications**: Sonner (toast notifications)

## 📋 Prerequisites

- **Python**: 3.12 or higher
- **Node.js**: 18 or higher
- **Poetry**: Python dependency manager
- **Docker**: For MongoDB (or local MongoDB installation)
- **OpenAI API Key**: Required for AI features

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd story-llm
```

### 2. Backend Setup

#### Start MongoDB

Using Docker:
```bash
docker-compose up -d
```

Or use a local MongoDB instance running on `mongodb://localhost:27017`

#### Install Python Dependencies

```bash
poetry install
```

#### Configure Environment Variables

Create a `.env` file in the root directory:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=story_llm

# JWT Authentication
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=your-openai-api-key-here

# Logfire (optional)
LOGFIRE_TOKEN=your-logfire-token-here

# Opik (optional)
OPIK_API_KEY=your-opik-api-key-here
```

#### Run the Backend

```bash
poetry shell
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment (Optional)

Create a `.env` file in the `frontend` directory if you need to customize the API URL:

```env
VITE_API_URL=http://localhost:8000
```

#### Run the Frontend

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 🎯 Usage

### 1. Register an Account
- Navigate to `http://localhost:5173`
- Click "Register" and create an account
- You'll be automatically logged in and redirected to the research page

### 2. Evaluate a Product Idea
- Enter your product idea in the "Product Idea" field
- Specify your target audience
- Click "Start Research"
- Wait for the AI agents to analyze your idea
- View the results including:
  - Feasibility score (0-100)
  - Market analysis
  - Competitor analysis
  - Strategic advice

## 🏛️ Project Structure

```
story-llm/
├── backend/
│   ├── src/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── core/                   # Core utilities (config, security)
│   │   ├── domain/                 # Domain models and business logic
│   │   ├── application/            # Use cases and services
│   │   ├── infrastructure/         # External integrations (DB, AI)
│   │   └── presentation/           # API routes and DTOs
│   └── tests/                      # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/             # Shared UI components
│   │   │   ├── layout/            # Layout components (AppShell)
│   │   │   └── ui/                # shadcn/ui components
│   │   ├── features/              # Feature-based modules
│   │   │   ├── auth/              # Authentication feature
│   │   │   │   ├── components/   # Auth UI components
│   │   │   │   ├── data/         # Schemas & services
│   │   │   │   └── hooks/        # React hooks & mutations
│   │   │   └── research/          # Research feature
│   │   │       ├── components/   # Research UI components
│   │   │       ├── data/         # Schemas & services
│   │   │       └── hooks/        # React hooks & mutations
│   │   ├── pages/                 # Page components
│   │   └── core/                  # Core utilities (API client)
│   └── public/                     # Static assets
├── .claude/                        # Documentation
│   └── doc/
│       └── frontend_refinement/   # Implementation plans
├── docker-compose.yml              # MongoDB setup
├── pyproject.toml                  # Python dependencies
└── README.md                       # This file
```

## 🧪 Running Tests

### Backend Tests

```bash
poetry shell
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🏗️ Building for Production

### Backend

```bash
poetry build
```

### Frontend

```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/`

## 🔑 Key Features

### Authentication
- JWT-based authentication
- Secure password hashing (bcrypt/argon2)
- Protected routes and API endpoints

### AI-Powered Research
- Multi-agent system for comprehensive analysis
- Market analysis and feasibility scoring
- Competitor identification
- Strategic recommendations

### Modern UI/UX
- Responsive design with Tailwind CSS
- Premium shadcn/ui components
- Toast notifications for user feedback
- Loading states and error handling
- Collapsible sections with accordions
- Smooth animations and transitions

### Architecture Patterns
- **Backend**: Clean Architecture with Domain-Driven Design
- **Frontend**: Feature-based architecture
- **API**: RESTful with OpenAPI documentation
- **State**: React Query for server state management
- **Validation**: Zod schemas for type-safe validation

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Research
- `POST /api/research` - Create new research analysis
- `GET /api/research/{id}` - Get research by ID
- `GET /api/research` - List all research (authenticated)

### Users
- `GET /api/users/me` - Get current user profile

## 🛠️ Development

### Code Style
- **Backend**: Follow PEP 8, use type hints
- **Frontend**: ESLint configuration, TypeScript strict mode

### Git Workflow
1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## 🐛 Troubleshooting

### MongoDB Connection Issues
- Ensure Docker is running: `docker ps`
- Check MongoDB logs: `docker-compose logs mongodb`
- Verify connection string in `.env`

### Frontend Build Issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

### Backend Import Errors
- Ensure you're in the poetry shell: `poetry shell`
- Reinstall dependencies: `poetry install`

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

## 📧 Contact

[Your Contact Information]
