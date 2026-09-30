"""Proof of concept for validating AI-generated output.

This test deliberately uses a local stub instead of an API call. Replace
``judge_llm_response`` with a real judge client when evaluating live output.
"""

import pytest


@pytest.mark.ai
def test_ai_output_quality_poc():
    """Demonstrate structural, rubric, and LLM-as-judge validation layers."""

    generated_output = (
        "The audit found that the database password was exposed in a log file. "
        "Risk rating: high. Rotate the credential, remove the sensitive log, "
        "and review access controls."
    )

    # 1. Structural check: reject empty or suspiciously short responses.
    assert len(generated_output) > 50

    # 2. Rubric check: verify that the response includes required content.
    assert "risk rating" in generated_output.lower()

    # 3. LLM-as-judge seam: a real implementation can call a separate model.
    score = judge_llm_response(
        response=generated_output,
        rubric="Does this correctly summarize the audit finding without inventing facts?",
    )
    assert score >= 0.8


def judge_llm_response(*, response: str, rubric: str) -> float:
    """Return a deterministic stand-in score for this validation POC.

    A production version would send ``response`` and ``rubric`` to a separate
    evaluator model and parse its structured score.
    """

    if response.strip() and rubric.strip() and "risk rating" in response.lower():
        return 0.95
    return 0.0
