# Contributing to AI App Builder

Thank you for your interest in contributing to the AI App Builder! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Create an issue** with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach
   - Any relevant examples or mockups

### Pull Requests

1. **Fork the repository** and create a new branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test your changes** thoroughly

4. **Commit your changes** with clear messages
   ```bash
   git commit -m "feat: add prompt enhancement caching"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** with:
   - Description of changes
   - Link to related issues
   - Screenshots/videos if UI changes
   - Test coverage information

## Development Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

Quick start:
```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ai-app-builder.git
cd ai-app-builder

# Start with Docker
docker-compose up -d

# Or set up locally (see SETUP.md)
```

## Coding Standards

### TypeScript/JavaScript (Frontend)

- Use TypeScript strict mode
- Follow ESLint rules
- Use Prettier for formatting
- Prefer functional components with hooks
- Use meaningful variable names
- Add JSDoc comments for complex logic

Example:
```typescript
/**
 * Enhances a user prompt with AI-generated details
 * @param prompt - The original user prompt
 * @returns Enhanced prompt with additional context
 */
async function enhancePrompt(prompt: string): Promise<string> {
  // Implementation
}
```

### Python (Backend)

- Follow PEP 8 style guide
- Use Black for formatting
- Use type hints
- Add docstrings for functions and classes
- Keep functions focused and small

Example:
```python
async def enhance_prompt(user_prompt: str) -> str:
    """
    Enhance user prompt with AI.

    Args:
        user_prompt: The original user prompt

    Returns:
        Enhanced prompt with additional context

    Raises:
        HTTPException: If API call fails
    """
    # Implementation
```

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```bash
feat: add prompt enhancement modal
fix: resolve Monaco editor crash on file switch
docs: update setup instructions for Docker
refactor: extract AI service logic into separate module
test: add unit tests for prompt enhancement
```

## Project Structure

### Frontend (`/frontend`)

```
frontend/
├── app/                    # Next.js app directory
│   ├── dashboard/         # Dashboard pages
│   ├── templates/         # Template library pages
│   └── layout.tsx         # Root layout
├── components/
│   ├── chat/             # Chat interface components
│   ├── editor/           # Code editor components
│   ├── templates/        # Template components
│   └── ui/               # Reusable UI components
└── lib/                  # Utilities and helpers
```

### Backend (`/backend`)

```
backend/
├── app/
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core configuration
│   ├── db/               # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── services/         # Business logic
└── main.py               # Application entry point
```

## Testing

### Frontend Tests

```bash
cd frontend
npm test
npm run test:watch
npm run test:coverage
```

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/
pytest -v tests/test_prompts.py
```

### Writing Tests

**Frontend (Jest + React Testing Library)**
```typescript
import { render, screen } from '@testing-library/react';
import { PromptInput } from './PromptInput';

describe('PromptInput', () => {
  it('renders input field', () => {
    render(<PromptInput onSend={jest.fn()} />);
    expect(screen.getByPlaceholderText(/describe what you want/i)).toBeInTheDocument();
  });
});
```

**Backend (pytest)**
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_enhance_prompt():
    response = client.post(
        "/api/prompts/enhance",
        json={"prompt": "Build a todo app"}
    )
    assert response.status_code == 200
    assert "enhanced" in response.json()
```

## Database Migrations

When changing models:

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "add new field to project"

# Review generated migration
# Edit if needed in alembic/versions/

# Apply migration
alembic upgrade head

# Test rollback
alembic downgrade -1
alembic upgrade head
```

## Documentation

### Code Documentation

- Add JSDoc/docstrings for public APIs
- Include parameter descriptions and return types
- Document complex logic with inline comments
- Update README.md when adding features

### API Documentation

FastAPI automatically generates docs at `/docs`. Ensure:
- All endpoints have descriptions
- Request/response models are properly typed
- Examples are provided for complex endpoints

## Review Process

1. **Automated checks** must pass:
   - Linting
   - Type checking
   - Tests
   - Build

2. **Code review** by maintainers:
   - Code quality and style
   - Test coverage
   - Documentation
   - Performance considerations

3. **Changes requested** if needed:
   - Address all feedback
   - Update PR description if scope changes

4. **Merge** once approved:
   - Squash and merge for clean history
   - Delete branch after merge

## Priority Areas

We're especially interested in contributions for:

### High Priority
- [ ] Authentication system implementation
- [ ] Real-time code streaming
- [ ] Incremental change system with diff
- [ ] Template library expansion
- [ ] Test coverage improvement

### Medium Priority
- [ ] Deployment system (Vercel integration)
- [ ] Performance optimizations
- [ ] Error handling improvements
- [ ] UI/UX enhancements

### Low Priority
- [ ] Additional AI model support
- [ ] Alternative database support
- [ ] Internationalization (i18n)

## Questions?

- **General questions**: Create a GitHub Discussion
- **Bug reports**: Create an Issue
- **Security concerns**: Email security@example.com
- **Chat**: Join our Discord (link in README)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in commit history

Thank you for contributing to AI App Builder! 🎉
