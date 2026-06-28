---
name: py-dockerize-service
description: Create Docker files and Compose configurations for a deployable Python application module inside the modular monolith, including Pipenv environment setup.
---

# Python Service Dockerizer (`py-dockerize-service`)

This skill guides the agent in setting up containerization and local environments for deployable Python application modules inside the monorepo.

---

## 1. Interaction Flow

When this skill is activated:
1.  **Ask for Module Target:** Ask the user: *"Which deployable application module (under `src/`) should I containerize?"*
2.  **Scaffold Docker Configurations:** Write the `Dockerfile`, `.dockerignore`, and `.envrc` files.
3.  **Update Compose File:** Integrate the new service container into the root `docker-compose.yml` (or create one if missing).
4.  **Verify Build:** Run a docker build command from the repository root to verify compilation.
5.  **Stage & Push:** Ask the user for permission to stage and commit the configurations.

---

## 2. Scaffolding Templates

### 2.1 Multi-Stage Dockerfile (`src/[module]/Dockerfile`)
*   **Base Image:** Use `python:3.14-slim`.
*   **Builder Stage:** Install `pipenv`, copy `Pipfile` and `Pipfile.lock`, set `ENV PIPENV_VENV_IN_PROJECT=1`, and run `pipenv install --deploy`.
*   **Runtime Stage:** Copy `/app/.venv` from the builder stage, set `ENV PYTHONPATH=/app`, copy the shared `src/common` library, copy the target service package, and expose ports.

### 2.2 Dockerignore (`src/[module]/.dockerignore`)
Ignore local caches and development configs to keep build context clean:
```
.venv/
__pycache__/
*.pyc
.env
.envrc
.pytest_cache/
tests/
```

### 2.3 Compose Configuration (`docker-compose.yml`)
Add the service mapping:
*   Set build context to the repository root (`.`).
*   Point the dockerfile to `src/[module]/Dockerfile`.
*   Add environment variables and map local directories/networks if required.
