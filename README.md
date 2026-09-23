# Implement Brain in Code

This project implements the basic "brain" of an AI agent using Python.

The brain acts as a coordinator. It receives the current agent state, creates a plan, executes actions, records what happened, and decides when to stop.

---

## Task 1 — State/Brain Contract

### Objective

The goal of this task is to create a clear connection between the agent's state and the brain.

The `AgentState` stores information about the current execution:

- `goal` — what the agent needs to achieve
- `plan` — actions that still need to be completed
- `observations` — results of actions that have already been executed
- `status` — current state such as `running`, `complete`, `failed`, or `limit_reached`

The `Brain` receives an `AgentState`, works on it, and returns the updated state.

### Basic Flow

```text
Goal
 ↓
AgentState
 ↓
Brain
 ↓
Create Plan
 ↓
Execute Action
 ↓
Store Observation
 ↓
Updated AgentState
```

### Implementation

The main implementation is available in:

```text
brain_contract.py
```

The brain:

1. Validates the incoming state.
2. Creates a plan if one does not already exist.
3. Executes one action at a time.
4. Stores the result in `observations`.
5. Stops when the plan is completed or a safety limit is reached.

### Validation

The brain checks that:

- The provided state is an `AgentState`.
- The goal is not empty.
- `max_steps` is greater than zero.
- The timeout is greater than zero.
- The retry count is not negative.

An empty goal is rejected with:

```text
ValueError: goal cannot be empty
```

### Guardrails

The implementation includes the following safety controls:

- **Step limit:** Prevents the brain from running forever.
- **Timeout:** Stops execution if the allowed time is exceeded.
- **Retry limit:** Allows only a limited number of retries for execution failures.
- **Validation:** Invalid input is rejected before execution.
- **Secret hygiene:** No API keys or credentials are stored in the source code.

### Run

Run the implementation using:

```bash
python brain_contract.brain_contract
```

### Automated Tests

Tests are available in:

```text
tests/test_brain_contract.py
```

Run them using:

```bash
pytest tests/test_brain_contract.py -v
```

The tests check:

- A valid goal completes successfully.
- An empty goal is rejected.
- The brain stops when the step limit is reached.

### Evidence

Program output can be saved using:

```bash
python brain.py > outputs/brain_contract.txt
```

Test results can be saved using:

```bash
pytest tests/test_brain_contract.py -v > outputs/test_brain_contract.txt
```

### Task 1 Result

The state/brain contract is successfully implemented. The brain accepts a valid state, updates it through controlled actions, records observations, and safely rejects invalid input.

---

## Task 2 — Control Loop

### Objective

This task implements the control loop of the agent.

The control loop allows the brain to work through the plan one action at a time. After each action, the result is stored as an observation and the loop checks whether more work is remaining.

The `AgentState` and `Brain` created in Task 1 are reused instead of creating them again.

### Implementation

The implementation is available in:

```text
control_loop/control_loop.py
```

Task 2 imports the existing components from Task 1:

```python
from brain_contract.brain_contract import AgentState, Brain
```

`ControlLoop` extends the existing `Brain`:

```python
class ControlLoop(Brain):
```

This allows the control loop to reuse state validation, plan creation, action execution, and the limits already defined by the brain.

### Control Loop Flow

```text
Agent State
    ↓
Create Plan
    ↓
Take Next Action
    ↓
Execute Action
    ↓
Store Observation
    ↓
More Actions?
   ↙       ↘
 Yes       No
  ↓         ↓
Repeat    Complete
```

### Step Limit

The loop keeps track of how many actions can be performed.

If the allowed number of steps is reached before the plan is complete, execution stops with:

```text
status = "limit_reached"
```

This prevents the control loop from continuing without a limit.

### Run

Run the implementation from the project root:

```bash
python -m control_loop.control_loop
```

### Automated Tests

The tests are available in:

```text
tests/test_control_loop.py
```

Run the tests using:

```bash
pytest tests/test_control_loop.py -v
```

The tests verify:

- A valid plan completes successfully.
- An empty goal is rejected.
- The control loop stops when the step limit is reached.

### Save Output

Save the implementation output:

```bash
python -m control_loop.control_loop > outputs/control_loop.txt
```

Save the automated test output:

```bash
pytest tests/test_control_loop.py -v > outputs/test_control_loop.txt
```

### Guardrails

The control loop uses the safety boundaries established by the brain, including:

- Step limit to prevent unlimited execution.
- Input validation to reject invalid states.
- Timeout configuration for operations that may take too long.
- Limited retries for temporary execution failures.
- No API keys or credentials stored in the source code.

The step-limit behavior is directly demonstrated in the automated tests.

### Task 2 Result

The control loop successfully reuses the Brain and AgentState from Task 1 and processes the plan one action at a time. Each completed action is recorded, and the loop stops when the plan is complete or when the allowed step limit is reached.