# VentureVibe

<div align="center">

**Validate Ideas at the Speed of Thought**

*AI-Powered Product Validation Platform*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Node](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev/)

</div>

---

## 🚀 What is VentureVibe?

**VentureVibe** is your intelligent co-founder that never sleeps. Transform raw product ideas into data-driven strategic insights in seconds using advanced AI agents. Get comprehensive market research, competitive analysis, and feasibility assessments—all before you write a single line of code or invest a dollar.

### ✨ Key Value Propositions

- **⚡ Instant Validation** - Get results in under 60 seconds (vs. weeks/months with traditional research)
- **🤖 AI-Powered Insights** - Multi-agent system for comprehensive analysis
- **💰 Cost-Effective** - Affordable subscription vs. $5,000-$50,000+ consultants
- **🎯 Strategic Guidance** - Actionable recommendations tailored to your idea
- **📊 Data-Driven** - Quantified feasibility scoring (0-100) based on market dynamics

---

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.12+) - Lightning-fast async API
- **Database**: MongoDB with Motor - Scalable NoSQL database
- **AI**: Pydantic AI - Structured AI agent orchestration
- **LLM**: OpenAI GPT / OpenRouter - State-of-the-art language models
- **Authentication**: JWT tokens with Argon2/bcrypt password hashing
- **Observability**: Logfire, Opik, OpenTelemetry instrumentation

### Frontend
- **Framework**: React 19 with TypeScript - Type-safe component architecture
- **Build Tool**: Vite - Next-gen build tooling with HMR
- **Styling**: Tailwind CSS - Utility-first styling with VentureVibe brand colors
- **UI Components**: shadcn/ui + Custom Premium Components (Animated Logo, Progress Circles)
- **State Management**: React Query (TanStack Query) - Intelligent data fetching
- **Routing**: React Router v7 - Client-side routing
- **Validation**: Zod schemas - Runtime type validation
- **Notifications**: Sonner - Beautiful toast notifications

### Design System
- **Color Palette**: 
  - Primary: Electric Blue (#3B82F6)
  - Secondary: Vibrant Indigo (#6366F1)
  - Accent: Deep Purple (#8B5CF6)
- **Visual Style**: 
  - Glassmorphism header & cards
  - Dynamic micro-animations (float, pulse, shimmer)
  - Premium gradient aesthetics
- **Typography**: 
  - Headings: **Outfit** (Modern, geometric)
  - Body: **Inter** (Clean, legible)
- **Branding**: Custom "Lightbulb-to-Rocket" logo

---

## 📋 Prerequisites

- **Python**: 3.12 or higher
- **Node.js**: 18 or higher
- **Poetry**: Python dependency manager ([Install](https://python-poetry.org/docs/#installation))
- **Docker**: For MongoDB (or local MongoDB installation)
- **OpenAI API Key**: Required for AI features ([Get one](https://platform.openai.com/api-keys))
- **OpenRouter API Key**: Alternative for accessing various models ([Get one](https://openrouter.ai/keys))

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Valaery/VentureVibe
cd VentureVibe
```

### 2. Backend Setup

#### Start MongoDB

Using Docker (recommended):
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
DATABASE_NAME=venture_vibe

# JWT Authentication
SECRET_KEY=your-secret-key-here-change-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (Required, can use OpenRouter API Key instead)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Logfire (Optional - for observability)
LOGFIRE_TOKEN=your-logfire-token-here

# Opik (Optional - for AI monitoring)
OPIK_API_KEY=your-opik-api-key-here
```

#### Run the Backend

```bash
poetry shell
cd backend
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

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

The application will be available at **`http://localhost:5173`**

---

## 🎯 Usage Guide

### 1. Create Your Account
1. Navigate to `http://localhost:5173`
2. Click **"Start Free Trial"**
3. Fill in your details (name, email, password)
4. You'll be automatically logged in

### 2. Validate Your Product Idea
1. Enter your product concept in the **"Product Idea"** field
2. Specify your **target audience** (e.g., "Remote workers", "SaaS founders")
3. Click **"Get Instant Validation"**
4. Watch as AI agents analyze your idea in real-time

### 3. Review Your Results
Your comprehensive analysis includes:
- **📊 Feasibility Score** (0-100) - Quantified assessment with color-coded badge
- **📈 Market Analysis** - Size, trends, growth potential
- **🏢 Competitor Analysis** - Direct and indirect competitors with strategic positioning
- **💡 Strategic Advice** - Actionable next steps customized to your idea

---

## 🏛️ Project Architecture

```
venturevibe/
├── backend/
│   ├── src/
│   │   ├── main.py                      # FastAPI application entry point
│   │   ├── app.py                       # App factory with CORS & middleware
│   │   ├── config/
│   │   │   └── settings.py             # Configuration management
│   │   ├── domain/                      # Domain models (User, Research)
│   │   │   ├── entities/               # Core business entities
│   │   │   ├── repositories/           # Repository interfaces
│   │   │   └── value_objects/          # Value objects
│   │   ├── application/                 # Use cases and services
│   │   │   ├── use_cases/              # Business logic orchestration
│   │   │   └── services/               # Application services
│   │   ├── infrastructure/              # External integrations
│   │   │   ├── database/               # MongoDB connection & repos
│   │   │   ├── ai/                     # Pydantic AI agents
│   │   │   └── web/                    # FastAPI routers
│   │   └── core/                        # Core utilities
│   │       ├── security.py             # JWT & password hashing
│   │       └── dependencies.py         # FastAPI dependencies
│   └── tests/                           # Backend tests
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                     # React entry point
│   │   ├── App.tsx                      # Root component with routing
│   │   ├── index.css                    # Global styles & VentureVibe colors
│   │   ├── components/
│   │   │   ├── layout/                 # Layout components
│   │   │   └── ui/                     # shadcn/ui components
│   │   ├── features/                    # Feature-based modules
│   │   │   ├── auth/
│   │   │   │   ├── components/        # LoginForm, RegisterForm
│   │   │   │   ├── data/              # Auth schemas & API service
│   │   │   │   └── hooks/             # useAuthContext, mutations
│   │   │   └── research/
│   │   │       ├── components/        # ResearchForm, ResultDisplay
│   │   │       ├── data/              # Research schemas & API service
│   │   │       └── hooks/             # useResearchMutation
│   │   ├── pages/                       # Page components
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   └── ResearchPage.tsx
│   │   ├── core/                        # Core utilities
│   │   │   └── api/                    # Axios client configuration
│   │   └── lib/                         # Utility functions
│   └── public/                          # Static assets
├── docker-compose.yml                   # MongoDB setup
├── pyproject.toml                       # Python dependencies (Poetry)
├── package.json                         # Frontend dependencies
└── README.md                            # This file
```

---

## 🧪 Testing

### Backend Tests

```bash
poetry shell
pytest
pytest --cov=src tests/  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage  # With coverage
```

---

## 🏗️ Building for Production

### Backend

```bash
poetry build
# Deploy the built package to your server
```

### Frontend

```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/` - ready to deploy to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Any static hosting service

---

## 🔑 Core Features

### 🔐 Authentication & Security
- JWT-based authentication with secure token management
- Argon2/bcrypt password hashing (enterprise-grade)
- Protected routes and API endpoints
- CORS configuration for secure cross-origin requests

### 🤖 AI-Powered Research Engine
- **Multi-Agent System**: Specialized AI agents for different analysis aspects
- **Market Analysis**: Size, trends, growth potential, TAM/SAM/SOM
- **Competitor Intelligence**: Direct and indirect competitors with positioning
- **Feasibility Scoring**: Quantified 0-100 assessment
- **Strategic Recommendations**: Actionable next steps

### 🎨 Premium UI/UX
- **VentureVibe Brand Colors**: Electric Blue, Vibrant Indigo, Deep Purple
- **Glassmorphic Design**: Backdrop blur, gradient backgrounds, premium shadows
- **Responsive**: Mobile-first design with adaptive layouts
- **Accessible**: ARIA-compliant components, high contrast text
- **Interactive**: 
  - Micro-interactions & hover effects
  - Loading skeletons & spinners
  - Animated data visualization (Progress Circles)
- **Organized Results**: Badge-based lists, clean typography hierarchy

### 🏛️ Architecture Patterns
- **Backend**: Clean Architecture with Domain-Driven Design
- **Frontend**: Feature-based architecture with clear separation of concerns
- **API**: RESTful with OpenAPI/Swagger documentation
- **State Management**: React Query for server state, Context for auth
- **Validation**: Zod schemas for runtime type safety

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/register` | Register new user | ❌ |
| `POST` | `/api/auth/login` | Login and get JWT token | ❌ |

### Research Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/research` | Create new research analysis | ✅ |
| `GET` | `/api/research/{id}` | Get research by ID | ✅ |
| `GET` | `/api/research` | List all user's research | ✅ |

### User Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/users/me` | Get current user profile | ✅ |

**Full API Documentation**: Visit `http://localhost:8000/docs` when running the backend

---

## 🛠️ Development

### Code Style

**Backend**:
- Follow PEP 8 style guide
- Use type hints for all functions
- Docstrings for public methods
- Black formatter (optional)

**Frontend**:
- ESLint configuration enforced
- TypeScript strict mode enabled
- Prettier for formatting (optional)
- Component naming: PascalCase

### Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes with clear commit messages
3. Run tests: `pytest` (backend) and `npm test` (frontend)
4. Push and create a pull request
5. Wait for review and CI checks

---

## 🐛 Troubleshooting

### MongoDB Connection Issues

```bash
# Check if Docker is running
docker ps

# Check MongoDB logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb

# Verify connection string in .env
echo $MONGODB_URL
```

### Frontend Build Issues

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite

# Clear browser cache and hard reload
# Chrome: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
```

### Backend Import Errors

```bash
# Ensure you're in the poetry shell
poetry shell

# Reinstall dependencies
poetry install

# Check Python version
python --version  # Should be 3.12+

# Verify PYTHONPATH
echo $PYTHONPATH
```

### OpenAI API Issues

```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API key with curl
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check rate limits and billing at platform.openai.com
```

---

## 🌟 Acknowledgments

Built with amazing open-source technologies:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Pydantic AI](https://ai.pydantic.dev/) - AI agent framework
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful UI components
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [MongoDB](https://www.mongodb.com/) - NoSQL database

---

## 💼 Portfolio Project

This is a **portfolio project** demonstrating full-stack development capabilities including:

### Technical Skills Showcased
- **Backend Development**: FastAPI, Clean Architecture, Domain-Driven Design
- **Frontend Development**: React 19, TypeScript, Modern UI/UX patterns
- **AI Integration**: Pydantic AI, OpenAI GPT, Multi-agent systems
- **Database Design**: MongoDB, Repository pattern
- **Authentication**: JWT, Argon2/bcrypt password hashing
- **API Design**: RESTful APIs with OpenAPI documentation
- **State Management**: React Query, Context API
- **Styling**: Tailwind CSS, shadcn/ui, Responsive design
- **DevOps**: Docker, Environment configuration
- **Testing**: pytest, React Testing Library
- **Code Quality**: TypeScript strict mode, ESLint, Type safety

### Architecture Highlights
- Clean separation of concerns (Domain, Application, Infrastructure layers)
- Feature-based frontend architecture
- Type-safe validation with Zod
- Secure authentication and authorization
- Observability and monitoring integration
- Scalable NoSQL database design

---

<div align="center">

**VentureVibe** - *AI-Powered Product Validation Platform*

**A portfolio project by Joan Alcaraz**

Showcasing modern full-stack development with AI integration

---

**Tech Stack**: Python • FastAPI • React • TypeScript • MongoDB • Pydantic AI • Tailwind CSS

[LinkedIn](https://linkedin.com/in/joanalcarazrego)

</div>