import pytest

from brain_contract.brain_contract import AgentState
from control_loop.control_loop import ControlLoop


def test_control_loop_completes_plan():
    loop = ControlLoop(max_steps=3)

    state = AgentState(goal="explain agent state")

    result = loop.run(state)

    assert result.status == "complete"
    assert len(result.observations) == 2
    assert result.plan == []


def test_control_loop_rejects_empty_goal():
    loop = ControlLoop()

    state = AgentState(goal="")

    with pytest.raises(ValueError,match="goal cannot be empty"):
        loop.run(state)


def test_control_loop_stops_at_step_limit():
    loop = ControlLoop(max_steps=1)

    state = AgentState(goal="explain agent state")

    result = loop.run(state)

    assert result.status == "limit_reached"
    assert len(result.observations) == 2
    assert len(result.plan) == 1