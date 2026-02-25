import logging
import os
import re

from antigravity_architect.core.engine import AntigravityEngine
from antigravity_architect.resources.constants import AGENT_DIR, CLASSIFICATION_RULES, TECH_ALIASES
from antigravity_architect.resources.templates import GITIGNORE_MAP


class AntigravityAssimilator:
    """
    Intelligent brain dump parsing and knowledge distribution.

    This class handles the "Assimilator" feature - parsing large text dumps,
    categorizing content using heuristics, and distributing it to appropriate
    .agent/ directories based on detected content type.
    All methods are static as they don't require instance state.
    """

    @staticmethod
    def detect_tech_stack(text: str) -> list[str]:
        """
        Intelligently detects technology keywords using primary keys and aliases.
        """
        detected = set()
        text_lower = text.lower()

        # Check primary keywords from mappings
        primary_sources = set(GITIGNORE_MAP.keys()) | set(TECH_ALIASES.keys())

        for k in primary_sources:
            if re.search(r"\b" + re.escape(k) + r"\b", text_lower):
                detected.add(k)

        # Check aliases for deeper detection
        for primary, aliases in TECH_ALIASES.items():
            for alias in aliases:
                if re.search(r"\b" + re.escape(alias) + r"\b", text_lower):
                    detected.add(primary)
                    break

        return list(detected)

    @staticmethod
    def build_tech_deep_dive(keywords: list[str], full_text: str) -> str:
        """
        Generates a deep-dive TECH_STACK.md based on detected keywords and text analysis.
        """
        content = "# 🛠️ Technical Stack Deep-Dive\n\n"
        content += "## 🚀 Primary Technologies\n"
        for k in sorted(keywords):
            content += f"- **{k.title()}**\n"

        content += "\n## 🔍 Contextual Observations\n"
        text_lower = full_text.lower()

        observation_map = {
            "architecture": "Structural architectural specifications detected.",
            "security": "Security-sensitive components or requirements identified.",
            "auth": "Security-sensitive components or requirements identified.",
            "database": "Data persistence layers identified.",
            "sql": "Data persistence layers identified.",
            "api": "API surfaces or integrations identified.",
            "endpoint": "API surfaces or integrations identified.",
        }

        observations = set()
        for key, obs in observation_map.items():
            if key in text_lower:
                observations.add(obs)

        if observations:
            for obs in sorted(observations):
                content += f"- {obs}\n"
        else:
            content += "- Standard project structure with generic tech stack.\n"

        content += "\n## ⚠️ Technical Debt & Tracking\n"
        debt_keywords = ["todo", "fixme", "refactor", "deprecated", "legacy", "optimization needed"]
        debts = [k for k in debt_keywords if k in text_lower]

        if debts:
            content += "Potential technical debt or optimization areas identified:\n"
            for d in debts:
                content += f"- {d.title()}\n"
        else:
            content += "No immediate technical debt keywords identified in source documents.\n"

        content += "\n## 🤖 Agent Interaction Map\n"
        content += "Agents should prioritize rules in `.agent/rules/` and use `TECH_STACK.md` as the primary architectural reference.\n"

        return content

    @staticmethod
    def identify_category(text: str) -> str:
        """
        Uses heuristics to decide if text is a Rule, Workflow, Skill, or Doc.

        Returns the category with the highest keyword match score.
        """
        text_lower = text.lower()
        scores: dict[str, int] = dict.fromkeys(CLASSIFICATION_RULES, 0)

        for category, keywords in CLASSIFICATION_RULES.items():
            for k in keywords:
                scores[category] += len(re.findall(r"\b" + re.escape(k) + r"\b", text_lower))

        best_cat = max(scores, key=lambda x: scores[x])
        if scores[best_cat] == 0:
            return "docs"
        return best_cat

    @staticmethod
    def get_destination_path(base_dir: str, category: str, safe_title: str) -> str:
        """Determines the file destination based on category."""
        category_paths: dict[str, str] = {
            "rules": os.path.join(base_dir, AGENT_DIR, "rules", f"imported_{safe_title}.md"),
            "workflows": os.path.join(base_dir, AGENT_DIR, "workflows", f"imported_{safe_title}.md"),
            "skills": os.path.join(base_dir, AGENT_DIR, "skills", f"imported_{safe_title}", "SKILL.md"),
            "docs": os.path.join(base_dir, "docs", "imported", f"{safe_title}.md"),
        }
        return category_paths.get(category, category_paths["docs"])

    @staticmethod
    def process_brain_dump(filepath: str | None, base_dir: str) -> list[str]:
        """
        Reads a brain dump file, splits by headers, and distributes to .agent/ folders.

        Returns a list of detected technology keywords from the content.
        """
        if not AntigravityEngine.validate_file_path(filepath):
            return []

        # Type narrowing: after validation, filepath is confirmed to be str
        assert filepath is not None

        logging.info(f"🧠 Assimilating knowledge from: {filepath}...")

        try:
            with open(filepath, encoding="utf-8", errors="replace") as f:
                full_text = f.read()
        except Exception as e:
            logging.error(f"Could not read brain dump: {e}")
            return []

        # 1. Archive Raw Content
        raw_dest = os.path.join(base_dir, "context", "raw", "master_brain_dump.md")
        AntigravityEngine.write_file(raw_dest, full_text, exist_ok=True)

        # 2. Extract Tech Stack Keywords
        detected_keywords = AntigravityAssimilator.detect_tech_stack(full_text)
        logging.info(f"🔍 Detected Tech Stack from Source: {', '.join(detected_keywords)}")

        # 3. Generate TECH_STACK.md (The Documentation Genie)
        tech_stack_path = os.path.join(base_dir, "docs", "TECH_STACK.md")
        tech_stack_content = AntigravityAssimilator.build_tech_deep_dive(detected_keywords, full_text)
        AntigravityEngine.write_file(tech_stack_path, tech_stack_content, exist_ok=True)

        # 4. Split & Distribute
        sections = re.split(r"(^#+\s+.*$)", full_text, flags=re.MULTILINE)

        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break
            header = sections[i].strip()
            content = sections[i + 1].strip()
            if not content:
                continue

            category = AntigravityAssimilator.identify_category(header + "\n" + content)
            safe_title = AntigravityEngine.slugify_title(header)
            dest = AntigravityAssimilator.get_destination_path(base_dir, category, safe_title)

            formatted = f"<!-- Auto-Assimilated Source -->\n\n{header}\n\n{content}"
            AntigravityEngine.append_file(dest, formatted)

        logging.info("🧠 Assimilation Complete.")
        return detected_keywords
