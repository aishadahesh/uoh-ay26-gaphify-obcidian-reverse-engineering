"""Gemini-backed bug-finding agent for EX04 token-efficiency evidence."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone

from .gemini_artifacts import write_gemini_artifacts
from .gemini_prompt import AgentPrompt, build_agent_prompt

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


@dataclass(frozen=True)
class GeminiResult:
    mode: str
    model: str
    estimated_prompt_tokens: int
    response_text: str
    files_sent: tuple[str, ...]
    generated_at_utc: str


def run_gemini_agent(repo_root, mode: str = "minimal", model: str | None = None) -> GeminiResult:
    """Run Gemini on the selected prompt packet.

    Requires GEMINI_API_KEY in the environment and the optional google-genai
    dependency installed in the active virtual environment.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Copy .env.example to .env or set it in the shell.")
    prompt = build_agent_prompt(repo_root, mode)
    selected_model = model or os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Install google-genai in .venv to run Gemini: python -m pip install google-genai") from exc

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(model=selected_model, contents=prompt.prompt)
    except Exception as exc:
        response, selected_model = _retry_default_model_if_env_is_stale(
            client, prompt.prompt, selected_model, model, exc
        )
    return GeminiResult(
        prompt.mode,
        selected_model,
        prompt.estimated_tokens,
        response.text or "",
        prompt.files,
        datetime.now(timezone.utc).isoformat(),
    )


def _retry_default_model_if_env_is_stale(client, prompt: str, selected_model: str, explicit_model: str | None, exc: Exception):
    message = str(exc)
    is_missing = "NOT_FOUND" in message or "not found" in message
    if is_missing and explicit_model is None and selected_model != DEFAULT_GEMINI_MODEL:
        return client.models.generate_content(model=DEFAULT_GEMINI_MODEL, contents=prompt), DEFAULT_GEMINI_MODEL
    if is_missing:
        raise RuntimeError(
            f"Gemini model {selected_model!r} is not available for this API key. "
            f"Try `--model {DEFAULT_GEMINI_MODEL}` or run "
            "`python -m gaphify_re gemini-models --repo .` to see available models. "
            "If your .env has GEMINI_MODEL=gemini-1.5-flash, replace it with "
            f"GEMINI_MODEL={DEFAULT_GEMINI_MODEL}."
        ) from exc
    raise exc


def list_gemini_models() -> list[str]:
    """Return Gemini model names available to the configured API key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Set it before listing models.")
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Install google-genai in .venv: python -m pip install google-genai") from exc
    client = genai.Client(api_key=api_key)
    return sorted(model.name for model in client.models.list())
