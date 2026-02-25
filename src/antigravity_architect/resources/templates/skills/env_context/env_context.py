# Antigravity Environment Detector
import os
import platform
import sys


def detect() -> None:
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Shell: {os.environ.get('SHELL', os.environ.get('COMSPEC', 'Unknown'))}")
    print(f"Python: {sys.version.split(' ')[0]}")
    print(f"Venv: {os.environ.get('VIRTUAL_ENV', 'None')}")
    print(f"In Docker: {os.path.exists('/.dockerenv')}")


if __name__ == "__main__":
    detect()
