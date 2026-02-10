#!/usr/bin/env python3
# Antigravity Sentinel: Proactive Security Auditor
import os
import subprocess
import sys

CRITICAL_FILES = [".env", ".agent/rules/", "antigravity_master_setup.py", "SECURITY.md"]


def run_audit():
    print("🛡️ Sentinel: Security-critical change detected. Running /doctor audit...")
    result = subprocess.run(
        ["python", "antigravity_master_setup.py", "--doctor", ".", "--fix"], capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Sentinel: Audit failed. Check security constraints.")
        # sys.exit(1) # Uncomment to block commits if audit fails


if __name__ == "__main__":
    run_audit()
