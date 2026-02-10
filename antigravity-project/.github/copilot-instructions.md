# GitHub Copilot Instructions

## Project Context

This project uses **linux** as its core technology stack. All code should follow the conventions and patterns established in the existing codebase.

## Development Workflow

### Before Making Changes
1. Check `docs/imported/` for project-specific documentation
2. Review `context/raw/` for original specifications
3. Consult `.agent/rules/` for coding standards and conventions
4. Read `CONTRIBUTING.md` for contribution guidelines

### Testing
```bash
# Run tests before committing
# [Add your test command here]
```

### Code Quality
```bash
# Lint and format code
# [Add your linting commands here]
```

## Project-Specific Patterns

### File Organization
- Source code: `src/`
- Tests: `tests/`
- Documentation: `docs/`
- Configuration: Root directory

### Coding Standards
1. **Security First**: Never commit secrets, API keys, or credentials
   - Use `.env` for environment variables
   - Reference `.env.example` for required variables
2. **Type Safety**: Use type hints/annotations where applicable
3. **Error Handling**: Always validate inputs and handle edge cases
4. **Documentation**: Add comments for complex logic

### Commit Conventions
Use [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/updates
- `chore:` Maintenance tasks

**Examples:**
```
feat: add user authentication
fix: resolve memory leak in data processor
docs: update API documentation
```

## Common Tasks

### Adding a New Feature
1. Create a feature branch: `git checkout -b feat/feature-name`
2. Review related files in `src/` for patterns
3. Write tests first (TDD approach recommended)
4. Implement the feature
5. Run tests and linting
6. Commit with conventional commit message

### Fixing a Bug
1. Reproduce the bug with a failing test
2. Review `SECURITY.md` if security-related
3. Fix the issue
4. Verify all tests pass
5. Document the fix in `CHANGELOG.md`

### Refactoring Code
1. Ensure all tests pass before starting
2. Make incremental changes
3. Run tests after each change
4. Update documentation if public APIs change

## Integration Points

### Environment Variables
Required variables are documented in `.env.example`. Never hardcode:
- API keys
- Database credentials
- Service endpoints
- Secret tokens

### External Dependencies
- Review existing dependencies before adding new ones
- Prefer stable, well-maintained packages
- Document why each dependency is needed

## AI Agent Workflows

This project includes AI agent workflows in `.agent/workflows/`. Use these commands:

- `/plan` - Generate project plan from specifications
- `/bootstrap` - Create initial code structure
- `/review` - Audit code for security and quality
- `/commit` - Generate conventional commit messages
- `/save` - Update project memory/scratchpad

## Key Files Reference

- [README.md](README.md) - Project overview and setup
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](SECURITY.md) - Security policies
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [.env.example](.env.example) - Environment configuration

## Quick Tips

1. **Read First, Code Second**: Always check existing patterns before writing new code
2. **Test Coverage Matters**: Aim for comprehensive test coverage
3. **Security is Paramount**: When in doubt, ask before handling sensitive data
4. **Document Decisions**: Use comments to explain "why", not "what"
5. **Follow the Stack**: Stick to linux unless discussing alternatives
