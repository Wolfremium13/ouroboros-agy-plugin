---
name: py-scaffold-tests
description: Automatically generate pytest, Hypothesis, and assertpy unit test templates and test data builders for domain models, value objects, and use cases.
---

# Python Test Template Scaffolder (`py-scaffold-tests`)

This skill guides the agent in generating unit and property-based test files conforming to the testing guidelines in `py-testing.md`.

---

## 1. Interaction Flow

When this skill is activated:
1.  **Ask for the Target Component:** Ask the user: *"Which Python file or class (Entity, Value Object, or Use Case) should I generate tests for?"*
2.  **Determine the Testing Layer:** Analyze the target class to categorize it (Value Object, Domain Entity/Aggregate, or Application Use Case).
3.  **Generate Test Skeletons:** Write the corresponding test files and test data builders using `assertpy` and `pytest`.
4.  **Verify:** Run `make tests` to ensure the scaffolded tests execute.

---

## 2. Scaffolding Blueprints

Based on the target category, scaffold the following structures:

### 2.1 Value Object Tests
Scaffold a test module in `tests/` verifying boundaries:
*   A success path test asserting that the factory method returns a `Success` monad containing the expected Value Object.
*   A parameterized test using `@pytest.mark.parametrize` testing invalid boundary inputs, verifying that they return a monadic `Failure` wrapping the expected exception class.
*   *Assertion style:* Always use `assertpy`'s `assert_that`.

### 2.2 Test Data Builders
For complex entities or aggregates, generate a Test Data Builder class to decouple tests from object constructors:
*   Includes fluent `with_[attribute]` chainable setter methods.
*   Includes a `build()` method that executes the classmethod factory and returns the entity (raising a ValueError inside the builder if construction fails).

### 2.3 Use Case Mocking Tests
Scaffold a mock-based test verifying orchestration behavior:
*   Use `unittest.mock.Mock` or `pytest-mock` fixtures to fake ports and dependency interfaces (Protocols).
*   Specify success/failure monadic return values for mocked ports.
*   Assert the resulting output using `assertpy`.
*   Verify call counts and arguments using `mock_port.assert_called_once_with(...)` or `mock_port.assert_not_called()`.

### 2.4 Property-Based & Documentation Tests
*   **Hypothesis Property Test:** Add a test case decorated with `@given` and appropriate strategies (e.g. `text()`, `integers()`) to test class properties against generalized bounds.
*   **Doctest example:** If the target is a pure function, add interactive shell examples (using `>>>`) inside its docstring.
