"""WhiteGate edge-case tests for MultiTeamOrchestrator."""

from jarvis.critics import CriticVerdict

pytest_plugins = ["tests.fixtures.orchestrator"]


def test_white_gate_blocks_downstream_when_rejected(
    build_orchestrator_with_critic_outputs,
):
    """Red critic rejection blocks innovators from executing."""
    red_verdict = CriticVerdict(approved=False, fixes=[], risk=0.2, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    (
        orchestrator,
        black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_verdict, blue_verdict
    )
    orchestrator.run("test objective")
    assert not black_agent.called


def test_white_gate_allows_downstream_when_approved(
    build_orchestrator_with_critic_outputs,
):
    """Approval from both critics allows innovators to execute."""
    red_verdict = CriticVerdict(approved=True, fixes=[], risk=0.0, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    (
        orchestrator,
        black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_verdict, blue_verdict
    )
    orchestrator.run("test objective")
    assert black_agent.called


def test_white_gate_accepts_dict_outputs(
    build_orchestrator_with_critic_outputs,
):
    """Critic verdicts provided as dicts are converted appropriately."""
    red_dict = {"approved": True, "risk": 0.0, "notes": ""}
    blue_dict = {"approved": True, "risk": 0.1, "notes": ""}
    (
        orchestrator,
        black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_dict, blue_dict
    )
    result = orchestrator.run("objective")
    assert black_agent.called
    assert result["halt"] is False


def test_white_gate_handles_unexpected_output_type(
    build_orchestrator_with_critic_outputs,
):
    """Non-dict/non-verdict outputs cause rejection and halt."""
    red_output = "unexpected"
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    (
        orchestrator,
        black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_output, blue_verdict
    )
    result = orchestrator.run("objective")
    assert not black_agent.called
    assert result["halt"] is True
    assert (
        "Unsupported output type"
        in result["critics"]["white_gate"]["notes"]
    )


def test_white_gate_calls_security_quality_always(
    build_orchestrator_with_critic_outputs,
):
    """Security-quality agent should run regardless of approval status."""
    red_verdict = CriticVerdict(approved=False, fixes=[], risk=0.2, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    (
        orchestrator,
        _black_agent,
        white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_verdict, blue_verdict
    )
    orchestrator.run("objective")
    assert white_agent.called


def test_white_gate_defaults_missing_fields(
    build_orchestrator_with_critic_outputs,
):
    """Missing fields default to rejection without crashing."""
    red_dict = {}
    blue_dict = {"risk": 0.0}
    (
        orchestrator,
        black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_dict, blue_dict
    )
    result = orchestrator.run("objective")
    assert not black_agent.called
    assert result["halt"] is True


def test_white_gate_handles_malformed_verdict(
    build_orchestrator_with_critic_outputs,
):
    """Invalid field types result in rejection and safe defaults."""
    red_dict = {"approved": True, "risk": "high"}
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=0.1, notes="")
    (
        orchestrator,
        black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_dict, blue_verdict
    )
    result = orchestrator.run("objective")
    assert not black_agent.called
    assert result["halt"] is True
    notes = result["critics"]["white_gate"]["notes"]
    assert "Malformed verdict structure" in notes
    assert result["critics"]["white_gate"]["risk"] == 1.0


def test_white_gate_propagates_critic_notes(
    build_orchestrator_with_critic_outputs,
):
    """Notes from both critics surface in merged verdict."""
    red_verdict = CriticVerdict(
        approved=True, fixes=[], risk=0.0, notes="red note"
    )
    blue_verdict = CriticVerdict(
        approved=True, fixes=[], risk=0.0, notes="blue note"
    )
    (
        orchestrator,
        _black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_verdict, blue_verdict
    )
    result = orchestrator.run("objective")
    notes = result["critics"]["white_gate"]["notes"]
    assert "red note" in notes
    assert "blue note" in notes


def test_white_gate_handles_extreme_risk(
    build_orchestrator_with_critic_outputs,
):
    """High risk scores halt workflow and surface the risk."""
    red_verdict = CriticVerdict(approved=True, fixes=[], risk=0.0, notes="")
    blue_verdict = CriticVerdict(approved=True, fixes=[], risk=10.0, notes="")
    (
        orchestrator,
        black_agent,
        _white_agent,
    ) = build_orchestrator_with_critic_outputs(
        red_verdict, blue_verdict
    )
    result = orchestrator.run("objective")
    assert not black_agent.called
    assert result["halt"] is True
    assert result["critics"]["white_gate"]["risk"] == 10.0
