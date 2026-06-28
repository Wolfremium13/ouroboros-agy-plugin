# Python Coding Style & Guidelines (Python Mastery)

This document outlines the coding standards, language features, and component design patterns used across Python projects, adapting clean architectural styles to Pythonic conventions.

---

## 1. Role, Philosophy & Modern Syntax (Python 3.10+)

We write **Pythonic, readable, concise, and maintainable code** following the philosophies of **PEP 20 (The Zen of Python)**.

### 1.1 Core Principles
*   **Beautiful is better than ugly.**
*   **Explicit is better than implicit.** Favor explicit imports (`import os`, `import asyncio`) and clear variable names. Avoid implicit wildcard imports or arbitrary arguments (`*args`, `**kwargs`) unless strictly necessary.
*   **Simple is better than complex.** Avoid over-engineering; use simple loops and filters instead of complicated nested comprehensions. Flat is better than nested.
*   **Adhere to PEP 8** for code formatting. Restrict line lengths (79 characters for code, 72 for docstrings/comments) to improve readability.
*   **Avoid backslashes for line continuation**; prefer implicit line continuation inside parentheses `()`.
*   **Formatting Strings:** **Always use f-strings** (`f"Hi {name}"`) instead of older `%` style or `.format()`. For Python 3.12+ (PEP 701), take advantage of full nesting capabilities (e.g., nesting double quotes inside quotes `f"User: {data['name']}"`), multi-line expressions, and inline comments within placeholders.

### 1.2 Modern Syntax and Features
*   **Type Hinting & Modern Generics:** Always use type annotations for function arguments and return values.
    *   **Modern Generics (Python 3.12+ / PEP 695):** Use the new square bracket syntax for generics (e.g., `class Box[T]:` and `def first[T](items: list[T]) -> T:`) instead of old `TypeVar` boilerplate.
    *   **Type Aliasing (Python 3.12+):** Define custom type aliases using the explicit `type` keyword: `type Coordinate = tuple[float, float]`.
    *   **Lazy Annotations (Python 3.14+ / PEP 649):** Type hints are evaluated lazily, improving startup times and avoiding circular dependency import workarounds.
    *   **Standard Typing:** Use Python 3.10+ native union operators (`int | None`) rather than importing `Union` or `Optional` from the `typing` module.
*   **Structural Pattern Matching:** Utilize `match`/`case` switch statements for complex value and sequence matching, incorporating guards (`if`) where necessary.
*   **Assignment Expressions:** Use the walrus operator (`:=`) to assign and evaluate variables in a single expression when it improves readability (e.g., inside loops or conditional clauses).
*   **Advanced Collections:** Use Python's built-in collections rather than reinventing the wheel (e.g., `defaultdict` for automatic dictionary value initialization, `ChainMap` to combine multiple scopes, and `enum.Enum` for grouping constants).
*   **Dataclasses:** Use `@dataclasses.dataclass` (with `frozen=True` where immutability is desired) to implement smart data storage with automatic type hinting, `__init__`, and `__repr__` generation.
*   **Generators over Lists:** For large datasets, **always prefer generators and generator comprehensions** over lists to dramatically reduce memory and CPU usage.
*   **EAFP over LBYL:** Prefer the "Easier to Ask for Forgiveness than Permission" (EAFP) pattern using `try/except` blocks over "Look Before You Leap" (LBYL) `if` checks. Rely on **duck typing** instead of strict type checking (`isinstance`) where appropriate.
*   **Explicit Method Overrides (Python 3.12+ / PEP 698):** Always decorate overridden methods in child classes or contract implementations with `@typing.override` to ensure type-check-time safety.
*   **Precise Type Narrowing (Python 3.13+ / PEP 742):** Use `typing.TypeIs` instead of `TypeGuard` for cleaner type narrowing that refines types in both the positive (`if`) and negative (`else`) branches.

---

## 2. Application Use Cases & Pipelines

Application Services coordinate domain interactions using functional query pipelines.

### 2.1 Pipeline Chaining & Private Helpers
*   Keep monadic query pipelines clean and readable (e.g., chaining `.bind()` or using generator expressions).
*   If a complex transformation or error mapping does not fit cleanly inside a pipeline, extract it to a **private helper function** (prefixed with `_`).

### 2.2 Application Contracts & Commands
*   **Contracts Folder:** Place use case contracts inside `application/contracts/`.
*   **Single File per Contract:** Declare exactly one use case/service interface (using `typing.Protocol` or `abc.ABC`) per file. Do not bundle multiple unrelated use case interfaces together.
*   **Commands in Contract Files:** Define the associated input Command or Request (typically a dataclass) directly in the same file as the interface contract, positioned immediately below the interface definition.

#### Example Contract File (`src/common/billing/users/register/application/contracts/register_user.py`)
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from returns.result import Result  # Or equivalent monadic Result/Either

@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    email: str

@dataclass(frozen=True)
class RegisteredUserInfo:
    user_id: str
    username: str

class RegisterUser(ABC):
    @abstractmethod
    def register(self, command: RegisterUserCommand) -> Result[RegisteredUserInfo, Exception]:
        """Register a new user."""
```

#### Example Use Case Implementation (`src/common/billing/users/register/application/use_cases/register_user.py`)
```python
from returns.result import Result, Success, Failure
from src.common.billing.users.register.application.contracts.register_user import (
    RegisterUser, RegisterUserCommand, RegisteredUserInfo
)
from src.common.billing.users.register.domain.models.user import User
from src.common.billing.users.register.domain.ports.user_repository import UserRepository
from src.common.billing.users.register.domain.ports.user_event_publisher import UserEventPublisher

class RegisterUserUseCase(RegisterUser):
    def __init__(self, user_repository: UserRepository, event_publisher: UserEventPublisher):
        self._user_repository = user_repository
        self._event_publisher = event_publisher

    def register(self, command: RegisterUserCommand) -> Result[RegisteredUserInfo, Exception]:
        # Chain steps monadically
        return (
            User.create(command.username, command.email)
            .bind(self._user_repository.save)
            .bind(self._event_publisher.publish_user_registered)
            .map(lambda user: RegisteredUserInfo(user.id, user.username))
        )
```

---

## 3. Centralized Error Handling

Custom errors are modeled using monadic Result containers (e.g. `Result[SuccessValue, ErrorValue]`).

### Error Handling Guidelines
*   **No Exceptions for Control Flow:** Do not raise exceptions to handle expected control flow, business validation, or external client failures in production code. Return `Failure(ErrorObject)` instead.
*   **Errors should never pass silently:** Catch specific exceptions (e.g., `ValueError`, `KeyError`) or explicitly log them using `logging.exception`. Never use bare `except: pass`.
*   **Exception Groups (Python 3.11+ / PEP 654):** In concurrent and asynchronous tasks (e.g. `asyncio`), use `ExceptionGroup` and `except*` syntax to handle multiple independent exceptions simultaneously.
*   **Logging over Print:** For production code, use the `logging` module instead of `print` statements. Implement proper logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) and configure loggers natively (using `dictConfig` or JSON/INI configurations).
*   **Test Builder Exception:** Inside test suites, Test Data Builders or Factories are permitted to raise exceptions if invalid arguments prevent object construction.

---

## 4. Web API Route Handlers

API Endpoints must follow the Single Responsibility Principle and the REPR (Request-Endpoint-Response) pattern.

*   **Single File per Handler:** Group handlers by bounded context under `routes/v[number]/[bounded_context]/[action].py`. Each module should expose route path handlers representing a single endpoint.
*   **Functional Mapping:** Map Result outcomes to HTTP response models or raise standard HTTP status codes based on the monad's inner value.

#### Example Route Handler (`src/internal_web/routes/v1/users/register.py`)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from returns.result import Success, Failure
from src.common.billing.users.register.application.contracts.register_user import RegisterUserCommand
from src.internal_web.dependencies import get_register_use_case

router = APIRouter()

@router.post("/register", status_code=status.HTTP_200_OK)
def register_user(username: str, email: str, use_case=Depends(get_register_use_case)):
    command = RegisterUserCommand(username=username, email=email)
    
    match use_case.register(command):
        case Success(info):
            return {"userId": info.user_id, "username": info.username}
        case Failure(error):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error)
            )
```

---

## 5. Event Consumers & Background Workers

Background services process incoming domain event payloads using monadic pipelines.

#### Example Background Consumer
```python
from returns.result import Result, Success, Failure
from src.common.billing.shared.domain.events import BillingNotificationEvent

class ProcessBillingNotificationConsumer:
    def __init__(self, notification_processor):
        self._notification_processor = notification_processor

    def process_message(self, json_payload: str) -> Result[None, Exception]:
        return (
            BillingNotificationEvent.from_json(json_payload)
            .bind(self._notification_processor.send_email_notification)
        )
```

---

## 6. Dependency Injection & Configuration Setup

*   **Explicit Setup:** Encapsulate service registrations in setup functions per bounded context (e.g. `register_room_access_services(container)`).
*   **Required Constructor Parameters & Logging:** Never default loggers to `None` in constructor signatures. Loggers must be required dependencies.
*   **Mocking in Tests:** In tests, pass standard mock objects (e.g. `unittest.mock.Mock` or `unittest.mock.AsyncMock`) rather than `None`.

---

## 7. Testing and Quality Assurance

*   **pytest over unittest:** Use `pytest` for writing unit and regression tests due to its cleaner output, simpler assertions (just use `assert`), and powerful `fixture` system.
*   **Doctests:** Use the `doctest` module to simultaneously document your code and write simple, execution-verified examples directly in your docstrings.
*   **Mocking:** Use `unittest.mock` (e.g., `@mock.patch`) or `pytest`'s `monkeypatch` to safely fake external resources, databases, or random operations in tests.

---

## 8. Deterministic vs. Non-Deterministic Operations

Do not access non-deterministic system operations directly within domain logic.

*   **Never call directly:** Never invoke functions like `datetime.now()`, `uuid.uuid4()`, or `random.random()` directly in domain entities or use cases.
*   **Use Providers/Ports:** Wrap non-deterministic generations behind interfaces/protocols to allow easy mocking during test execution.

#### Example Interface & Usage
```python
from typing import Protocol
from datetime import datetime
import uuid

class DateTimeProvider(Protocol):
    def utc_now(self) -> datetime:
        ...

class UUIDProvider(Protocol):
    def new_uuid(self) -> uuid.UUID:
        ...
```

---

## 9. Naming Conventions

Consistent naming ensures readability, reduces cognitive load, and aligns Python code with the business domain.

### 9.1 Naming Conventions Table

| Element | Style | Example | Notes |
| :--- | :--- | :--- | :--- |
| **Interfaces / Protocols / ABCs** | PascalCase | `InvoicePaymentClient` | Represents a port or abstraction. |
| **Classes / Dataclasses** | PascalCase | `InvoicePayment` | Implementations, entities, or value objects. |
| **Methods & Functions** | snake_case | `process_payment` | Should start with a verb indicating action. |
| **Method Parameters & Variables** | snake_case | `invoice_id`, `given_amount` | Descriptive snake_case names. |
| **Private Fields & Methods** | snake_case, leading `_` | `_payment_client` | For class-level private dependencies or state. |
| **Constants** | UPPER_CASE | `DEFAULT_TIMEOUT` | Declared at the module level. |
| **Unit Test Classes** | PascalCase, starts with `Test` | `TestPaymentProcessor` | Standard class identifier for pytest. |
| **Test Methods** | snake_case, starts with `test_` | `test_approve_valid_payment` | States the expected outcome or scenario. |
| **Test Data Builders & Factories**| PascalCase, suffixed | `InvoiceBuilder` | Follows the builder or factory patterns. |

### 9.2 Core Naming Guidelines

1.  **Adopt the Ubiquitous Language:** Base class, method, and variable names strictly on the vocabulary spoken by domain experts. Avoid artificial technical suffixes like `OrderFactory`, `OrderManager`, or `OrderHelper` unless they have genuine business meaning.
2.  **Focus on Intent and Purpose:** Name classes and protocols to explicitly describe their purpose and role, without referencing *how* they achieve it.
3.  **Ports & Interfaces as Behavior Expressions (No `I` Prefix):** Define ports using `typing.Protocol` or `abc.ABC` without Hungarian notation. **Interfaces must represent behavior expressions** (focusing on capabilities, actions, or roles, e.g., `Reader`, `Writer`, `EventPublisher`, `UserRepository`). They must contain no connection, database, or technology-specific details.
4.  **Infrastructure Implementations (Adapters):** Prefix the implementation with the specific technology or protocol being used (e.g., `PostgresUserRepository`, `HttpGovernmentClient`, `KafkaEventPublisher`). Never use generic suffixes like `Impl` or `Base`.
5.  **Eliminate Technical Jargon:** Do not embed technical patterns or data types in class names. Avoid suffixes like `Abstract` or `Base` in class names, and avoid extraneous nouns like `Object` (e.g., use `File` instead of `FileObject`).
6.  **Avoid Catch-All Words:** Avoid overly generic words such as `Manager`, `Helper`, `Processor`, `Engine`, `Tool`, or `Utils` unless representing a precise design pattern.
7.  **Do Not Use Acronyms:** Spell out words fully to ensure clarity, reduce ambiguity, and maintain readability across the codebase (e.g., use `user_identifier` instead of `uid`, or `request` instead of `req`).
8.  **Do Not Use "Should" in Production Naming:** Production code names (including files, classes, methods, and variables) must not contain the word 'should' (case-insensitive). The use of 'should' is strictly reserved for test files and test methods.

