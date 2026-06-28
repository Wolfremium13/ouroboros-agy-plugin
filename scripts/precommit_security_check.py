import subprocess
import sys
import re

def main():
    # Run git diff --cached to get staged changes
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running git diff --cached", file=sys.stderr)
        sys.exit(1)

    diff_text = result.stdout
    lines = diff_text.splitlines()

    # Simple regexes for potential secrets/credentials added (lines starting with +)
    secret_patterns = [
        r"(?i)api[-_]?key\s*=\s*['\"][a-zA-Z0-9_\-\.]{16,}['\"]",
        r"(?i)password\s*=\s*['\"][a-zA-Z0-9_\-\.]{8,}['\"]",
        r"(?i)secret\s*=\s*['\"][a-zA-Z0-9_\-\.]{16,}['\"]",
        r"(?i)token\s*=\s*['\"][a-zA-Z0-9_\-\.]{16,}['\"]",
        r"AKIA[0-9A-Z]{16}", # AWS Access Key ID
        r"xox[bapr]-[0-9]{12}", # Slack tokens
        r"amqp://[a-zA-Z0-9_]+:[a-zA-Z0-9_]+@", # AMQP url credentials
        r"mongodb\+srv://[a-zA-Z0-9_]+:[a-zA-Z0-9_]+@", # MongoDB url credentials
        r"postgresql://[a-zA-Z0-9_]+:[a-zA-Z0-9_]+@", # Postgres url credentials
    ]

    findings = []
    current_file = ""

    for line in lines:
        if line.startswith("+++ b/"):
            current_file = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:].strip()
            # Skip comments or obvious mock tokens
            if "mock" in added_content.lower() or "dummy" in added_content.lower() or "fake" in added_content.lower():
                continue
            for pattern in secret_patterns:
                if re.search(pattern, added_content):
                    findings.append((current_file, added_content))
                    break

    if findings:
        print("❌ SECURITY ERROR: Detected potential credentials or secrets in staged code:", file=sys.stderr)
        for file, content in findings:
            print(f"  File: {file}\n  Line: {content}\n", file=sys.stderr)
        print("Please replace secrets with environment variables or mock tokens.", file=sys.stderr)
        sys.exit(1)

    print("✅ Security check passed. No secrets detected in staged changes.")
    sys.exit(0)

if __name__ == "__main__":
    main()
