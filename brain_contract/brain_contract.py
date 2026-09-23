from dataclasses import dataclass, field
import time


@dataclass
class AgentState:
    goal: str
    plan: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    status: str = "running"


class Brain:
    def __init__(self, max_steps=3, timeout_seconds= 2.0, max_retries=1,):
        if max_steps <= 0:
            raise ValueError("max_steps must be greater than 0")

        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than 0")

        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")

        self.max_steps = max_steps
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    def validate_state(self, state: AgentState) -> None:
        if not isinstance(state, AgentState):
            raise TypeError("state must be an AgentState")

        if not state.goal.strip():
            raise ValueError("goal cannot be empty")

    def create_plan(self, state: AgentState) -> list[str]:
        return [
            f"inspect goal: {state.goal}",
            f"process goal: {state.goal}",
        ]

    def execute_action(self, action: str) -> str:
        return f"executed:{action}"

    def run(self, state: AgentState) -> AgentState:
        self.validate_state(state)

        start_time = time.perf_counter()

        if not state.plan:
            state.plan = self.create_plan(state)

        retries = 0

        for step in range(1, self.max_steps + 1):

            time_used = time.perf_counter() - start_time

            if time_used > self.timeout_seconds:
                state.status = "timeout"
                state.observations.append("brain stopped: timeout reached")
                return state

            if not state.plan:
                state.status = "complete"
                return state

            action = state.plan.pop(0)

            try:
                observation = self.execute_action(action)
                state.observations.append(observation)

            except RuntimeError as error:
                if retries < self.max_retries:
                    retries += 1
                    state.plan.insert(0, action)
                    state.observations.append(f"retry:{retries}:{error}")
                    continue

                state.status = "failed"
                state.observations.append(f"failed:{error}")
                return state

            if not state.plan:
                state.status = "complete"
                return state

        state.status = "limit_reached"
        return state


if __name__ == "__main__":
    brain = Brain()

    state = AgentState(goal="explain agent state")

    result = brain.run(state)

    print("=== AGENT BRAIN ===")
    print(f"Goal: {result.goal}")
    print(f"Status: {result.status}")
    print(f"Remaining plan: {result.plan}")

    print("\nObservations:")
    for observation in result.observations:
        print(f"- {observation}")