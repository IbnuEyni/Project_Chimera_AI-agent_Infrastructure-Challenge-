# Contributing to Project Chimera

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd 10AcademyWeek0phase2
   ```

2. **Environment Setup**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure Environment**
   ```bash
   cp .env.template .env
   # Edit .env with your API keys and configuration
   ```

4. **Install Development Dependencies**
   ```bash
   make install-dev
   ```

5. **Setup Pre-commit Hooks**
   ```bash
   make setup
   ```

## Development Workflow

### Daily Development
```bash
make daily          # Pull latest, install deps, run quality checks
make commit-daily    # Make daily commit (required)
```

### Code Quality
```bash
make format         # Format code with black and isort
make lint          # Run linting checks
make type-check    # Run mypy type checking
make security      # Run security scans
make quality       # Run all quality checks
```

### Testing
```bash
make test          # Run unit tests
make test-integration  # Run integration tests
make test-e2e      # Run end-to-end tests
make test-all      # Run all tests
make test-cov      # Run tests with coverage
```

### Documentation
```bash
make docs          # Build documentation
make docs-serve    # Serve docs locally
```

## Code Standards

### Python Style
- Use Black for formatting (line length: 88)
- Use isort for import sorting
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for all public methods

### Commit Messages
Follow conventional commits format:
```
type(scope): description

feat(agents): add new planner agent capability
fix(security): resolve prompt injection vulnerability
docs(readme): update installation instructions
```

### Testing Requirements
- Minimum 80% code coverage
- Unit tests for all new functionality
- Integration tests for API endpoints
- End-to-end tests for critical workflows

### Security Guidelines
- Never commit API keys or secrets
- Use environment variables for configuration
- Validate all inputs
- Follow zero-trust architecture principles
- Regular security scans with bandit and safety

## Architecture Guidelines

### Module Structure
```
src/chimera/
├── core/           # Core swarm coordination
├── agents/         # Agent implementations
├── mcp/           # MCP integration layer
├── security/      # Security framework
├── commerce/      # Economic sovereignty
└── utils/         # Shared utilities
```

### Design Principles
1. **Modularity**: Each component should be independently testable
2. **Scalability**: Design for 10,000+ concurrent agents
3. **Security**: Zero-trust architecture throughout
4. **Observability**: Comprehensive logging and monitoring
5. **Economic Agency**: Agents as economic participants

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Develop and Test**
   ```bash
   make quality
   make test-all
   ```

3. **Update Documentation**
   - Update relevant docstrings
   - Add/update tests
   - Update README if needed

4. **Submit Pull Request**
   - Clear description of changes
   - Link to related issues
   - Include test results
   - Request review from maintainers

## Issue Reporting

### Bug Reports
Include:
- Environment details (OS, Python version)
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs
- Minimal code example

### Feature Requests
Include:
- Clear use case description
- Proposed implementation approach
- Impact on existing functionality
- Alternative solutions considered

## Release Process

1. **Version Bump**
   ```bash
   # Update version in src/chimera/__init__.py
   # Update CHANGELOG.md
   ```

2. **Quality Assurance**
   ```bash
   make ci  # Run full CI pipeline
   ```

3. **Create Release**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

## Getting Help

- **Documentation**: Check docs/ directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Security**: Email security@10academy.org for security issues

## License

By contributing to Project Chimera, you agree that your contributions will be licensed under the MIT License.