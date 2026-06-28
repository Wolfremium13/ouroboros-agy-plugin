# 🐍 Ouroboros Antigravity Plugin

![Ouroboros Banner](_docs/ouroboros_banner_ascii.png)

This repository contains **Ouroboros**, a specialized Google Antigravity (AGY) plugin designed to enforce and automate high-quality, standardized Python development workflows.

---

## 1. Plugin Purpose

Ouroboros establishes a rigorous Software Development Life Cycle (SDLC) and Software Testing Life Cycle (STLC) for Python projects. It equips AI agents with the rules, skills, and execution hooks necessary to build clean, testable, and secure modular monoliths or monorepos on Linux using `pyenv` and `pipenv`.

---

## 2. Overview of Features

The plugin is structured into three core components: Rules, Skills, and Lifecycle Hooks.

### 2.1 Project Rules (`rules/`)
*   **[py-way-of-working.md](rules/py-way-of-working.md):** Defines Git flow, branch naming (`conventionalbranch.org`), commit messages (`conventionalcommits.org`), strict TDD cycles (Red-Green-Refactor), security guidelines, and task automation.
*   **[py-architecture.md](rules/py-architecture.md):** Establishes the directory structure (`src/` and `tests/`), clean architecture layers, dependency direction boundaries, absolute imports, containerization (multi-stage Pipenv Dockerfiles), and templates for configuration files (Makefile, Pipfile, setup.cfg, .gitignore, .envrc).
*   **[py-coding-style.md](rules/py-coding-style.md):** Enforces PEP 8, strict type hints, explicit method overrides (`@typing.override`), naming conventions (no `I` prefixes on interfaces), and modern Python 3.11–3.14 features.
*   **[py-domain-driven-design.md](rules/py-domain-driven-design.md):** Guides Domain-Driven Design (DDD) encapsulation, factory method initialization, aggregates, value objects, and transactional outbox patterns.
*   **[py-bdd.md](rules/py-bdd.md):** Sets rules for writing declarative, concise, and independent Gherkin/BDD scenarios.
*   **[py-testing.md](rules/py-testing.md):** Defines test structures using `pytest`, fluent assertions with `assertpy`, property-based tests via `Hypothesis`, and mock usage.

### 2.2 Specialized Skills (`skills/`)
*   **`py-add-comments`:** Automatically documents classes and public methods using Sphinx Napoleon Google Style docstrings.
*   **`py-create-project`:** Scaffolds a new modular monolith repository structure populated with all configuration files and a pipeline-verifying dummy test.
*   **`py-create-module`:** Adds a new vertical bounded context slice or deployable service skeleton to an existing project.
*   **`py-dockerize-service`:** Generates multi-stage Pipenv Dockerfiles and Compose configurations for a service.
*   **`py-normalize-project`:** Automatically refactor, format, and normalize Python/C# files to conform to conventions.
*   **`py-scaffold-bdd`:** Automatically generates Python step definitions from Gherkin feature files.
*   **`py-scaffold-tests`:** Generates pytest, Hypothesis, and assertpy unit test templates and builders.


### 2.3 Automated Safety Gates & Utility Commands (`hooks.json` & `scripts/`)
Contains automation hooks and code generation commands:
*   **[precommit_security_check.py](scripts/precommit_security_check.py):** Scans staged code changes to prevent hardcoded passwords, tokens, API keys, or private credential files from leaking into Git history.
*   **[lint_compliance_check.py](scripts/lint_compliance_check.py):** Prevents commits containing C#-style Hungarian notation (`class IUserRepository`), Arrange/Act/Assert comments in tests, or layer dependency violations.
*   **[create_value_object.py](scripts/create_value_object.py):** Command line utility to automatically scaffold fully-encapsulated monadic Domain Value Objects and their unit tests.


---

## 3. References

To learn more about configuring, installing, and managing hooks and plugins in Google Antigravity, refer to the official documentation:
*   [Antigravity CLI Plugins & Hooks Documentation](https://antigravity.google/docs/cli/plugins)
