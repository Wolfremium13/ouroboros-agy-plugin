# Python Way of Working (py-way-of-working)

Python SDLC/STLC rule: Trunk-Based Development, TDD, conventional commits, and HITL push.

---

## 1. Branching & Git Flow (Trunk-Based Development)

Before writing any code or tests, the developer (agent) must work on a dedicated, short-lived branch.

### Branch Naming Conventions (conventionalbranch.org)
All branch names must follow the format:
`<category>/<kebab-case-description>`

*   **`feature/`**: New feature implementations (e.g., `feature/user-authentication`)
*   **`bugfix/`**: Fixes for bugs found in non-production environments (e.g., `bugfix/token-expiration`)
*   **`hotfix/`**: Quick fixes for production critical issues (e.g., `hotfix/db-connection-leak`)
*   **`docs/`**: Documentation-only changes (e.g., `docs/api-guide`)
*   **`refactor/`**: Code restructuring without changing behavior or adding tests (e.g., `refactor/extract-helper-methods`)
*   **`test/`**: Adding or updating tests without source code changes (e.g., `test/unit-test-suite`)
*   **`chore/`**: Maintenance tasks, dependencies updates, etc. (e.g., `chore/bump-dependencies`)

---

## 2. Commit Message Convention (conventionalcommits.org)

Every commit must follow the Conventional Commits specification.

### Commit Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

*   **`feat`**: A new feature (corresponds to `feature/` branch or parts of it)
*   **`fix`**: A bug fix
*   **`docs`**: Documentation updates
*   **`style`**: Formatting, missing semi-colons, etc.; no production code change
*   **`refactor`**: Code changes that neither fix a bug nor add a feature
*   **`perf`**: A code change that improves performance
*   **`test`**: Adding missing tests or correcting existing tests
*   **`build`**: Changes that affect the build system or external dependencies
*   **`ci`**: Changes to CI configuration files and scripts
*   **`chore`**: Other changes that don't modify src or test files

*Example*: `feat(auth): add JWT validation middleware`

---

## 3. Test-Driven Development (TDD) Lifecycle

Development must strictly proceed in small, iterative steps following the Red-Green-Refactor cycle. No implementation code may be written before a failing test exists.

### Step 1: RED (Write a Failing Test)
1.  Identify the next small unit of functionality to implement.
2.  Write a test in `tests/` targeting the new behavior.
3.  Run the test suite (e.g., `pytest`). **Confirm that the test fails** (and fails for the correct reason).
4.  **Commit the failing test immediately.**
    *   *Commit message*: `test(<scope>): add failing test for <behavior>` (e.g., `test(auth): add failing test for invalid token rejection`).

### Step 2: GREEN (Make the Test Pass)
1.  Write the **minimum viable code** required to make the failing test pass. Do not write ahead or over-engineer.
2.  Run the test suite. **Confirm that all tests, including the new one, are green.**
3.  **Commit the implementation immediately.**
    *   *Commit message*: `feat(<scope>): implement <behavior>` or `fix(<scope>): resolve <behavior>` (e.g., `feat(auth): implement invalid token rejection`).

### Step 3: REFACTOR (Optional)
1.  Review the newly written code and existing code for code smells, duplication, naming improvements, or type-safety enhancements.
2.  Refactor while keeping all tests green. Run the test suite frequently to ensure no regressions.
3.  **Commit each refactoring step immediately.**
    *   *Commit message*: `refactor(<scope>): <description of refactor>` (e.g., `refactor(auth): simplify token verification clause`).

---

## 4. Human-In-The-Loop (HITL) & Push Guardrail

1.  **Do not force push or push directly to remote.**
2.  Once the TDD cycle is completed for the task/feature:
    *   Stage all files: `git add .` (or target specific files).
    *   Check `git status` to ensure only the intended files are staged.
3.  **Ask the human** for permission to push or prompt the human to run the push command.
    *   *Agent Action*: Present a clear summary of the branch created, tests implemented, and commits made, and ask: *"I have staged the changes. Would you like me to push these to the remote repository, or would you prefer to review and push them yourself?"*

---

## 5. Credential & Secret Leak Prevention

1.  **Strictly Prohibited:** Never commit real credentials, access tokens, API keys, passwords, private keys, or sensitive configuration files to the repository.
2.  **Environment Variables:** Always use environment variables or configuration files listed in `.gitignore` (such as `.env`) to load sensitive information.
3.  **Mocking/Dummy Data:** For testing and TDD, use mock objects or dummy strings (e.g., `"fake_api_key_123"`, `"mock_db_password"`) rather than production or live staging values.
4.  **Pre-Staging Review:** Before staging files (`git add`), verify the differences using `git diff` to ensure no keys or secrets are accidentally embedded in the code or tests.

---

## 6. Python-Specific Best Practices & STLC

*   **Local Runtime Environment (pyenv & Linux)**: Projects target Linux environments and use `pyenv` to enforce specific Python runtime versions. Ensure a local `.python-version` file is present at the repository root to automatically manage the correct interpreter version.
*   **Dependency Management**: Always manage project packages using `pipenv` (with `Pipfile` and `Pipfile.lock`).
*   **Virtual Environments**: Run all tests, tools, and commands inside the pipenv environment (e.g., `pipenv run pytest`, `pipenv run ruff`).
*   **Makefile Command Automation**: A `Makefile` must exist in the root of the project to standardize command execution. Always use the following commands rather than raw shell invocations:
    *   `make setup`: Installs development and production dependencies.
    *   `make tests`: Executes the unit and integration test suite.
    *   `make lint`: Checks and formats project code.
    *   `make clean`: Deletes cached directories and removes the virtual environment.
*   **Type Hinting**: Ensure all new Python code includes type annotations.
*   **Formatting/Linting**: Run `make lint` on modified files before committing green/refactored phases.
