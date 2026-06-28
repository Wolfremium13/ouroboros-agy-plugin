# Python Domain-Driven Design (DDD) & Domain Models Guide

This document defines the rules and guidelines for domain logic encapsulation, entity modeling, value objects, events, and transactional boundaries in Python.

---

## 1. Class and Dataclass Organization

To establish clear semantic purposes across Python types:
- **Domain Models (Entities & Aggregates)**: Use standard Python `class` types or mutable `@dataclasses.dataclass` with custom business methods.
- **Value Objects**: Use immutable `@dataclasses.dataclass(frozen=True)` to measure, quantify, or describe domain concepts.
- **Domain & Integration Events**: Always use immutable `@dataclasses.dataclass(frozen=True)`. Since events represent historical, immutable facts, frozen dataclasses are ideal for their representation.
- **Data Transfer Objects (DTOs)**: Use `@dataclasses.dataclass(frozen=True)` or Pydantic `BaseModel` (with `frozen=True`).

---

## 2. Domain Encapsulation & Validation

Domain models must protect their invariants and remain isolated from external concerns.

### 2.1 State Encapsulation ("Tell, Don't Ask")
- Do not expose class attributes directly for public mutation. Internal state variables should be prefixed with a single underscore (e.g., `_status`) to denote protect/private visibility.
- State mutation and queries must happen exclusively through domain-language methods representing business actions (e.g., `user.activate()`, not `user.status = "active"`).
- The Domain layer must be entirely isolated from Application and Infrastructure layers. Define Ports (interfaces) in the Domain using `typing.Protocol` or `abc.ABC` that are implemented in the Infrastructure.

### 2.2 Factory Methods & Initialization
- **Encapsulated Constructors**: Python does not support private constructors natively. By convention, callers must not invoke `__init__` directly. Enforce instantiation through class-level factory methods.
- **Factory Methods**: Instantiation must go through `@classmethod` factory methods (e.g., `create()`).
- **Validation**: Factory methods must validate all business invariants and return a monadic container (e.g. `returns.result.Result`). Never raise exceptions for normal domain validation failures.
- **Immutability**: Internal fields of Value Objects must be read-only. Replace them entirely when their value changes rather than mutating fields.

### 2.3 Value Object Example (`InvoiceId`)
```python
from dataclasses import dataclass
from returns.result import Result, Success, Failure

@dataclass(frozen=True)
class InvoiceId:
    _value: str

    @classmethod
    def create(cls, given_invoice_id: str) -> Result["InvoiceId", Exception]:
        if not given_invoice_id or not given_invoice_id.strip():
            return Failure(ValueError("Invoice Identifier cannot be empty or null."))

        if len(given_invoice_id) < 5:
            return Failure(ValueError("Invoice Identifier is too short."))

        return Success(cls(given_invoice_id))

    def __str__(self) -> str:
        return self._value
```

---

## 3. Aggregates & Eventual Consistency

- **Small Aggregates**: Design small aggregates to protect business invariants. Reference other aggregates by unique identity only (e.g., `uuid.UUID` or a typed Value Object identifier like `UserId`), never by direct object reference.
- **Eventual Consistency**: Use Domain Events for eventual consistency. When an aggregate undergoes a state transition, it should append a Domain Event to an internal list (e.g., `self.domain_events.append(...)`). These events are handled after the primary transaction commits.
- **Outbox Pattern**: When publishing integration events to external systems, store the events in an Outbox table within the same database transaction as the domain changes. A background worker should read and dispatch the events, ensuring reliable at-least-once delivery.
- **Transactional Safety**: If any step of an application workflow returns a validation or domain error (a monadic `Failure` result), the transaction must be aborted/rolled back, ensuring no partial state is committed to the persistence layer.
- **Repositories**: Create repositories only for Aggregate Roots. Provide a collection-like interface (defined via a `Protocol` port) that completely hides underlying database operations.
