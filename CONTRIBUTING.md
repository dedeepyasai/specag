# Contributing to Rootine

Thank you for considering contributing. Rootine is an early-stage open-source project and every contribution matters.

## Ways to Contribute

### 1. Use it and report back

The most valuable contribution right now is **using Rootine on a real project** and telling us what broke, what was confusing, or what you wish existed. Open an issue with:

- What you tried to do
- What happened
- What you expected

### 2. Improve documentation

Found a confusing paragraph? A missing step in the quick start? A broken link? Fix it and open a PR. Documentation PRs are merged fast.

### 3. Add an example project

Build something small with Rootine (a todo app, a CLI tool, an API) and submit it to `examples/`. Include:

- `rootine.config.yaml` with your tier choice
- At least 2-3 specs showing the spec-driven flow
- A README explaining what you built and what tier you used

### 4. Write a custom hook

Implement the `PreCallHook` interface for a use case we haven't covered. Examples:

- A hook that reads blocker status from Jira/Linear instead of a local YAML file
- A hook that enforces different token caps on weekends vs weekdays
- A hook that routes different epic categories to different models

### 5. Contribute a tier profile

If you've customized the tier matrix for your use case (e.g., a "regulated" tier between T3 and T4), submit it as a PR to `templates/`.

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/rootine.git
cd rootine
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

### Code style

```bash
ruff check rootine/
ruff format rootine/
```

## Pull Request Guidelines

1. **One PR per change.** Don't bundle unrelated fixes.
2. **Write a clear description.** What changed, why, and how to test it.
3. **Follow existing patterns.** Read the code around your change before writing new abstractions.
4. **No comments unless the WHY is non-obvious.** Code should be self-documenting.
5. **Test your change.** If you're adding CLI functionality, manually test `rootine <command>`.

## Code of Conduct

Be kind. Be constructive. Focus on the work, not the person. This is a blameless project (see the Bible's retro rules — they apply to contributions too).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
