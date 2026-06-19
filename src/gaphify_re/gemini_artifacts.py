"""Artifact writers for Gemini-backed debugging runs."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gemini_agent import GeminiResult


def write_gemini_artifacts(repo_root: Path, result: GeminiResult) -> tuple[Path, Path]:
    """Persist the latest Gemini agent run as JSON and Markdown evidence."""
    artifacts_dir = repo_root / "artifacts"
    reports_dir = repo_root / "reports"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    json_path = artifacts_dir / "gemini_agent_result.json"
    md_path = reports_dir / "GEMINI_AGENT_REPORT.md"
    json_path.write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
    md_path.write_text(_format_markdown_report(result), encoding="utf-8")
    return json_path, md_path


def _format_markdown_report(result: GeminiResult) -> str:
    files = "\n".join(f"- `{name}`" for name in result.files_sent)
    return f"""# Gemini Agent Report

Generated at: `{result.generated_at_utc}`

| Field | Value |
|---|---|
| Mode | `{result.mode}` |
| Model | `{result.model}` |
| Estimated prompt tokens | `{result.estimated_prompt_tokens}` |
| Files sent | `{len(result.files_sent)}` |

## Files Sent To Gemini

{files}

## Agent Output

{result.response_text}
"""
