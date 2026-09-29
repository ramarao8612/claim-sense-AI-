"""Structured summary generation (Guide Step 9).

LLMProvider is an adapter: today it talks to Ollama (free, local).
Tomorrow you swap in BedrockProvider without touching the API layer —
same .generate(prompt) interface.

The prompt forces JSON output: facts, policy provisions WITH citation ids,
missing items, conflicts, recommendation, limitations. Citations keep the
summary evidence-based per the SDD.
"""
import json

import httpx

from app.core.config import settings

SUMMARY_SCHEMA_HINT = """Return ONLY valid JSON with keys:
facts, policy_provisions[{text, citation_id}], missing_items, conflicts,
recommendation, limitations."""


class LLMProvider:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class OllamaProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        resp = httpx.post(
            f"{settings.ollama_host}/api/generate",
            json={"model": settings.ollama_model, "prompt": prompt,
                  "stream": False, "format": "json"},
            timeout=180,
        )
        resp.raise_for_status()
        return resp.json()["response"]


# TODO: class BedrockProvider(LLMProvider) for the AWS "pro" step.


def build_prompt(facts: list[dict], citations: list[dict], scores: dict) -> str:
    return f"""You are an insurance claim review assistant. Summarize the claim
for a human adjuster. Be factual, cite sources, flag uncertainty.

EXTRACTED FACTS (with document/page provenance):
{json.dumps(facts, indent=2)}

RETRIEVED POLICY PROVISIONS:
{json.dumps(citations, indent=2)}

SCORES:
{json.dumps(scores, indent=2)}

{SUMMARY_SCHEMA_HINT}"""


def summarize(facts, citations, scores, provider: LLMProvider | None = None) -> dict:
    provider = provider or OllamaProvider()
    raw = provider.generate(build_prompt(facts, citations, scores))
    return json.loads(raw)
