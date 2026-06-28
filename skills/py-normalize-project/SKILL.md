---
name: py-normalize-project
description: Refactor, format, and normalize C# and Python code to conform to Clean Architecture and DDD.
---

# Python Codebase Compliance Normalizer (`py-normalize-project`)

This skill defines the rules for automatically refactoring, formatting, and correcting compliance violations across Python source files.

---

## 1. Interaction Flow

When this skill is activated:
1.  **Ask for Target Files:** Ask the user: *"Which directories or files should I normalize?"*
2.  **Verify Setup:** Check if `make lint` is configured and that `ruff` or the project's formatting tools are accessible.
3.  **Execute Normalizations:** Modify files in small batches to fix style, architecture, and syntax discrepancies.
4.  **Confirm Changes:** Run `make lint` and `make tests` to ensure code remains fully functional, showing a diff summary of applied refactorings.

---

## 2. Refactoring Transformations

Apply the following automated corrections:

### 2.1 Tooling & Formatting
*   **Linters/Formatters:** Run `make lint` to automatically clean up whitespaces, unused imports, and basic formatting issues.
*   **PEP 8 Compliance:** Ensure strict line length limits (79 for code, 72 for comments/docstrings).

### 2.2 Import Normalization
*   **Absolute Paths:** Rewrite relative import statements (e.g., `from ...models import User`) to absolute imports under the `src/` directory (e.g., `from src.common.billing.users.register.domain.models import User`).

### 2.3 Assertions Upgrade
*   **Fluent Assertions:** Convert standard `assert` statements in unit tests into `assertpy` expressions:
    *   `assert result == expected` $\rightarrow$ `assert_that(result).is_equal_to(expected)`
    *   `assert isinstance(err, ValueError)` $\rightarrow$ `assert_that(err).is_instance_of(ValueError)`

### 2.4 Modern Syntax Upgrades (Python 3.12+)
*   **Method Overrides:** Inject the `@typing.override` decorator (imported from `typing` or `typing_extensions`) onto methods that implement protocol definitions or abstract methods.
*   **Modern Generics:** Refactor generic classes and functions to use square bracket syntax (PEP 695) instead of `TypeVar` variables:
    *   `T = TypeVar('T')` / `class Box(Generic[T])` $\rightarrow$ `class Box[T]`
*   **Native Union Syntax:** Replace `typing.Union[X, Y]` and `typing.Optional[X]` with the native pipe `X | Y` and `X | None` type hints.

### 2.5 Test File Cleanup
*   **Remove Section Comments:** Delete any `# Arrange`, `# Act`, or `# Assert` comments within unit tests, ensuring the blocks are separated solely by empty lines.
