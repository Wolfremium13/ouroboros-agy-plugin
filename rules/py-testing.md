# Python Testing Patterns & Guidelines

This document outlines the testing strategy, tools, and patterns implemented to ensure correctness and stability of Python domain models, use cases, and workflows.

---

## 1. Testing Stack & Libraries

The testing strategy focuses on isolated, fast-running unit tests and integration tests using:
- **`pytest`**: The standard test runner and structural framework.
- **`assertpy`**: Fluent, natural-language assertions (e.g., `assert_that(value).is_equal_to(expected)`).
- **`unittest.mock`**: Clean, standard mocking framework for faking external dependencies and interfaces.
- **`Hypothesis`**: Property-based testing library for automated boundary data generation.
- **`doctest`**: Python's built-in module for executing examples inside docstrings.

### Crucial Constraints
- **No Comments in Tests**: Do not write comments in unit tests or integration tests to label sections (such as `# Arrange`, `# Act`, or `# Assert`). Instead, separate these logical phases strictly using vertical whitespace (empty lines).

---

## 2. TDD Heuristics and Best Practices

TDD in Python is driven by the iterative **Red-Green-Refactor** cycle: write a failing test (Red), implement the minimum code to pass (Green), and improve the design (Refactor).

*   **The FIRST Principle**: Tests must be **F**ast, **I**ndependent, **R**epeatable, **S**elf-validating, and **T**imely (written *before* production code).
*   **Arrange-Act-Assert (AAA)**: Separate the setup, execution, and validation blocks with vertical blank lines (no inline comments!).
*   **Single Reason to Fail**: Each test must evaluate a single behavior or business rule.
*   **Expressive Naming**: Test names must document the system's behavior and business rules (e.g., `test_fails_when_password_is_too_short`), rather than internal implementation steps.
*   **Transformation Priority Premise (TPP)**: Step-by-step, code should be transformed to be increasingly generic (e.g., hardcoded value $\rightarrow$ variable $\rightarrow$ conditional $\rightarrow$ loop).

---

## 3. Value Object Unit Tests

Value object tests must assert both the successful construction boundary and failures for invalid boundaries using `assertpy` and monadic `returns.result.Result` match patterns.

### Example Value Object Test
```python
import pytest
from assertpy import assert_that
from returns.result import Success, Failure
from src.common.billing.invoice_generation.domain.models.invoice_id import InvoiceId

def test_invoice_id_be_created_correctly():
    raw_id = "INV-2026-9999"
    result = InvoiceId.create(raw_id)

    match result:
        case Success(invoice_id):
            assert_that(str(invoice_id)).is_equal_to(raw_id)
        case Failure(error):
            pytest.fail(f"Expected Success, got Failure: {error}")

@pytest.mark.parametrize("invalid_id", [
    "",
    " ",
    "123"
])
def test_invoice_id_fail_creation_when_value_is_invalid(invalid_id):
    result = InvoiceId.create(invalid_id)

    match result:
        case Success(_):
            pytest.fail("Expected Failure, got Success")
        case Failure(error):
            assert_that(error).is_instance_of(ValueError)
```

---

## 4. Test Data Builders

Complex domain structures use the Builder pattern to provide fluid, maintainable arrangements in tests, avoiding duplicate instantiation code. In Python, builders can raise exceptions when unable to construct a valid object.

### Example Builder Pattern
```python
from src.common.billing.invoice_generation.domain.models.invoice_id import InvoiceId
from returns.result import Success, Failure

class InvoiceIdBuilder:
    def __init__(self):
        self._value = "INV-2026-9999"

    def with_value(self, value: str) -> "InvoiceIdBuilder":
        self._value = value
        return self

    def build(self) -> InvoiceId:
        result = InvoiceId.create(self._value)
        match result:
            case Success(invoice_id):
                return invoice_id
            case Failure(error):
                raise ValueError(f"Failed to build InvoiceId: {error}")
```

---

## 5. Use Case Mocking Unit Tests

Unit tests for application Use Cases set up mock behaviors on Ports (Protocols) using `unittest.mock` and verify invocation counts.

### Example Use Case Mocking Test
```python
from unittest.mock import Mock
from assertpy import assert_that
from returns.result import Success, Failure
from src.common.billing.invoice_generation.application.use_cases.process_invoice_payment import ProcessInvoicePayment
from tests.common.billing.invoice_generation.domain.builders.invoice_id_builder import InvoiceIdBuilder

def test_retrieve_token_from_cache_when_it_exists():
    token_cache = Mock()
    payment_client = Mock()
    gateway_client = Mock()
    use_case = ProcessInvoicePayment(token_cache, payment_client, gateway_client, "test-env")
    invoice_id = InvoiceIdBuilder().build()
    cached_token = "TOKEN-123456"
    token_cache.find_by.return_value = Success(cached_token)

    result = use_case.process(invoice_id, 150.00)

    match result:
        case Success(token):
            assert_that(str(token)).is_equal_to(cached_token)
            token_cache.find_by.assert_called_once_with(invoice_id, "test-env")
            payment_client.request_token.assert_not_called()
            gateway_client.execute_transaction.assert_not_called()
        case Failure(error):
            pytest.fail(f"Expected success, got: {error}")
```

---

## 6. Testing Strategy by Layer

Testing is structured to balance execution speed and safety:

### 6.1 Web API Route Handlers (FastAPI)
- **Unit Tests with Mocks**: API Endpoints must be tested using unit tests with mock representations of the application use cases using `unittest.mock`.
- **Scope**: Validate routing, status codes, input parsing, error mapping to JSON responses, and that the correct use case was executed.

### 6.2 Infrastructure Layer
- **Integration Tests**: Infrastructure-level components (database repositories, HTTP clients, cache wrappers) must be tested using integration tests against real or containerized services.
- **Testcontainers**: For databases (PostgreSQL) or event brokers (RabbitMQ, Kafka), use the `testcontainers` library to spin up clean containerized environments dynamically.

### 6.3 Domain Layer
- **Pure Unit Tests**: Domain Models (Entities, Aggregates) and Value Objects must be thoroughly tested without mocks or external dependencies.
- **Scope**: Validate all business invariants, state transition rules, and factory methods (`create`).

---

## 7. Documentation & Property-Based Testing

### 7.1 Documentation Tests (`doctest`)
Use doctests to simultaneously document code and write simple, execution-verified examples directly in docstrings.
*   *Heuristic Note*: Use the `+ELLIPSIS` flag to ignore unpredictable substrings (e.g. memory addresses) and `+NORMALIZE_WHITESPACE` to handle blank formatting issues.

```python
def square(n: int) -> int:
    """
    Returns the input number, squared.
    
    >>> square(2)
    4
    >>> square(3)
    9
    """
    return n ** 2
```

### 7.2 Property-Based Testing (`Hypothesis`)
Use `Hypothesis` to automate the generation of hundreds of boundary data combinations to test against core properties. Combine with `assertpy` for fluent assertions.

```python
from hypothesis import given
from hypothesis.strategies import text
from assertpy import assert_that

@given(text())
def test_hash_has_always_the_same_fixed_length(text_input):
    assert_that(len(calculate_hash(text_input))).is_equal_to(10)
```

---

## 8. Test Doubles & Mocks

*   **Mocking with `unittest.mock.patch`**: Use mocks/patches to isolate systems from non-deterministic logic (e.g. system clock, random generator).
*   **Heuristic Note**: Use mocks sparingly. Overusing mocks—especially mocking other mocks—tightly couples your tests to implementation details and inhibits refactoring.

```python
from unittest import mock
import random

@mock.patch('random.random')
def test_random_generation(mock_random):
    mock_random.return_value = 0.1

    assert_that(random.random()).is_equal_to(0.1)
    assert_that(mock_random.call_count).is_equal_to(1)
```

---

## 9. Scenario Tests & Concurrency

Scenario tests verify complete end-to-end workflows. They share stateful external resources, and running them concurrently can lead to race conditions.

- **Dedicated Files**: Each scenario test must reside in its own dedicated file under a `tests/scenarios/` directory.
- **Isolate State**: Ensure each test run uses unique identifiers (e.g., randomly generated UUIDs, unique transaction codes) to prevent test-to-test pollution.
- **pytest Ordering**: If parallel run configurations (like `pytest-xdist`) are active, mark scenario tests (e.g. `@pytest.mark.sequential`) or segregate databases to prevent concurrent state corruption.
