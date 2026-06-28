---
name: py-create-project
description: Create clean Python projects, domain models, ports, and use cases complying with DDD and BDD.
---

# Clean Python Project Creator (`py-create-project`)

This skill guides the agent in creating and scaffolding a new Python project, bounded context, or vertical feature slice from scratch, driven by a Behavior-Driven Development (BDD) specification.

---

## 1. Initial Interaction Flow

Before generating any files or templates, you **MUST** align on the business scenario to implement:

1.  **Ask for the Use Case:** Explicitly ask the user: *"Please provide the BDD use case (Gherkin format/scenarios) you want me to implement."*
2.  **Iterate for Clarity:** Analyze the user's input against the BDD rules (declarative, single action, concrete data, independent, concise). If the scenario is imperative, unclear, or violating any rules, **propose an updated version and ask for feedback.**
    *   *Constraint:* Repeat this iteration cycle until the Gherkin specification is fully clear, declarative, and approved by the user.

---

## 2. Project Scaffolding Structure

Once approved, scaffold the project according to the **modular monolith** structure under `src/` and `tests/`:

```
├── src/
│   ├── common/                      # Shared package
│   │   └── [domain_subdomain]/
│   │       └── [bounded_context]/
│   │           └── [action]/
│   │               ├── domain/      # Models (dataclasses) & Ports (Protocols)
│   │               ├── application/ # UseCases & Contracts
│   │               └── infrastructure/ # Database, APIs, Settings
│   ├── internal_web/                # Web gateway with Dockerfile
│   └── internal_worker/             # Background workers with Dockerfile
├── tests/                           # Parallel test directory
├── .python-version                  # pyenv configuration (Python 3.14)
├── Pipfile                          # pipenv dependencies (returns, fastapi, pydantic, assertpy, etc.)
├── setup.cfg                        # Tool configurations
├── Makefile                         # automate tasks (setup, tests, lint, clean)
├── .gitignore                       # standard ignores
└── .envrc                           # direnv setup (use pyenv 3.14, layout pipenv)
```

---

## 3. Setup File Verification

Ensure the setup files conform to the templates defined in `py-architecture.md`:
*   Use `python_version = "3.14"` and `python:3.14-slim` base Docker images.
*   Configure `assertpy` in `Pipfile` dev dependencies.
*   Configure `direnv` in `.envrc`.

## 4. Scaffold Execution and Dummy Test (HITL)

Rather than implementing full logic or running TDD cycles, only build the boilerplate architecture skeleton:
1.  **Generate Scaffold:** Create all folders, packages, and files mapped in Section 2, ensuring they are populated with the standard configuration templates defined in the architecture rule.
2.  **Dummy Test:** Place a simple dummy test file at `tests/test_dummy.py` using `assertpy` to verify the testing pipeline is functional:
    ```python
    from assertpy import assert_that

    def test_pipeline_is_functional():
        assert_that(True).is_true()
    ```
3.  **Run Makefile Verification:** Execute `make setup` followed by `make tests` to ensure the environment initializes correctly and the dummy test successfully passes.
4.  **Staging and Push:** Stage all generated files (`git add .`), review diffs to ensure no credentials/secrets are present, and ask the user for permission to push the scaffolded project to the remote repository.
