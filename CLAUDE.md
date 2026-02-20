# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VentureVibe** — An AI-powered product validation platform.

- Validates product ideas via multi-agent AI system (Pydantic AI + OpenAI/OpenRouter), delivering market analysis, competitor intelligence, and feasibility scoring
- Full-stack application: Python 3.12 FastAPI backend + React 19 frontend
- Database: MongoDB + Motor (async driver)
- Observability: Logfire + Opik
- Deployment: Docker Compose

## Architecture

### Monorepo Structure

```
VentureVibe/
├── backend/         # Python FastAPI (hexagonal architecture)
├── frontend/        # React 19 + TypeScript (feature-based)
├── .claude/         # Agents, commands, skills
└── docker-compose.yml
```

### Backend — Hexagonal Architecture

**Dependency flow: api → infrastructure → application → domain**

```
backend/src/
  domain/
    entities.py          # User, Research domain models
    exceptions.py        # Domain-specific errors

  application/
    ports/
      agent_service.py   # AgentService abstract interface
      repositories.py    # Repository abstract interfaces
    use_cases/
      auth_service.py    # Authentication business logic
      workflow_service.py# Research workflow orchestration

  infrastructure/
    adapters/
      agent_adapter.py   # Pydantic AI concrete agent
      repositories/
        mongo_repositories.py
        mongo_user_repository.py
    web/
      routers/
        auth.py          # /api/auth endpoints
        api.py           # /api/research endpoints
      dtos/
        schemas.py       # Pydantic request/response models
      security.py        # JWT & password hashing (Argon2/bcrypt)
      dependencies.py    # FastAPI DI container
    database.py          # MongoDB connection lifecycle

  config/
    settings.py          # Environment & settings management
```

**Key rules:**
- Domain layer: NO FastAPI/Pydantic imports (framework-independent)
- Use cases: Constructor injection, single `execute()` method
- Ports: Abstract interfaces in domain, concrete implementations in infrastructure
- DTOs: Pydantic models in infrastructure/web/dtos only
- Error handling: Map domain exceptions to HTTP status codes in middleware

### Frontend — Feature-Based Architecture

```
frontend/src/
  core/
    data/
      api.ts             # Axios API client
  features/
    auth/
      components/        # LoginForm, RegisterForm
      data/
        schemas/         # authSchemas.ts (Zod)
        services/        # authService.ts
      hooks/             # useAuthContext
    research/
      components/        # ResearchForm, ResearchResultDisplay
      data/
        schemas/         # researchSchemas.ts (Zod)
        services/        # researchService.ts
      hooks/
        mutations/       # useResearchMutation
        queries/         # useResearchQuery
  components/
    ui/                  # shadcn/ui + custom (progress-circle, skeleton, etc.)
    brand/               # VentureVibeLogo
  pages/                 # LoginPage, RegisterPage, ResearchPage
  lib/
    utils.ts             # Utility functions
```

**Key rules:**
- Server state: TanStack Query (`useQuery`, `useMutation`)
- Client state: Context API or `useState`
- HTTP client: Axios via `core/data/api.ts`
- Custom hooks encapsulate feature logic
- Components: shadcn/ui from `@/components/ui/`
- Routing: React Router v7 with lazy loading
- Type safety: TypeScript strict mode

### Docker Compose Services

| Service | Port | Purpose |
|---------|------|---------|
| mongodb | 27017 | Document database |

## Development Commands

### Backend

```bash
# From project root
poetry install               # Install dependencies
poetry run pytest            # Run tests (80% coverage enforced)
# Dev server
python -m uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
# From frontend/ directory
npm install           # Install dependencies
npm run dev           # Vite dev server
npm run build         # Production build (tsc + vite build)
npm run lint          # ESLint
npm run preview       # Preview production build
```

### Docker

```bash
docker compose up -d     # Start MongoDB
docker compose down      # Stop services
```

## AI Agent System

Specialized agents in `.claude/agents/`:

| Agent | Expertise |
|-------|-----------|
| backend-developer | Hexagonal architecture, Python/FastAPI |
| backend-test-engineer | Backend testing, pytest |
| frontend-developer | React 19, feature-based architecture |
| frontend-test-engineer | Frontend testing, React Testing Library, Vitest |
| market-research-analyst | Market research, competitive analysis |
| opik-architect | Opik AI observability integration |
| playwright-link-scraper | Web scraping, Playwright automation |
| product-strategy-analyst | Product strategy, idea validation |
| pydantic-ai-architect | Pydantic AI agent design |
| qa-criteria-validator | Acceptance criteria, Playwright testing |
| shadcn-ui-architect | shadcn/ui components, Tailwind CSS |
| ui-ux-analyzer | UI/UX review, Playwright automation |
| web-content-summarizer | Web content analysis and summarization |

**Usage rules:**
- Sub-agents do research and report feedback; you do the actual implementation
- Exception: `backend-test-engineer` and `frontend-test-engineer` can and should do implementation directly
- Run backend + frontend agents concurrently when possible
- When passing tasks to sub-agents, include the context file path

## Custom Commands

Commands in `.claude/commands/`:

| Command | Purpose |
|---------|---------|
| `explore-plan` | Plan implementation for a user request |
| `ideation` | Generate and explore feature ideas |
| `create-new-gh-issue` | Create a well-structured GitHub issue |
| `implement-feedback` | Apply feedback from a GitHub issue |
| `update-feedback` | Update a GitHub issue with progress |
| `analyze_bug` | Analyze a bug or error |
| `worktree` | Git worktree management |
| `worktree-tdd` | Create worktree from GitHub issue with TDD |
| `rule2hook` | Convert project rules to Claude Code hooks |

## Code Writing Standards

- **Address me as "Joan"** in all communications
- **Simplicity First**: Prefer simple, clean, maintainable solutions over clever ones
- **ABOUTME Comments**: All files must start with a 2-line comment, each line prefixed with `ABOUTME: `
- **Minimal Changes**: Make the smallest reasonable changes to achieve the desired outcome
- **Style Matching**: Match existing code style/formatting within each file
- **Preserve Comments**: Never remove comments unless provably false
- **No Temporal Naming**: Avoid 'new', 'improved', 'enhanced', 'recently' in names/comments
- **Evergreen Documentation**: Comments describe the code as it is, not its history
- **No Unrelated Changes**: If you notice something unrelated that should be fixed, document it rather than fixing it
- **No Whitespace Changes**: Do not change whitespace unrelated to code you're modifying
- **Never Rewrite Without Permission**: Never throw away implementations to rewrite them without explicit permission
- **No Stray .md Files**: Never create .md files (reports, plans, feedback, summaries) in the project root or subproject roots (`frontend/`, `backend/`). The only root .md files allowed are `CLAUDE.md`, `README.md`, `API.md`, and `DOCKER.md`. Any other generated .md output goes to `docs/`

## Version Control

- Non-trivial edits must be tracked in git, don't ask, just commit.
- If there are uncommitted changes when starting work, ask how to handle them
- Create WIP branches for new work when no clear branch exists
- Commit frequently throughout development
- **Commit format:** `feat(scope): description` (conventional commits)
- **Build verification:** Run `npm run build` (frontend) after each task group

## Testing Requirements

**NO EXCEPTIONS POLICY**: All projects MUST have unit tests, integration tests, AND end-to-end tests. The only way to skip: Joan EXPLICITLY states "I AUTHORIZE YOU TO SKIP WRITING TESTS THIS TIME."

**Every implementation task MUST:**
1. Implement the feature
2. Write comprehensive tests immediately (same session)
3. Document test status in `backend/tests/VALIDATION_STATUS.md` or `frontend/tests/VALIDATION_STATUS.md`
4. Validate tests can run

**Coverage targets:**
- Backend: >80% (enforced in pyproject.toml)
- Frontend: >70%

**Test organization:**
```
backend/tests/
├── conftest.py        # Fixtures & configuration
└── test_api.py        # API endpoint tests

frontend/tests/        # (to be set up)
```

**Testing principles:**
- Domain layer: ZERO external dependencies, mock all ports
- Infrastructure: Unit tests mock clients, integration tests use real services
- If environment isn't set up, still write the tests and note "Pending environment setup"

## Sub-Agent Workflow

- Before starting work, check for `.claude/sessions/context_session_{feature_name}.md` — read it if it exists, create it if it doesn't
- After finishing work or each phase, update the context session file
- When passing tasks to sub-agents, include the context file path
- After each sub-agent finishes, read their documentation before executing

## MCP Servers

See `.mcp.json` for configuration. Key servers:

- **context7**: Up-to-date framework docs (React, FastAPI, etc.)
- **sequentialthinking**: Multi-step problem breakdown
- **playwright**: E2E testing and web automation
- **shadcn-components**: Component source, demos, metadata
- **memory**: Persistent knowledge graph
- **github**: Issues, PRs, code search
- **logfire**: Structured logging and traces

## Environment Variables

Required in `.env`:
- `MONGODB_URL` — MongoDB connection string
- `DATABASE_NAME` — Database name (`venturevibe_db`)
- `SECRET_KEY` — JWT signing secret
- `ALGORITHM` — JWT algorithm (`HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — Token lifetime in minutes
- `OPENAI_API_KEY` — OpenAI API key (required)
- `LOGFIRE_TOKEN` — Logfire token (optional)
- `OPIK_API_KEY` — Opik API key (optional)

## CI/CD Workflows

*Not yet configured.*

## Key Documentation

- Project overview: `README.md`
- Backend entry point: `backend/src/main.py`
- Environment setup: `.env.example`
