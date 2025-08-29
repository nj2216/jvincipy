# Contributing to jvincipy

Thanks for your interest in contributing! This document describes a simple, low-friction workflow to help your changes get reviewed and merged quickly.

## Getting started

1. Fork the repository and create a branch for your changes:
   ```bash
   git checkout -b feature/my-feature
   ```
2. Install development dependencies and run tests (optional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -U pytest
   ```
3. Make your changes, add tests, and run the tests:
   ```bash
   pytest
   ```

## Code style

- Keep the code clear and idiomatic Python 3.10+.
- Prefer small, focused commits with descriptive messages.
- Write tests for new features and bug fixes where possible.
- Keep public API backwards-compatible unless there is a compelling reason and clear migration notes.

## Pull requests

- Open a Pull Request against the `main` branch of the upstream repository.
- Describe the problem you're solving and include example usage where appropriate.
- Link to any relevant issues or discussions.
- Use a clear title and include tests where applicable.

## Issues

- Use issues to report bugs or request features.
- Provide a clear, minimal reproduction when reporting bugs (a small code sample is ideal).

## Security

If you discover a security vulnerability, please **do not** open a public issue. Instead, email the maintainers directly (replace with your contact) or use the repository's security reporting mechanism.

## License

By contributing to this repository, you agree that your contributions will be licensed under the project's MIT License.
