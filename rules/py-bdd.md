# Behavior-Driven Development (BDD) Guidelines

This document defines the rules and best practices for writing clean, maintainable, and business-focused BDD specifications (Gherkin/Feature files) for Python projects.

---

## 1. Core BDD Rules

To write high-quality executable specifications, all scenarios must adhere to the following rules:

### Rule 1: Be Declarative, Not Imperative (Focus on *What*, Not *How*)
A good BDD example describes the business intent and user behavior, without getting bogged down in technical implementation or UI mechanics.
*   **Bad (Imperative):** Scenarios that read like manual test scripts.
    *   *Example:* `When he goes to the registration page, And he enters 'Bill' in the first name field, And he enters 'Smith' in the surname field... And he clicks on submit`. This is fragile and tightly coupled to the UI.
*   **Good (Declarative):** Scenarios that focus on the business action.
    *   *Example:* `When he submits his application online`. You can also hide field values inside a data table to keep the core action readable.

### Rule 2: Test a Single Action and Illustrate a Single Rule
A good scenario focuses on one specific behavior or business rule. Mixing multiple actions and expected outcomes creates confusing, script-like tests.
*   **Bad (Multiple Actions):** Mixing `When` and `Then` steps repeatedly.
    *   *Example:* `When I select the 'accounts' menu / Then I should see the 'Accounts' page / When I click on 'Edit' / Then I should see 'Account Details'`.
*   **Good (Single Action):**
    *   *Example:* `When I update my address details / Then the updated details should be visible in the account summary`. If an example naturally illustrates multiple rules at once, it must be split up so each scenario focuses on just one rule.

### Rule 3: Use Concrete, Essential Data Only
Good examples use specific, real-world data (actual text strings, values, dates) to avoid ambiguity, but they strictly exclude any data that is not directly related to the behavior being illustrated.
*   **Bad (Irrelevant Clutter):** Specifying the type of pizza ordered and confirming that payment was authorized when the scenario is *only* supposed to be testing if a user can change their delivery address. Exposing technical setup details is also bad, such as: `Given that an admin account is set up in the database`.
*   **Good (Essential Context):**
    *   *Example:* `Given I am logged in as an administrator` focuses purely on the business context needed for the test to make sense.

### Rule 4: Ensure Scenario Independence
Every executable specification must be self-sufficient and prepare its own initial state.
*   **Bad (Dependent):** Scenario 1 (`Adding an item to the cart`) adds an item, and Scenario 2 (`Purchasing items in my cart`) assumes the cart is already populated from the first scenario. If run out of order or on a fresh environment, Scenario 2 will fail.
*   **Good (Independent):** Each scenario establishes its own preconditions in the `Given` step, ensuring the system is in the exact state needed before the `When` action occurs.

### Rule 5: Eliminate Duplication Using Tables and Backgrounds
A good BDD structure avoids repetitive, wordy scenarios that cause readers to skim and miss important details.
*   **Bad (Duplication):** Writing out five almost identical scenarios to test how different frequent flyer statuses (Standard, Silver, Gold) affect earned points.
*   **Good (Concise):** Using a `Scenario Outline` with an `Examples` data table to test multiple variations of a rule in a single block. Additionally, if multiple scenarios share the same exact setup steps, a good structure moves those shared steps into a single `Background` block at the top of the feature file.

---

## 2. Python Integration & Testing

For Python BDD implementation, use libraries such as **`behave`** or **`pytest-bdd`**. Ensure step definitions call domain entities or use case contracts directly rather than coupling step definitions to low-level implementation details.
