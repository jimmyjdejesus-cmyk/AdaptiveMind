# Contributing to AdaptiveMind

Thank you for your interest in contributing to AdaptiveMind! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Security](#security)
- [Communication](#communication)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- UV package manager (recommended) or pip
- Make (optional, for using make commands)

### Quick Start

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/Jarvis_AI.git
   cd Jarvis_AI
   ```

2. **Set up development environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync --dev --all-extras
   ```

3. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

4. **Run initial quality checks**
   ```bash
   ruff check .
   ruff format .
   mypy .
   pytest
   ```

## Development Environment Setup

### Using UV (Recommended)

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync --dev --all-extras

# Activate virtual environment
source .venv/bin/activate
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### IDE Configuration

#### Visual Studio Code

Install recommended extensions:
- Python
- Pylance  
- Ruff
- Black Formatter
- GitLens

Recommended settings (`.vscode/settings.json`):
```json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "none",
    "python.formatting.ruffPath": "ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## Contribution Guidelines

### Types of Contributions

We welcome the following types of contributions:

- **Bug fixes** - Fixing existing issues
- **New features** - Adding new functionality
- **Documentation** - Improving docs, examples, guides
- **Tests** - Adding or improving test coverage
- **Performance** - Optimizing code performance
- **Security** - Improving security aspects
- **Refactoring** - Improving code quality without changing behavior

### Before You Start

1. **Check existing issues** - Look for existing issues related to your planned contribution
2. **Create an issue** - For new features or significant changes, create an issue first
3. **Discuss your approach** - For complex changes, discuss your approach in the issue
4. **Claim the issue** - Comment on the issue to claim it

### Branch Strategy

- **main** - Stable release branch
- **develop** - Integration branch for features
- **feature/description** - Feature branches
- **fix/description** - Bug fix branches
- **security/description** - Security fix branches

### Commit Messages

Follow conventional commits format:

```
type(scope): description

Longer explanation if needed

Breaking changes or other notes
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks
- `security` - Security improvements

**Examples:**
```bash
feat(orchestrator): add new agent routing algorithm
fix(api): resolve timeout issue in chat endpoint
docs(readme): update installation instructions
security(audit): enhance password validation logic
```

## Pull Request Process

### Before Submitting

1. **Update documentation** - Update relevant documentation
2. **Add tests** - Ensure adequate test coverage
3. **Run quality checks** - All quality checks must pass
   ```bash
   ruff check .
   ruff format .
   mypy .
   bandit -r .
   pytest
   ```

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Code is well-commented, particularly in complex areas
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] No new security vulnerabilities
- [ ] Performance impact considered
- [ ] Backward compatibility maintained (or breaking changes documented)

### PR Template

Use the provided PR template and fill out all sections:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
```

### Review Process

1. **Automated checks** - CI/CD must pass all checks
2. **Code review** - At least one maintainer review required
3. **Testing** - Manual testing may be required for complex changes
4. **Security review** - Required for security-sensitive changes

## Coding Standards

### Code Quality

- Follow [DEVELOPMENT_STANDARDS.md](DEVELOPMENT_STANDARDS.md) for detailed standards
- Use Ruff for formatting and linting
- Maintain MyPy type hints
- Keep cyclomatic complexity under 10
- Use meaningful variable and function names

### Style Guidelines

- **PEP 8** - Follow Python style guidelines
- **Google Style Docstrings** - Use for all public APIs
- **Type Hints** - Use for function parameters and return values
- **Line Length** - Maximum 88 characters (Ruff default)
- **Imports** - Use isort for import organization

### Documentation

- Document all public APIs
- Include docstrings for functions, classes, and modules
- Add type hints where possible
- Update relevant documentation when making changes

## Testing Requirements

### Test Categories

1. **Unit Tests** - Test individual functions and classes
2. **Integration Tests** - Test component interactions
3. **Contract Tests** - Test API compatibility
4. **Security Tests** - Test security controls

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=adaptivemind --cov-report=html

# Run specific test categories
pytest -m "not slow"          # Skip slow tests
pytest -m "integration"       # Run only integration tests
pytest -m "security"          # Run only security tests

# Run specific test file
pytest tests/test_orchestrator.py
```

### Test Coverage

- **Minimum coverage**: 80% for new code
- **Critical path coverage**: 95% for security-critical functions
- **All new features** must include tests
- **Bug fixes** should include regression tests

### Writing Tests

- Use descriptive test names
- Follow Arrange-Act-Assert pattern
- Mock external dependencies
- Test edge cases and error conditions
- Use fixtures for common setup

## Documentation

### Required Documentation

1. **Code Documentation**
   - Docstrings for all public APIs
   - Inline comments for complex logic
   - Type hints for function signatures

2. **User Documentation**
   - README updates for new features
   - API documentation
   - Usage examples

3. **Developer Documentation**
   - Architecture decisions
   - Setup instructions
   - Development guidelines

### Documentation Standards

- Use clear, concise language
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Use proper Markdown formatting

## Security

### Security Guidelines

- **No hardcoded secrets** - Use environment variables
- **Input validation** - Validate all user inputs
- **SQL injection prevention** - Use parameterized queries
- **XSS prevention** - Sanitize HTML output
- **HTTPS everywhere** - Never use plain HTTP for sensitive data

### Reporting Security Issues

- **Do not** create public issues for security vulnerabilities
- **Do** report security issues privately via email or private issue
- **Include** detailed description and steps to reproduce
- **Allow** reasonable time for response before public disclosure

### Security Review

- All security-related changes require review
- Use security scanning tools (Bandit, Safety)
- Test security controls thoroughly
- Follow security best practices

## Communication

### Where to Get Help

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and general discussion
- **Email** - For security issues or private matters

### Response Times

- **Issues**: 1-3 business days for initial response
- **Security**: 24-48 hours for acknowledgment
- **Reviews**: 3-5 business days for PR reviews

### Getting Help

If you need help:

1. Check existing documentation
2. Search existing issues
3. Create a new issue with detailed description
4. Tag appropriately for faster response

## Recognition

Contributors who make significant contributions will be recognized:

- **Contributors list** in README.md
- **Release notes** acknowledgment
- **Special mentions** for major contributions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (CC BY 4.0).

## Questions?

If you have questions about contributing, please:

1. Check this document and other documentation
2. Search existing issues
3. Create a new issue with your question
4. Contact the maintainers

Thank you for contributing to AdaptiveMind!

---

**Last Updated**: 2025-12-18  
**Maintained By**: AdaptiveMind Development Team
