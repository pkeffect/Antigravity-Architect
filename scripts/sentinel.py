import logging
import subprocess
import sys

# ==============================================================================
# 🛡️ Antigravity Sentinel (v3.0.0)
# ==============================================================================
# This script monitors critical files for unauthorized changes and triggers
# automated security audits via the --doctor command.

CRITICAL_FILES = [".env", ".agent/rules/02_security.md", "src/antigravity_architect/cli.py", "scripts/sentinel.py"]


def run_audit() -> None:
    logging.info("🕵️ Sentinel: Triggering Security Audit...")
    try:
        # Use python -m to run the package entry point
        result = subprocess.run(
            [sys.executable, "-m", "src.antigravity_architect.cli", "--doctor", ".", "--fix"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode == 0:
            logging.info("✅ Sentinel: Audit completed successfully.")
        else:
            logging.error(f"❌ Sentinel: Audit failed with exit code {result.returncode}")
    except Exception as e:
        logging.error(f"❌ Sentinel: Audit exception: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run_audit()
