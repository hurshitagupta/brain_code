from brain_contract.brain_contract import AgentState, Brain

class ControlLoop(Brain):

    def run(self, state: AgentState) -> AgentState:
        self.validate_state(state)

        if not state.plan:
            state.plan = self.create_plan(state)

        step_count = 0

        while state.plan:

            if step_count >= self.max_steps:
                state.status = "limit_reached"
                state.observations.append("control loop stopped: step limit reached")
                return state

            current_action = state.plan.pop(0)

            result = self.execute_action(current_action)

            state.observations.append(result)

            step_count += 1

        state.status = "complete"
        return state


if __name__ == "__main__":
    loop = ControlLoop(max_steps=3)

    state = AgentState(goal="explain agent state")

    result = loop.run(state)

    print("=== CONTROL LOOP ===")
    print(f"Goal: {result.goal}")
    print(f"Status: {result.status}")
    print(f"Steps used: {len(result.observations)}")

    print("\nObservations:")
    for observation in result.observations:
        print(f"- {observation}")