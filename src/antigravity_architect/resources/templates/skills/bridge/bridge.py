# Antigravity Skill Bridge
# Standardized execution runner for AI agent skills.
import subprocess


def run_skill(command: str) -> subprocess.CompletedProcess:
    """Run a skill command using subprocess."""
    return subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
