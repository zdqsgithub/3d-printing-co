#!/usr/bin/env python3
"""
Test Specs — Validates SKILL.md structure and helper script functionality
for all 9 nanobot skills across 3 solutions.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_ROOT = PROJECT_ROOT / "skills"

# All 9 skills with their paths
SKILL_PATHS = [
    ("sales-support/product-recommender", True),   # has scripts
    ("sales-support/order-quote", True),
    ("sales-support/faq-troubleshooting", False),   # no scripts
    ("inventory-forecasting/stock-monitor", True),
    ("inventory-forecasting/trend-analysis", True),
    ("inventory-forecasting/alert-report", True),
    ("marketing-leadgen/lead-discovery", True),
    ("marketing-leadgen/content-generation", True),
    ("marketing-leadgen/outreach-scheduler", True),
]


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from SKILL.md content."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


class TestSkillStructure:
    """Validate that all SKILL.md files have correct structure."""

    @pytest.mark.parametrize("skill_path,_", SKILL_PATHS)
    def test_skill_md_exists(self, skill_path, _):
        """Each skill directory must contain a SKILL.md file."""
        skill_file = SKILLS_ROOT / skill_path / "SKILL.md"
        assert skill_file.exists(), f"SKILL.md not found at {skill_file}"

    @pytest.mark.parametrize("skill_path,_", SKILL_PATHS)
    def test_valid_frontmatter(self, skill_path, _):
        """SKILL.md must have valid YAML frontmatter with name and description."""
        skill_file = SKILLS_ROOT / skill_path / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        assert "name" in fm, f"Missing 'name' in frontmatter of {skill_path}"
        assert "description" in fm, f"Missing 'description' in frontmatter of {skill_path}"
        assert len(fm["name"]) > 0, "Skill name cannot be empty"
        assert len(fm["description"]) > 10, "Skill description should be meaningful"

    @pytest.mark.parametrize("skill_path,_", SKILL_PATHS)
    def test_has_metadata(self, skill_path, _):
        """SKILL.md frontmatter must include nanobot metadata."""
        skill_file = SKILLS_ROOT / skill_path / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        assert "metadata" in fm, f"Missing 'metadata' in frontmatter of {skill_path}"
        meta = json.loads(fm["metadata"])
        assert "nanobot" in meta, "Metadata must contain 'nanobot' key"

    @pytest.mark.parametrize("skill_path,_", SKILL_PATHS)
    def test_has_spec_section(self, skill_path, _):
        """SKILL.md must contain a Spec section with Inputs, Outputs, Constraints."""
        skill_file = SKILLS_ROOT / skill_path / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        assert "## Spec" in content or "### Inputs" in content, f"Missing Spec section in {skill_path}"
        assert "### Inputs" in content or "Inputs" in content, f"Missing Inputs in {skill_path}"
        assert "### Outputs" in content or "Outputs" in content, f"Missing Outputs in {skill_path}"
        assert "### Constraints" in content or "Constraints" in content, f"Missing Constraints in {skill_path}"

    @pytest.mark.parametrize("skill_path,_", SKILL_PATHS)
    def test_has_edge_cases(self, skill_path, _):
        """SKILL.md must document edge cases."""
        skill_file = SKILLS_ROOT / skill_path / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        assert "Edge Case" in content or "edge case" in content.lower(), f"Missing Edge Cases in {skill_path}"

    @pytest.mark.parametrize("skill_path,_", SKILL_PATHS)
    def test_has_usage_section(self, skill_path, _):
        """SKILL.md must contain usage instructions."""
        skill_file = SKILLS_ROOT / skill_path / "SKILL.md"
        content = skill_file.read_text(encoding="utf-8")
        assert "## Usage" in content or "## Cron" in content or "usage" in content.lower(), \
            f"Missing Usage section in {skill_path}"


class TestResources:
    """Validate resource files."""

    def test_catalog_json_valid(self):
        """Product catalog must be valid JSON with required fields."""
        catalog_path = SKILLS_ROOT / "sales-support/product-recommender/resources/catalog.json"
        assert catalog_path.exists()
        with open(catalog_path, encoding="utf-8") as f:
            catalog = json.load(f)
        assert isinstance(catalog, list)
        assert len(catalog) > 0
        for product in catalog:
            assert "id" in product
            assert "name" in product
            assert "category" in product
            assert "price" in product
            assert isinstance(product["price"], (int, float))
            assert product["price"] > 0

    def test_faq_json_valid(self):
        """FAQ knowledge base must be valid JSON with required fields."""
        faq_path = SKILLS_ROOT / "sales-support/faq-troubleshooting/resources/faq_knowledge_base.json"
        assert faq_path.exists()
        with open(faq_path, encoding="utf-8") as f:
            faqs = json.load(f)
        assert isinstance(faqs, list)
        assert len(faqs) > 0
        for faq in faqs:
            assert "id" in faq
            assert "question" in faq
            assert "answer" in faq
            assert len(faq["answer"]) > 20


class TestScripts:
    """Validate that helper scripts are syntactically correct and accept --help."""

    SCRIPTS = [
        "sales-support/product-recommender/scripts/product_catalog.py",
        "sales-support/order-quote/scripts/quote_calculator.py",
        "inventory-forecasting/stock-monitor/scripts/inventory_poller.py",
        "inventory-forecasting/trend-analysis/scripts/trend_analyzer.py",
        "inventory-forecasting/alert-report/scripts/report_generator.py",
        "marketing-leadgen/lead-discovery/scripts/lead_finder.py",
        "marketing-leadgen/content-generation/scripts/content_drafter.py",
        "marketing-leadgen/outreach-scheduler/scripts/outreach_manager.py",
    ]

    @pytest.mark.parametrize("script_path", SCRIPTS)
    def test_script_exists(self, script_path):
        """Helper script must exist."""
        full_path = SKILLS_ROOT / script_path
        assert full_path.exists(), f"Script not found: {full_path}"

    @pytest.mark.parametrize("script_path", SCRIPTS)
    def test_script_syntax(self, script_path):
        """Helper script must have valid Python syntax."""
        full_path = SKILLS_ROOT / script_path
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(full_path)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Syntax error in {script_path}: {result.stderr}"

    @pytest.mark.parametrize("script_path", SCRIPTS)
    def test_script_help(self, script_path):
        """Helper script must accept --help without crashing."""
        full_path = SKILLS_ROOT / script_path
        result = subprocess.run(
            [sys.executable, str(full_path), "--help"],
            capture_output=True, text=True, timeout=10
        )
        assert result.returncode == 0, f"--help failed for {script_path}: {result.stderr}"
        assert "usage" in result.stdout.lower() or "options" in result.stdout.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
