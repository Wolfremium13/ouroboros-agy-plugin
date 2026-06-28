#!/usr/bin/env python3
import argparse
import os
import re
import sys

def to_snake_case(name):
    # Convert PascalCase to snake_case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Scaffold a DDD Value Object and its corresponding unit tests."
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Name of the Value Object in PascalCase (e.g., EmailAddress)."
    )
    parser.add_argument(
        "--type",
        required=True,
        help="Underlying primitive data type (e.g., str, int, float)."
    )
    parser.add_argument(
        "--dir",
        required=True,
        help="Target directory for the production model (e.g., src/common/billing/users/register/domain/models)."
    )
    return parser.parse_args()

def generate_vo_code(class_name, primitive_type):
    return f'''from dataclasses import dataclass
from returns.result import Result, Success, Failure

@dataclass(frozen=True)
class {class_name}:
    """
    {class_name} represents a domain value object.
    
    Invariants:
    - Must be validated upon instantiation via the create() factory.
    """
    _value: {primitive_type}

    @classmethod
    def create(cls, value: {primitive_type}) -> Result["{class_name}", Exception]:
        """
        Factory method to create a validated {class_name} instance.
        
        Args:
            value: The raw input value.
            
        Returns:
            A Success containing the validated {class_name} or a Failure wrapping a ValueError.
        """
        # TODO: Implement invariant validation rules
        if not value:
            return Failure(ValueError("{class_name} cannot be empty."))
            
        return Success(cls(value))

    def __str__(self) -> str:
        return str(self._value)
'''

def generate_test_code(class_name, snake_name, import_path, primitive_type):
    # Set sample values based on type
    if primitive_type == "int":
        valid_val, invalid_val_1, invalid_val_2 = "42", "0", "-1"
    elif primitive_type == "float":
        valid_val, invalid_val_1, invalid_val_2 = "42.0", "0.0", "-1.0"
    else:
        valid_val, invalid_val_1, invalid_val_2 = '"valid_string"', '""', '" "'

    return f'''import pytest
from assertpy import assert_that
from returns.result import Success, Failure
from {import_path} import {class_name}

def test_{snake_name}_created_successfully():
    valid_value = {valid_val}
    result = {class_name}.create(valid_value)

    match result:
        case Success(vo):
            assert_that(str(vo)).is_equal_to(str(valid_value))
        case Failure(error):
            pytest.fail(f"Expected Success, got Failure: {{error}}")

@pytest.mark.parametrize("invalid_value", [
    {invalid_val_1},
    {invalid_val_2}
])
def test_{snake_name}_fails_creation_when_value_is_invalid(invalid_value):
    result = {class_name}.create(invalid_value)

    match result:
        case Success(_):
            pytest.fail("Expected Failure, got Success")
        case Failure(error):
            assert_that(error).is_instance_of(ValueError)
'''

def main():
    args = parse_arguments()
    class_name = args.name
    primitive_type = args.type
    prod_dir = args.dir

    # Validate class name conventions
    if not re.match(r"^[A-Z][a-zA-Z0-9]*$", class_name):
        print(f"Error: Class name '{class_name}' must be PascalCase.", file=sys.stderr)
        sys.exit(1)

    if "should" in class_name.lower():
        print("Error: Production class names must not contain the word 'should'.", file=sys.stderr)
        sys.exit(1)

    # Normalize directories
    prod_dir = os.path.normpath(prod_dir)
    snake_name = to_snake_case(class_name)
    vo_filename = f"{snake_name}.py"
    vo_filepath = os.path.join(prod_dir, vo_filename)

    # Calculate test path by swapping src/ with tests/
    if not prod_dir.startswith("src/"):
        # If it doesn't start with src/, we assume it is under project root
        test_dir = os.path.join("tests", prod_dir)
    else:
        test_dir = prod_dir.replace("src/", "tests/", 1)
    
    test_filename = f"test_{snake_name}.py"
    test_filepath = os.path.join(test_dir, test_filename)

    # Calculate python import path from prod_dir
    # e.g., src/common/billing/domain/models -> src.common.billing.domain.models.email_address
    import_path = prod_dir.replace(os.sep, ".").strip(".") + f".{snake_name}"

    # Write VO file
    os.makedirs(prod_dir, exist_ok=True)
    with open(vo_filepath, "w", encoding="utf-8") as f:
        f.write(generate_vo_code(class_name, primitive_type))
    print(f"Scaffolded Value Object: {vo_filepath}")

    # Write Test file
    os.makedirs(test_dir, exist_ok=True)
    with open(test_filepath, "w", encoding="utf-8") as f:
        f.write(generate_test_code(class_name, snake_name, import_path, primitive_type))
    print(f"Scaffolded Unit Test: {test_filepath}")

    print("Scaffolding complete. Please run tests and format code using 'make tests' and 'make lint'.")

if __name__ == "__main__":
    main()
