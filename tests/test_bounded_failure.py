import time

from brain_contract.brain_contract import AgentState
from bounded_failure.bounded_failure import BoundedFailure, TemporaryFailure



def test_bounded_failure_happy_path():
    brain = BoundedFailure()

    state = AgentState( goal="explain agent state")

    result = brain.run(state)

    assert result.status == "complete"
    assert result.plan == []


def test_temporary_failure_retries_then_succeeds():
    brain = BoundedFailure(max_retries=1)

    call_count = 0

    def fail_once(action: str) -> str:
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            raise TemporaryFailure("service temporarily unavailable")

        return f"executed:{action}"

    brain.execute_action = fail_once

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "complete"
    assert call_count == 3

    assert any(decision.action == "retry" for decision in brain.decisions)


def test_retry_limit_stops_failure():
    brain = BoundedFailure(max_retries=1)

    def always_fail(action: str) -> str:
        raise TemporaryFailure("service temporarily unavailable")

    brain.execute_action = always_fail

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "failed"

    assert brain.decisions[-1].reason == ("retry limit reached")


def test_timeout_stops_execution():
    brain = BoundedFailure(timeout_seconds=0.01)

    def slow_action(action: str) -> str:
        time.sleep(0.02)
        return f"executed:{action}"

    brain.execute_action = slow_action

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "timeout"

    assert brain.decisions[-1].reason == ("timeout reached")


def test_step_limit_stops_execution():
    brain = BoundedFailure(max_steps=1)

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    assert result.status == "limit_reached"

    assert brain.decisions[-1].reason == ("step limit reached")