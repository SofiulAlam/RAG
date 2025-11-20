# AI-Powered Application Builder

Build web applications through natural language prompts. Powered by Claude AI with intelligent prompt enhancement, context management, and iterative development workflows.

## Features

### 🎯 Core Features (MVP)

- **Prompt Enhancement System** - One-click AI-powered prompt improvement
- **Project & System Prompts** - Customizable instructions that guide AI behavior
- **Context Management** - Smart handling of conversation history to prevent memory loss
- **Incremental Changes** - Make small, precise changes without regenerating everything
- **File Locking** - Protect files from AI modification
- **Live Preview** - Real-time preview of generated application with hot reload
- **Code Streaming** - Stream AI-generated code token-by-token
- **Monaco Editor** - Professional code editing experience
- **File Tree** - Visual file management with lock indicators

### 🚀 Advanced Features

- **Template Library** - Pre-built prompt templates for common apps
- **Deployment System** - One-click deployment to hosting platforms
- **Troubleshooting Guidance** - Detect issues and guide users to solutions
- **Production-Ready Code** - Generate code that meets industry standards

## Tech Stack

### Frontend
- **Next.js 14+** (App Router, TypeScript, React Server Components)
- **Monaco Editor** for code editing
- **shadcn/ui + Radix UI** for components
- **Tailwind CSS** for styling
- **Socket.io Client** for real-time updates
- **Zustand** for state management
- **React Query** for server state

### Backend
- **FastAPI** (Python 3.11+) with async/await
- **LangChain** for LLM orchestration
- **Python-socketio** for real-time communication
- **SQLAlchemy 2.0** ORM
- **Pydantic v2** for validation
- **PostgreSQL** for database
- **Redis** for caching

### AI/LLM
- **Primary**: Anthropic Claude 3.5 Sonnet API
- **Fallback**: OpenAI GPT-4 Turbo

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)
- Anthropic API key
- PostgreSQL (via Docker or local)
- Redis (via Docker or local)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-app-builder
   ```

2. **Set up environment variables**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your API keys

   # Frontend
   cp frontend/.env.local.example frontend/.env.local
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Start PostgreSQL and Redis (via Docker)
docker-compose up postgres redis -d

# Run migrations
alembic upgrade head

# Start the server
python main.py
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local

# Start development server
npm run dev
```

## Project Structure

```
ai-app-builder/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # Next.js app directory
│   │   ├── dashboard/       # Dashboard pages
│   │   ├── templates/       # Template library
│   │   └── globals.css      # Global styles
│   ├── components/          # React components
│   │   ├── chat/           # Chat interface components
│   │   ├── editor/         # Editor components
│   │   ├── templates/      # Template components
│   │   └── ui/             # UI components (shadcn/ui)
│   ├── lib/                # Utilities
│   └── package.json
│
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── endpoints/  # API endpoint handlers
│   │   ├── core/           # Core configuration
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic services
│   ├── main.py             # FastAPI application entry point
│   └── requirements.txt
│
├── docker-compose.yml       # Docker compose configuration
└── README.md
```

## API Documentation

### Key Endpoints

#### Projects
- `POST /api/projects` - Create a new project
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `PUT /api/projects/{id}/prompt` - Update project prompt

#### Chat
- `GET /api/chat/{project_id}/messages` - Get chat messages
- `POST /api/chat/{project_id}/messages` - Send message
- `POST /api/chat/{project_id}/summarize` - Summarize and reset chat

#### Prompts
- `POST /api/prompts/enhance` - Enhance a prompt with AI

#### Files
- `GET /api/files/{project_id}` - List project files
- `GET /api/files/{project_id}/{path}` - Get file content
- `POST /api/files/{project_id}` - Create file
- `PUT /api/files/{project_id}/{path}` - Update file
- `DELETE /api/files/{project_id}/{path}` - Delete file

Full API documentation available at: http://localhost:8000/docs

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ai_app_builder

# Redis
REDIS_URL=redis://localhost:6379/0

# AI API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional fallback

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Environment
ENVIRONMENT=development
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## Development Roadmap

### ✅ Phase 1: Foundation (Completed)
- [x] Project setup and infrastructure
- [x] Database models and schema
- [x] Basic API endpoints
- [x] Frontend structure with Next.js
- [x] UI components with shadcn/ui

### ✅ Phase 2: Core Features (Completed)
- [x] Prompt Enhancement System
- [x] Project and System Prompts
- [x] Monaco Editor integration
- [x] File Tree component
- [x] Chat Interface
- [x] Live Preview
- [x] Context Management
- [x] Claude API integration

### 🚧 Phase 3: Advanced Features (In Progress)
- [ ] Authentication system
- [ ] Incremental Change System with diff
- [ ] Template Library
- [ ] Deployment System
- [ ] Enhanced error handling
- [ ] Code streaming with WebSocket

### 📋 Phase 4: Polish & Testing (Planned)
- [ ] Unit and integration tests
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation completion
- [ ] User onboarding flow

## Usage Examples

### 1. Creating a New Project

```typescript
// Start by creating a project from the dashboard
// Click "New Project" button
// Enter project details:
{
  name: "My SaaS App",
  framework: "Next.js",
  project_prompt: "Build a modern SaaS dashboard with user authentication"
}
```

### 2. Enhancing a Prompt

```typescript
// Original prompt
"Build a todo app"

// Click "Enhance Prompt" button
// AI-enhanced result:
"Create a modern, production-ready todo application using Next.js 14:

Architecture:
- Next.js 14 with App Router and Server Components
- TypeScript for type safety
- Tailwind CSS for styling
- shadcn/ui components

Features:
- Add, edit, delete todos
- Mark todos as complete/incomplete
- Filter by status (all, active, completed)
- Local storage persistence
- Responsive design (mobile-first)

Design:
- Clean, modern interface
- Smooth animations
- Accessible (ARIA labels, keyboard nav)
- Dark mode support

Best Practices:
- TypeScript strict mode
- Error handling
- Loading states
- Optimistic UI updates"
```

### 3. Iterative Development

```typescript
// Make specific changes
"Change the button color to blue in the Header component"

// Lock files you don't want to change
// Click lock icon on files in the tree

// AI will only modify the specified files
// Other files remain untouched
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Create an issue on GitHub
- Email: support@example.com

## Acknowledgments

- Built with [Anthropic Claude](https://www.anthropic.com/)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons from [Lucide](https://lucide.dev/)
