---
name: py-create-module
description: Create a new bounded context slice or deployable service inside an existing Python monorepo.
---

# Python Monorepo Module Scaffolder (`py-create-module`)

This skill guides the agent in adding a new module—either a new domain bounded context slice under `src/common/` or a new deployable application under `src/`—inside an existing Python modular monolith/monorepo project.

---

## 1. Initial Interaction Flow

Before creating any folders or files, align on the business logic:

1.  **Ask for the Use Case:** Explicitly ask the user: *"Please provide the BDD use case (Gherkin format/scenarios) for the new module."*
2.  **Iterate for Clarity:** Analyze the use case against the BDD rules in `py-bdd.md`. If it lacks clarity or is imperatively written, **propose an updated version and ask for feedback.**
    *   *Constraint:* Do not proceed to scaffolding until the Gherkin specification is approved by the user.

---

## 2. Scaffolding Options

Identify the type of module the user wants to add:

### Option A: Bounded Context / Vertical Feature Slice
Create a new feature slice inside the shared library `src/common/`:

```
src/common/[domain_subdomain]/[bounded_context]/[action]/
├── domain/
│   ├── models/            # Entity models and Value Objects (dataclasses)
│   └── ports/             # Domain repository and publisher ports (Protocols/ABCs)
├── application/
│   ├── contracts/         # Use case interfaces and associated commands (dataclasses)
│   └── use_cases/         # Workflow handlers (monadic pipelines returning Result)
└── infrastructure/        # Framework implementations (database repositories, HTTP clients)
```

Create a parallel testing structure under `tests/common/`:
```
tests/common/[domain_subdomain]/[bounded_context]/[action]/
├── domain/
│   ├── test_models.py     # Simple unit test using assertpy
│   └── builders/          # Test data builders
└── application/
    └── test_use_cases.py  # Dummy use case test mocking ports
```

### Option B: Deployable Application Module
Create a new standalone application/service at the root of `src/` (e.g. `src/internal_analytics/`):

```
src/[module_name]/
├── routes/                # Endpoint routes
├── consumers/             # Message brokers / event consumers
├── Dockerfile             # Multi-stage Docker setup (Python 3.14 + Pipenv)
└── main.py                # Service entry point and DI configuration
```

Create a parallel testing structure under `tests/[module_name]/`.

---

## 3. Implementation Workflow

1.  **Scaffold Skeleton:** Create the folders and placeholder python files (e.g., contract protocols, model dataclasses, and dummy handlers).
2.  **Dummy Test:** Implement a simple dummy test file in the newly created test directory verifying that the module skeleton is discoverable and executable (using `assertpy`).
3.  **Verify Setup:** Execute `make tests` to ensure the new tests are detected and pass.
4.  **Staging and Push:** Stage files (`git add .`), review diffs to ensure no credentials or secrets are present, and ask the user for permission to push to the remote repository.
