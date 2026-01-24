# Contributing to Antigravity Architect

## Getting Started
1. **Clone the repo.**
2. **Install Dev Dependencies:**
   ```bash
   pip install -e .[dev]
   ```
3. **Run the Test Suite:**
   ```bash
   pytest tests/
   ```

## Development Workflow
This project adheres to **"Agent-First"** principles.
1. **Code Style:** We use `ruff` and `black`.
   ```bash
   ruff check .
   black .
   ```
2. **Type Safety:** We use `mypy`.
   ```bash
   mypy antigravity_master_setup.py --ignore-missing-imports
   ```
3. **Single File Rule:**
   - All logic MUST remain in `antigravity_master_setup.py`.
   - **NO external dependencies** (standard library only).
   - If adding a feature, add it as a function or class within the master script.

## Commit Guidelines
- Use [Conventional Commits](https://www.conventionalcommits.org/).
- Example: `feat: added new python 3.14 support`
