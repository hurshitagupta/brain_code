import time

from brain_contract.brain_contract import AgentState
from decision_trace.decision_trace import DecisionTrace


class TemporaryFailure(RuntimeError):
    """Used when an action fails temporarily."""


class BoundedFailure(DecisionTrace):

    def execute_with_retry(self, action: str) -> str:
        retry_count = 0

        while True:
            try:
                return self.execute_action(action)

            except TemporaryFailure as error:
                if retry_count >= self.max_retries:
                    raise error

                retry_count += 1

                self.record_decision(
                    step=retry_count,
                    action="retry",
                    reason=f"temporary failure: {error}",
                )

    def run(self, state: AgentState) -> AgentState:
        self.decisions = []
        self.validate_state(state)

        if not state.plan:
            state.plan = self.create_plan(state)

        start_time = time.perf_counter()
        step_count = 0

        while state.plan:

            if step_count >= self.max_steps:
                state.status = "limit_reached"

                self.record_decision(
                    step=step_count,
                    action="stop",
                    reason="step limit reached",
                )

                return state

            time_used = time.perf_counter() - start_time

            if time_used > self.timeout_seconds:
                state.status = "timeout"

                self.record_decision(
                    step=step_count,
                    action="stop",
                    reason="timeout reached",
                )

                return state

            current_action = state.plan.pop(0)

            self.record_decision(
                step=step_count + 1,
                action=current_action,
                reason="next action in the plan",
            )

            try:
                result = self.execute_with_retry(current_action)

            except TemporaryFailure as error:
                state.status = "failed"

                state.observations.append(
                    f"failed:{error}"
                )

                self.record_decision(
                    step=step_count + 1,
                    action="stop",
                    reason="retry limit reached",
                )

                return state

            state.observations.append(result)
            step_count += 1

        state.status = "complete"

        self.record_decision(
            step=step_count,
            action="stop",
            reason="plan completed",
        )

        return state


if __name__ == "__main__":
    brain = BoundedFailure(
        max_steps=3,
        timeout_seconds=2.0,
        max_retries=1,
    )

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    print("=== BOUNDED FAILURE ===")
    print(f"Goal: {result.goal}")
    print(f"Status: {result.status}")

    print("\nObservations:")
    for observation in result.observations:
        print(f"- {observation}")

    print("\nDecisions:")
    for decision in brain.decisions:
        print(
            f"Step {decision.step} | "
            f"Action: {decision.action} | "
            f"Reason: {decision.reason}"
        )