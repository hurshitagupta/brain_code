import pytest

from brain_contract.brain_contract import AgentState
from decision_trace.decision_trace import DecisionTrace


def test_decision_trace_records_decisions():
    brain = DecisionTrace(max_steps=3)

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "complete"
    assert len(brain.decisions) == 3

    assert brain.decisions[0].step == 1
    assert brain.decisions[0].reason == "next action in the plan"

    assert brain.decisions[-1].action == "stop"
    assert brain.decisions[-1].reason == "plan completed"


def test_decision_trace_rejects_empty_goal():
    brain = DecisionTrace()

    state = AgentState(goal="")

    with pytest.raises(ValueError,match="goal cannot be empty"):
        brain.run(state)


def test_decision_trace_records_step_limit():
    brain = DecisionTrace(max_steps=1)

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "limit_reached"

    assert brain.decisions[-1].action == "stop"
    assert brain.decisions[-1].reason == "step limit reached"