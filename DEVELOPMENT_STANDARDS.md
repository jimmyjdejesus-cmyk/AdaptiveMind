# Development Standards for AdaptiveMind

## Overview

This document outlines the development standards, practices, and tooling for the AdaptiveMind project. These standards ensure code quality, security, maintainability, and consistency across the codebase.

## Code Quality Standards

### Code Formatting & Linting

- **Primary Tool**: [Ruff](https://github.com/astral-sh/ruff) - A fast Python linter and formatter
- **Configuration**: See `ruff.toml` for detailed rules
- **Type Checking**: [MyPy](https://github.com/python/mypy) with configuration in `mypy.ini`

#### Running Code Quality Checks

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Type checking
mypy .
```

### Code Quality Rules

#### Essential Rules Enabled
- **E, W**: Pycodestyle errors and warnings
- **F**: Pyflakes for import and name analysis
- **I**: isort for import sorting
- **N**: PEP8 naming conventions
- **D**: Pydocstyle for docstring validation
- **UP**: Pyupgrade for modern Python features
- **B**: Flake8-bugbear for common Python mistakes
- **S**: Security rules (Bandit integration)
- **SIM**: Flake8-simplify for code simplification

#### Documentation Standards
- Google-style docstrings required for public APIs
- Comprehensive docstring coverage (>80%)
- Type hints encouraged for public functions and classes

## Security Standards

### Security Scanning

- **Primary Tool**: [Bandit](https://github.com/PyCQA/bandit) for static security analysis
- **Configuration**: See `.bandit` for security rules
- **Dependency Scanning**: Safety for known vulnerability detection

#### Running Security Scans

```bash
# Security scanning
bandit -r . -f json

# Dependency vulnerability check
safety check
```

### Security Best Practices

1. **No hardcoded secrets** - Use environment variables or secure configuration
2. **Input validation** - Validate all user inputs
3. **SQL injection prevention** - Use parameterized queries
4. **XSS prevention** - Sanitize HTML output
5. **HTTPS everywhere** - Never use plain HTTP for sensitive data

## Testing Standards

### Testing Framework

- **Framework**: [pytest](https://pytest.org/)
- **Configuration**: `pytest.ini` and `pyproject.toml`

### Test Categories

1. **Unit Tests** - Test individual functions and classes
2. **Integration Tests** - Test component interactions
3. **Contract Tests** - Test API compatibility
4. **Security Tests** - Test security controls

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=adaptivemind --cov-report=html

# Run specific test categories
pytest -m "not slow"          # Skip slow tests
pytest -m "integration"       # Run only integration tests
pytest -m "security"          # Run only security tests
```

### Test Coverage Requirements

- **Minimum Coverage**: 80% for new code
- **Critical Path Coverage**: 95% for security-critical functions
- **Documentation**: All public APIs must have tests

## Git Workflow & Commit Standards

### Pre-commit Hooks

- **Tool**: [pre-commit](https://pre-commit.com/)
- **Configuration**: `.pre-commit-config.yaml`
- **Enforced Checks**: Code formatting, linting, security scanning, tests

#### Setup Pre-commit

```bash
# Install pre-commit hooks
pre-commit install

# Run on all files (first time setup)
pre-commit run --all-files
```

### Commit Message Format

```
type(scope): description

Longer explanation if needed

Breaking changes or other notes
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `security`: Security improvements

**Examples**:
```
feat(orchestrator): add new agent routing algorithm
fix(api): resolve timeout issue in chat endpoint
docs(readme): update installation instructions
security(audit): enhance password validation logic
```

## Documentation Standards

### Required Documentation

1. **README.md** - Project overview and quick start
2. **CONTRIBUTING.md** - Contribution guidelines
3. **API Documentation** - OpenAPI/Swagger specs
4. **Architecture Documentation** - System design
5. **Security Policy** - Vulnerability reporting process

### Documentation Tools

- **MarkdownLint** - Markdown formatting validation
- **Interrogate** - Docstring coverage analysis
- **Markdownlint-CLI** - Command-line Markdown linting

## Dependency Management

### Package Management

- **Primary Tool**: [UV](https://github.com/astral-sh/uv) for dependency management
- **Configuration**: `pyproject.toml` and `requirements.txt`
- **Version Pinning**: Use ranges for dependencies, exact versions for development tools

### Dependency Security

- **Regular Updates**: Monthly dependency audits
- **Vulnerability Scanning**: Automated with Safety
- **License Compliance**: Ensure all dependencies have compatible licenses

## Performance Standards

### Code Complexity

- **Cyclomatic Complexity**: Maximum 10 per function
- **Cognitive Complexity**: Maximum 15 per function
- **Tool**: Radon for complexity analysis

#### Running Complexity Analysis

```bash
# Analyze code complexity
radon cc . --min=B

# Generate complexity report
radon cc . --json > complexity_report.json
```

### Performance Monitoring

- **Response Time**: < 100ms for API endpoints (95th percentile)
- **Memory Usage**: Monitor for memory leaks
- **CPU Usage**: Profile hot paths

## Code Review Standards

### Review Checklist

1. **Functionality** - Code works as intended
2. **Security** - No security vulnerabilities introduced
3. **Performance** - No performance regressions
4. **Testing** - Adequate test coverage
5. **Documentation** - Code is well-documented
6. **Style** - Follows project style guidelines
7. **Complexity** - Code is not overly complex

### Reviewer Responsibilities

- **Primary Reviewer**: Domain expert for the affected area
- **Security Reviewer**: For security-sensitive changes
- **Performance Reviewer**: For performance-critical changes

## Continuous Integration

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

1. **Code Quality** - Ruff linting and formatting
2. **Security Scanning** - Bandit security analysis
3. **Testing** - Full test suite execution
4. **Coverage** - Code coverage reporting
5. **Documentation** - Documentation validation

### Quality Gates

- **All tests must pass**
- **Code coverage must not decrease**
- **No security vulnerabilities**
- **Code quality checks must pass**
- **Documentation must be updated**

## IDE Configuration

### Recommended VS Code Extensions

- **Python** - Microsoft Python extension
- **Pylance** - Language server for better IntelliSense
- **Ruff** - Ruff integration for VS Code
- **Black Formatter** - Code formatting
- **GitLens** - Enhanced Git capabilities

### IDE Settings

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

## Environment Setup

### Development Environment

```bash
# Clone repository
git clone <repository-url>
cd Jarvis_AI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv sync --dev --all-extras

# Install pre-commit hooks
pre-commit install

# Run quality checks
ruff check .
ruff format .
mypy .
pytest
```

## Monitoring & Metrics

### Code Quality Metrics

- **Test Coverage**: Tracked in CI/CD
- **Complexity**: Monitored with Radon
- **Security**: Scanned with Bandit and Safety
- **Documentation**: Coverage tracked with Interrogate

### Performance Metrics

- **API Response Times**: Monitored in production
- **Memory Usage**: Tracked for memory leaks
- **Error Rates**: Monitored for stability

## Enforcement

### Automated Enforcement

- **Pre-commit hooks** - Block commits with quality issues
- **CI/CD pipeline** - Block merges with failing checks
- **Code coverage** - Block merges that reduce coverage
- **Security scans** - Block merges with vulnerabilities

### Manual Review

- **Architecture changes** - Require design review
- **Security changes** - Require security team review
- **Breaking changes** - Require major version consideration

## Resources

- [Python PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Security Best Practices](https://python-security.readthedocs.io/)
- [Testing Best Practices](https://docs.pytest.org/)
- [Git Flow Workflow](https://nvie.com/posts/a-successful-git-branching-model/)

---

**Last Updated**: 2025-12-18  
**Maintained By**: AdaptiveMind Development Team  
**Contact**: Create an issue for questions about these standards
