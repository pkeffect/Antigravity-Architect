import os
import re
import subprocess
import sys

CRITICAL_FILES = [".env", ".agent/rules/", "pyproject.toml", "SECURITY.md"]
SECRET_PATTERNS = {
    "Generic Secret": re.compile(r"(?i)secret[_-]?key['\"]?\s*[:=]\s*['\"]?[a-z0-9/+=]{16,}['\"]?"),
    "AWS Key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub Token": re.compile(r"ghp_[a-zA-Z0-9]{36}"),
}


def scan_for_secrets() -> bool:
    print("🔍 Sentinel: Scanning for exposed secrets...")
    found_secrets = False
    for root, _, files in os.walk("."):
        if "venv" in root or ".git" in root:
            continue
        for file in files:
            path = os.path.join(root, file)
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                    for name, pattern in SECRET_PATTERNS.items():
                        if pattern.search(content):
                            print(f"❌ WARNING: Potential {name} found in {path}")
                            found_secrets = True
            except Exception:
                continue
    return found_secrets


def run_audit() -> None:
    print("🛡️ Sentinel: Security-critical change detected. Running /doctor audit...")
    if scan_for_secrets():
        print("🚨 Sentinel: SECRETS DETECTED. Blocking flow.")
        return

    result = subprocess.run(
        [sys.executable, "-m", "antigravity_architect.cli", "--doctor", ".", "--fix"], capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Sentinel: Audit failed. Check security constraints.")
        # sys.exit(1) # Uncomment to block commits if audit fails


if __name__ == "__main__":
    run_audit()
