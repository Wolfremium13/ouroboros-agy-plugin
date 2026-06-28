---
name: py-add-comments
description: Add or update Python docstrings and comments using Google Style. Triggers when the user wants to add, document, or check comments in Python code.
---

# Google-Style Python Documenter (`py-add-comments`)

This skill guides the agent in adding, updating, and auditing Python docstrings and comments. It enforces the Google Python Style Guide for docstrings, promotes concise public-only documentation, and restricts inline comments to non-obvious details.

## 1. Initial Interaction Pattern

When this skill is activated, you **MUST** immediately prompt the user to specify the target file or directory to process:
*   *Required User Input:* "Where should I start looking to put or update comments?"
*   *Action:* Do not begin scanning or modifying files until the user has responded with a file, directory path, or scope.

## 2. Docstring Rules (Google Style)

For all public classes, functions, and methods, write docstrings using the **Google style docstrings** format (Sphinx Napoleon standard):
*   Provide a single-line summary of what the method/function does.
*   Keep explanation of the code **as short as possible**.
*   **Only document public methods, functions, and classes.** Do not add docstrings to private helper methods (prefixed with `_` or `__`) unless explicitly requested.

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

## 3. Inline Comments Rules

Inline comments must be kept to an absolute minimum and obey these constraints:
*   **Do not repeat the code:** If the code already expresses the action (e.g. `x = x + 1`), do not add an inline comment explaining that.
*   **Explain the non-obvious:** Only use inline comments to explain things the code cannot explain itself (such as framework quirks, design workarounds, complex external API dependencies, or non-obvious success paths).
*   *Example:*
    ```python
    return None  # This is how the framework handles success
    ```
    ```python
    time.sleep(0.1)  # Required to prevent rate limiting from the third-party api
    ```

---

## 4. Execution Workflow

1.  **Ask the human:** Ask the human where to start looking.
2.  **Scan the targets:** Analyze the Python files in the specified location.
3.  **Identify public methods:** List all public classes, functions, and methods lacking docstrings or containing outdated/non-Google-style docstrings.
4.  **Edit in small batches:** Use code editing tools to update the files, following the TDD/Branching rules (if active).
5.  **Review inline comments:** Clean up redundant inline comments and add comments only for non-obvious patterns.
