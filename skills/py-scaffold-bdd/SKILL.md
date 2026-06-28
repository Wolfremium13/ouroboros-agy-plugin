---
name: py-scaffold-bdd
description: Generate Python step definitions from Gherkin feature files, connected to use case contracts.
---

# Python BDD Step Scaffolder (`py-scaffold-bdd`)

This skill guides the agent in translating a Gherkin feature file into executable step definitions in Python, ensuring alignment with the project's architecture layers.

---

## 1. Interaction Flow

When this skill is activated:
1.  **Ask for Feature File:** Ask the user: *"Which Gherkin feature file (`.feature`) should I generate step definitions for?"*
2.  **Verify Feature File:** Verify that the feature file complies with the declarative BDD rules in `py-bdd.md`. If it is imperatively defined, iterate with the user to refine it first.
3.  **Generate Step Skeletons:** Write the step definition module (typically using `pytest-bdd` decorators).
4.  **Confirm Execution:** Run `make tests` to ensure the new step definitions are successfully registered.

---

## 2. Step Generation Guidelines

Ensure step definitions adhere to these structural constraints:

*   **No Technical Jargon in Step Signatures:** Maintain Gherkin step names representing purely domain-focused events and conditions.
*   **Direct Application Injection:** In step definitions:
    *   Initialize command or request DTOs (e.g. `RegisterUserCommand`) inside `Given` or `When` steps using test data builders.
    *   Invoke the application layer use case contract (e.g., calling `use_case.register(command)`) inside the `When` step.
    *   Capture the monadic `Result` outcome and store it in a test state context (such as a pytest fixture context).
*   **Decoupled assertions:** In `Then` steps, use `assertpy` to check the success/failure values stored in the test context.
*   **Use Fixtures for State:** In `pytest-bdd`, pass parameters using pytest fixtures rather than global variables to guarantee test independence.
