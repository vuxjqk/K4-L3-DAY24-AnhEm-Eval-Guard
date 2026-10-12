"""The imported evaluator uses Gemini; Phase A should not require an OpenAI key."""
from unittest.mock import Mock

import pytest

from scripts import run_experiments

pytestmark = pytest.mark.student


def test_phase_a_accepts_only_its_evaluator_key(monkeypatch):
    monkeypatch.setattr(run_experiments, "OPENAI_API_KEY", "")
    monkeypatch.setattr(run_experiments, "GEMINI_API_KEY", "fake-test-key")
    runner = Mock()
    monkeypatch.setattr(run_experiments, "run_phase_a", runner)
    assert run_experiments.main(["--phase", "a", "--live"]) == 0
    runner.assert_called_once_with()


def test_phase_a_rejects_missing_gemini_before_running(monkeypatch, capsys):
    monkeypatch.setattr(run_experiments, "OPENAI_API_KEY", "fake-unrelated-key")
    monkeypatch.setattr(run_experiments, "GEMINI_API_KEY", "")
    runner = Mock()
    monkeypatch.setattr(run_experiments, "run_phase_a", runner)
    with pytest.raises(SystemExit) as error:
        run_experiments.main(["--phase", "a", "--live"])
    assert error.value.code == 2
    assert "GEMINI_API_KEY" in capsys.readouterr().err
    runner.assert_not_called()


def test_phase_b_still_requires_openai_key(monkeypatch, capsys):
    monkeypatch.setattr(run_experiments, "OPENAI_API_KEY", "")
    monkeypatch.setattr(run_experiments, "GEMINI_API_KEY", "fake-unrelated-key")
    with pytest.raises(SystemExit) as error:
        run_experiments.main(["--phase", "b", "--live"])
    assert error.value.code == 2
    assert "OPENAI_API_KEY" in capsys.readouterr().err
