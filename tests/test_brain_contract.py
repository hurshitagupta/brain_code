import pytest

from brain_contract.brain_contract import AgentState, Brain


def test_brain_completes_valid_goal():
    brain = Brain()

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "complete"
    assert len(result.observations) == 2
    assert result.plan == []


def test_brain_rejects_empty_goal():
    brain = Brain()

    state = AgentState(goal="")

    with pytest.raises(ValueError,match="goal cannot be empty"):
        brain.run(state)


def test_brain_respects_step_limit():
    brain = Brain(max_steps=1)

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "limit_reached"
    assert len(result.observations) == 1