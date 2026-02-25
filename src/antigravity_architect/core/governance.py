import json
import os


class AntigravityGovernance:
    """Phase 16: Security & Governance - Handles licenses and safety checks."""

    @staticmethod
    def scan_licenses(base_dir: str) -> dict[str, str]:
        """Scans for dependency licenses and identifies potential conflicts."""
        # Simple mapping for demonstration; in production would use pkg_resources
        conflicts = {}
        # Placeholder logic: scan requirements.txt for known GPL libs
        req_path = os.path.join(base_dir, "requirements.txt")
        if os.path.exists(req_path):
            with open(req_path) as f:
                for line in f:
                    if "gpl" in line.lower():
                        conflicts["GPL Conflict"] = f"Detected potentially incompatible license in: {line.strip()}"

        return conflicts

    @staticmethod
    def generate_sbom(base_dir: str, project_name: str) -> str:
        """Generates a minimal CycloneDX-style SBOM in JSON format."""
        from typing import Any

        sbom: dict[str, Any] = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "metadata": {"component": {"name": project_name, "type": "application"}},
            "components": [],
        }

        # Discover components from requirements.txt
        req_path = os.path.join(base_dir, "requirements.txt")
        if os.path.exists(req_path):
            with open(req_path) as f:
                for line in f:
                    if "==" in line:
                        name, version = line.strip().split("==")
                        sbom["components"].append({"name": name, "version": version, "type": "library"})

        return json.dumps(sbom, indent=2)

    @staticmethod
    def validate_env_schema(base_dir: str) -> list[str]:
        """Enforces .env.schema compliance."""
        errors = []
        schema_path = os.path.join(base_dir, ".env.schema")
        env_path = os.path.join(base_dir, ".env")

        if not os.path.exists(schema_path):
            return []

        required_vars = []
        with open(schema_path) as f:
            required_vars = [line.split("=")[0].strip() for line in f if "=" in line]

        current_vars: set[str] = set()
        if os.path.exists(env_path):
            with open(env_path) as f:
                current_vars = {line.split("=")[0].strip() for line in f if "=" in line}

        for var in required_vars:
            if var not in current_vars:
                errors.append(f"❌ Missing required environment variable: {var}")

        return errors
