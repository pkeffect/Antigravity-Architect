import os
import sys
import subprocess
import logging

# ==============================================================================
# 🛡️ Antigravity Sentinel (v1.6.2)
# ==============================================================================
# This script monitors critical files for unauthorized changes and triggers
# automated security audits via the /doctor command.

CRITICAL_FILES = [
    ".env",
    ".agent/rules/02_security.md",
    "antigravity_master_setup.py",
    "scripts/sentinel.py"
]

def run_audit():
    logging.info("🕵️ Sentinel: Triggering Security Audit...")
    try:
        # Run the doctor command on the current directory
        # We assume the master script is in the same or parent directory
        script_path = "antigravity_master_setup.py"
        if os.path.exists(script_path):
            result = subprocess.run(
                [sys.executable, script_path, "--doctor", ".", "--fix"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.returncode == 0:
                logging.info("✅ Sentinel: Audit completed successfully.")
            else:
                logging.error(f"❌ Sentinel: Audit failed with exit code {result.returncode}")
        else:
            logging.error("❌ Sentinel: Could not find antigravity_master_setup.py")
    except Exception as e:
        logging.error(f"❌ Sentinel: Audit exception: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    run_audit()
