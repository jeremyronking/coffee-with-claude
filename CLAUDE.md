# Project Instructions

## Git Workflow

- **Always use feature branches** — Never commit directly to `main`.
- **Branch naming convention:**
  - `feature/<description>` — New features
  - `bugfix/<description>` — Bug fixes
  - `hotfix/<description>` — Urgent production fixes
- **Branch from the latest `main`** before starting any work.
- Follow standard Git flow: branch → commit → PR → merge.

## Testing

- **Every new piece of code must have a complementary unit test.**
- Use **pytest** as the test framework.
- Work is **not considered done** until all unit tests pass.
- Run tests with `pytest` before finalizing any change.

## Documentation

- All documentation lives in the `docs/` folder as Markdown files.
- **New features** — Create corresponding documentation in `docs/`.
- **Existing code changes** — Review related documentation and update it to stay current.
- Documentation must accurately reflect the current state of the codebase.

## Python Best Practices

- Follow **PEP 8** for code style and formatting.
- Use **type hints** for function signatures.
- Use **docstrings** (Google style) for modules, classes, and functions.
- Keep functions focused and single-purpose.
- Use meaningful variable and function names.
- Organize imports per PEP 8: standard library, third-party, local.
