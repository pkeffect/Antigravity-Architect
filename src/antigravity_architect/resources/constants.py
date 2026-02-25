from pathlib import Path

VERSION = "3.0.1"

# Core Directories
AGENT_DIR = ".agent"
ANTIGRAVITY_DIR_NAME = ".antigravity"
PRESETS_DIR = Path.home() / ANTIGRAVITY_DIR_NAME / "presets"
KNOWLEDGE_LAKE_DIR = Path.home() / ANTIGRAVITY_DIR_NAME / "knowledge_lake"

# Filename Constants
GITIGNORE_FILE = ".gitignore"
README_FILE = "README.md"
ENV_EXAMPLE_FILE = ".env.example"
LICENSE_FILE = "LICENSE"
CHANGELOG_FILE = "CHANGELOG.md"
CONTRIBUTING_FILE = "CONTRIBUTING.md"
AUDIT_FILE = "AUDIT.md"
SECURITY_FILE = "SECURITY.md"
CODE_OF_CONDUCT_FILE = "CODE_OF_CONDUCT.md"
BOOTSTRAP_FILE = "BOOTSTRAP_INSTRUCTIONS.md"
AGENT_MANIFEST = "manifest.json"

RULE_ARCHITECTURE = "05_architecture.md"
RULE_SECURITY_EXPERT = "07_security_expert.md"
RULE_IDENTITY = "00_identity.md"
RULE_TECH_STACK = "01_tech_stack.md"
RULE_SECURITY = "02_security.md"

# UI Constants
SEPARATOR = "=========================================="

# Alias Mapping for Intelligent Tech Detection
TECH_ALIASES: dict[str, list[str]] = {
    "python": [
        "django",
        "flask",
        "fastapi",
        "numpy",
        "pandas",
        "pytorch",
        "tensorflow",
        "scipy",
        "pytest",
        "poetry",
    ],
    "node": [
        "javascript",
        "typescript",
        "react",
        "vue",
        "svelte",
        "sveltekit",
        "nextjs",
        "express",
        "nest",
        "npm",
        "yarn",
        "pnpm",
    ],
    "docker": ["container", "dockerfile", "docker-compose", "kubernetes", "k8s"],
    "sql": ["postgres", "postgresql", "sqlite", "mysql", "mariadb", "oracle", "db2"],
    "cloud": ["aws", "azure", "gcp", "google cloud", "lambda", "s3", "ec2"],
}

# Heuristic Classification Keywords
CLASSIFICATION_RULES: dict[str, list[str]] = {
    "rules": [
        "always",
        "never",
        "must",
        "style",
        "convention",
        "standard",
        "protocol",
        "policy",
        "lint",
        "formatting",
        "security",
    ],
    "workflows": [
        "step",
        "guide",
        "process",
        "workflow",
        "how-to",
        "deploy",
        "setup",
        "run",
        "execution",
        "plan",
        "roadmap",
    ],
    "skills": [
        "command",
        "cli",
        "tool",
        "usage",
        "utility",
        "script",
        "automation",
        "flags",
        "arguments",
        "terminal",
    ],
    "docs": ["overview", "architecture", "introduction", "background", "context", "diagram", "concept", "summary"],
}
