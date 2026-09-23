from dataclasses import dataclass

from brain_contract.brain_contract import AgentState
from control_loop.control_loop import ControlLoop


@dataclass
class Decision:
    step: int
    action: str
    reason: str


class DecisionTrace(ControlLoop):

    def __init__(self,max_steps= 3,timeout_seconds= 2.0,max_retries= 1,):
        super().__init__(max_steps=max_steps,timeout_seconds=timeout_seconds,max_retries=max_retries)

        self.decisions: list[Decision] = []

    def record_decision(self,step: int,action: str,reason: str,) -> None:
        decision = Decision(step=step,action=action,reason=reason)

        self.decisions.append(decision)

    def run(self, state: AgentState) -> AgentState:
        self.validate_state(state)

        if not state.plan:
            state.plan = self.create_plan(state)

        step_count = 0

        while state.plan:

            if step_count >= self.max_steps:
                state.status = "limit_reached"

                self.record_decision(step=step_count,action="stop",reason="step limit reached")

                return state

            current_action = state.plan.pop(0)

            self.record_decision(step=step_count + 1,action=current_action,reason="next action in the plan")

            result = self.execute_action(current_action)

            state.observations.append(result)

            step_count += 1

        state.status = "complete"

        self.record_decision(step=step_count,action="stop",reason="plan completed")

        return state


if __name__ == "__main__":
    brain = DecisionTrace(max_steps=3)

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    print("=== DECISION TRACE ===")
    print(f"Goal: {result.goal}")
    print(f"Status: {result.status}")

    print("\nDecisions:")

    for decision in brain.decisions:
        print(
            f"Step {decision.step} | "
            f"Action: {decision.action} | "
            f"Reason: {decision.reason}"
        )

    print("\nObservations:")

    for observation in result.observations:
        print(f"- {observation}")