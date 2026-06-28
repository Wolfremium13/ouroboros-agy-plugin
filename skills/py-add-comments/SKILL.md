---
name: py-add-comments
description: Add/update Google Style Python docstrings and comments when documenting or checking Python code.
---

# Google-Style Python Documenter (`py-add-comments`)

This skill guides the agent in adding, updating, and auditing Python docstrings and comments. It enforces the Google Python Style Guide for docstrings, promotes clean self-documenting code principles, and restricts inline comments to non-obvious details.

---

## 1. Initial Interaction Pattern

When this skill is activated, you **MUST** immediately prompt the user to specify the target file or directory to process:
*   *Required User Input:* "Where should I start looking to put or update comments?"
*   *Action:* Do not begin scanning or modifying files until the user has responded with a file, directory path, or scope.

---

## 2. Core Heuristics: Avoid Redundant Comments

The overarching rule is: **Avoid comments as much as possible.** Code must be self-documenting through clear naming, static type hints, and clean structure.

*   **No Comments in Tests:** Do not write comments in unit or integration tests to label sections (e.g., do NOT write `# Arrange`, `# Act`, `# Assert`). Instead, separate these logical phases strictly using vertical whitespace (empty lines).
*   **Favor Naming and Types:** If a comment simply explains what a block of code does, extract the block into a helper function and give it a well-thought-out name. Rely on Python type hinting to make interfaces self-explanatory.
*   **Do Not Explain the "How":** If a comment details the mechanics of the implementation, delete it. The code already shows how it operates; commenting on the mechanics violates the DRY (Don't Repeat Yourself) principle.
*   **Do Not Repeat the Code:** If a reader could write the exact same comment just by looking at the adjacent line, the comment is redundant and must be removed.

---

## 3. Docstring Rules (Google Style)

For all public classes, functions, and methods, write docstrings using the **Google style docstrings** format (Sphinx Napoleon standard):
*   Provide a single-line summary of what the method/function does.
*   Keep explanation of the code **as short as possible**.
*   **Only document public methods, functions, and classes.** Do not add docstrings to private helper methods (prefixed with `_` or `__`) unless explicitly requested.
*   **Docstrings as a Design Tool:**
    *   Draft the public interface docstrings *before* writing the implementation.
    *   **"Hard to Describe" Red Flag:** If you find it difficult to write a simple, complete docstring for a method or class, this indicates a flawed design or poor abstraction. Use this as a trigger to rethink the code structure.

### Google Style Examples

#### Functions/Methods with arguments and return values:
```python
def calculate_metrics(data: list[float], threshold: float = 0.5) -> dict[str, float]:
    """Calculate summary metrics for thresholded values.

    Args:
        data: List of numerical float values.
        threshold: Minimum value cutoff (default: 0.5).

    Returns:
        A dictionary containing "mean" and "count" metrics.
    """
```

#### Exceptions:
```python
def fetch_user(user_id: str) -> User:
    """Fetch user by ID.

    Args:
        user_id: Unique string identifier for the user.

    Returns:
        The matched User object.

    Raises:
        UserNotFoundError: If no user matches the ID.
    """
```

---

## 4. Inline Comments Rules

Inline comments must be kept to an absolute minimum and obey these constraints:
*   **Document the "Why":** Use inline comments to explain goals, engineering trade-offs, design choices, and why certain alternatives were discarded.
*   **Explain the Non-Obvious:** Only use inline comments to explain details the code cannot explain itself (such as framework quirks, design workarounds, complex external API dependencies, or non-obvious success paths).
    *   *Example:* `return None  # This is how the framework handles success`
    *   *Example:* `time.sleep(0.1)  # Required to prevent rate limiting from the third-party api`
*   **Add Precision to Variables:** Use comments to clarify abstract meanings that code cannot express, such as units of measurement (e.g., pixels, milliseconds), inclusive/exclusive boundary conditions, or what a `None` value implies.
*   **Document Surprises and Quirks:** Use comments to explain complex regular expressions, surprising library behaviors, or workarounds for bugs.

---

## 5. Execution Workflow

1.  **Ask the human:** Ask the human where to start looking.
2.  **Scan the targets:** Analyze the Python files in the specified location.
3.  **Identify public methods:** List all public classes, functions, and methods lacking docstrings or containing outdated/non-Google-style docstrings.
4.  **Audit existing comments:**
    *   Identify and remove comments in test files (e.g., `# Arrange/Act/Assert`).
    *   Identify and remove comments that repeat the code or explain "how" it works.
5.  **Edit in small batches:** Use code editing tools to update the files, following the TDD/Branching rules (if active).
6.  **Evaluate abstractions:** If any method/class docstring is hard to summarize concisely, alert the user and propose refactoring the code structure rather than documenting a bad design.
