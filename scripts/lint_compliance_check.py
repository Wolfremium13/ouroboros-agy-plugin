import subprocess
import sys
import re

def get_staged_files():
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return [f.strip() for f in result.stdout.splitlines() if f.strip().endswith(".py")]

def main():
    staged_files = get_staged_files()
    if not staged_files:
        print("No staged Python files found to lint.")
        sys.exit(0)

    violations = []

    # Compile regexes
    interface_prefix_pattern = re.compile(r"^\s*(class\s+I[A-Z][a-zA-Z0-9]*)")
    test_comment_pattern = re.compile(r"^\s*#\s*(Arrange|Act|Assert)\b", re.IGNORECASE)

    for file_path in staged_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
            continue

        lines = content.splitlines()

        # Rule 1: Check for interface prefix 'I' (Hungarian notation)
        for line_num, line in enumerate(lines, 1):
            match = interface_prefix_pattern.match(line)
            if match:
                violations.append(
                    f"{file_path}:{line_num}: Hungarian notation warning. Avoid prefixing class '{match.group(1).split()[1]}' with 'I'."
                )

            # Rule 2: Check for Arrange/Act/Assert comments in test files
            if "test" in file_path.lower():
                if test_comment_pattern.match(line):
                    violations.append(
                        f"{file_path}:{line_num}: Remove test labeling comment '{line.strip()}'. Separate phases with blank lines."
                    )

        # Rule 3: Check architectural layer dependency violations
        if "domain" in file_path:
            for line_num, line in enumerate(lines, 1):
                if "import" in line:
                    if any(x in line for x in [".application", ".infrastructure", "api_gateway", "internal_web", "internal_worker"]):
                        violations.append(
                            f"{file_path}:{line_num}: Domain layer violation. Domain must not import from higher layers: '{line.strip()}'."
                        )

    if violations:
        print("❌ LINT COMPLIANCE ERROR: Found standard violations in staged Python files:", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        sys.exit(1)

    print("✅ Lint compliance check passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
