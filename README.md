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

---

## Task 3 — Decision Trace

### Objective

This task adds a decision trace to the agent.

The decision trace records what action the brain selected at each step and why it selected or stopped that action. This makes the execution easier to follow and review.

The implementation reuses the `AgentState` from Task 1 and the `ControlLoop` from Task 2.

### Implementation

The implementation is available in:

```text
decision_trace/decision_trace.py
```

Task 3 builds on the previous tasks:

```text
Brain
  ↓
Control Loop
  ↓
Decision Trace
```

Each decision stores:

- Step number
- Selected action
- Reason for the decision

For example:

```text
Step 1
Action: inspect goal: explain agent state
Reason: next action in the plan
```

The decision to stop is also recorded.

### Decision Flow

```text
Check Plan
    ↓
Select Action
    ↓
Record Decision
    ↓
Execute Action
    ↓
Store Observation
    ↓
Continue or Stop
```

This makes it possible to follow the decisions made during execution instead of only seeing the final result.

### Run

Run the implementation from the project root:

```bash
python -m decision_trace.decision_trace
```

### Automated Tests

Tests are available in:

```text
tests/test_decision_trace.py
```

Run:

```bash
pytest tests/test_decision_trace.py -v
```

The tests verify:

- Decisions are recorded during successful execution.
- An empty goal is rejected.
- The reason for stopping at the step limit is recorded.

### Save Output

Save the implementation output:

```bash
python -m decision_trace.decision_trace > outputs/decision_trace.txt
```

Save the automated test output:

```bash
pytest tests/test_decision_trace.py -v > outputs/test_decision_trace.txt
```

Generated output files:

```text
outputs/decision_trace.txt
outputs/test_decision_trace.txt
```

### Guardrails

This task continues to use the safety boundaries established in the previous tasks.

The decision trace also makes these boundaries easier to review because the reason for stopping is recorded.

For example:

```text
Action: stop
Reason: step limit reached
```

Input validation continues to reject invalid states, and no credentials or secrets are stored in the source code.

### Task 3 Result

The agent now keeps a clear record of its decisions. Each selected action and the reason for stopping can be followed through the decision trace, making the brain's execution easier to understand and review.

---

## Task 4 — Bounded Failure

### Objective

This task ensures that failures cannot make the agent run forever.

The implementation reuses the Brain, control loop, and decision trace from the previous tasks and adds controlled handling for retries, timeouts, and step limits.

### Implementation

The implementation is available in:

```text
bounded_failure/bounded_failure.py
```

Task 4 builds on the previous architecture:

```text
Brain
  ↓
Control Loop
  ↓
Decision Trace
  ↓
Bounded Failure
```

### Temporary Failure and Retry

A `TemporaryFailure` represents an error that may succeed if attempted again.

Only this type of failure is retried.

Retries are limited using `max_retries`. If the action continues to fail after the allowed retries, execution stops with:

```text
status = "failed"
```

The decision trace records the retry and the reason for stopping.

### Timeout

The brain keeps track of how much time the execution has used.

If the configured timeout is exceeded, execution stops with:

```text
status = "timeout"
```

### Step Limit

The existing step limit is also enforced.

If the maximum number of steps is reached before the plan is complete:

```text
status = "limit_reached"
```

### Failure Flow

```text
Execute Action
      ↓
   Failure?
   ↙     ↘
 No      Yes
 ↓        ↓
Continue  Temporary?
          ↓
         Yes
          ↓
     Retry Allowed?
       ↙       ↘
     Yes        No
      ↓          ↓
    Retry       Stop
```

### Run

Run the implementation from the project root:

```bash
python -m bounded_failure.bounded_failure
```

### Automated Tests

Tests are available in:

```text
tests/test_bounded_failure.py
```

Run:

```bash
pytest tests/test_bounded_failure.py -v
```

The tests verify:

- Normal execution completes successfully.
- A temporary failure is retried.
- Execution stops when the retry limit is reached.
- Execution stops when the timeout is reached.
- Execution stops when the step limit is reached.

### Save Output

Save the implementation output:

```bash
python -m bounded_failure.bounded_failure > outputs/bounded_failure.txt
```

Save the automated test output:

```bash
pytest tests/test_bounded_failure.py -v > outputs/test_bounded_failure.txt
```

### Guardrails

This task directly demonstrates:

- **Step limit:** Prevents unlimited control-loop execution.
- **Timeout:** Stops execution when the allowed time is exceeded.
- **Retry limit:** Only temporary failures are retried and retries are capped.
- **Validation:** Invalid states continue to be rejected by the Brain.
- **Secret hygiene:** No credentials or API keys are stored in source code.

### Task 4 Result

The agent handles failures within clear limits. Temporary failures can be retried, while repeated failures, excessive execution time, and excessive steps cause the brain to stop safely instead of continuing indefinitely.

---

## Task 5 — Architecture Review

### Objective

This task reviews the architecture created across the previous tasks.

The purpose is to verify that important responsibilities such as validation, planning, action execution, decision tracing, and safety limits are clearly separated instead of being hidden inside one large function.

### Implementation

The implementation is available in:

```text
architecture_review/architecture_review.py
```

The complete architecture developed across the assessment is:

```text
Brain Contract
      ↓
Control Loop
      ↓
Decision Trace
      ↓
Bounded Failure
      ↓
Architecture Review
```

The architecture review checks that the brain provides:

- State validation
- Separate planning
- Separate action execution
- Decision tracing
- Step, timeout, and retry limits

Each check produces a structured PASS or FAIL result.


### Failure Case

The automated tests also review an intentionally incomplete brain.

Because the incomplete version does not contain validation, planning, action execution, or decision tracing, the architecture review returns failed checks.

This demonstrates that the reviewer can identify missing parts instead of always returning PASS.

### Run

Run the implementation from the project root:

```bash
python -m architecture_review.architecture_review
```

### Automated Tests

Tests are available in:

```text
tests/test_architecture_review.py
```

Run:

```bash
pytest tests/test_architecture_review.py -v
```

The tests verify:

- The complete architecture passes all checks.
- An incomplete architecture fails the expected checks.

### Save Output

Save the implementation output:

```bash
python -m architecture_review.architecture_review > outputs/architecture_review.txt
```

Save the automated test output:

```bash
pytest tests/test_architecture_review.py -v > outputs/test_architecture_review.txt
```

### Architecture Result

The final implementation keeps the main responsibilities separated and reviewable.

The Brain manages the basic state contract, the control loop manages repeated execution, the decision trace records decisions, and bounded failure keeps execution within defined limits.

Because these responsibilities are separated, individual parts can be tested or changed without placing all agent behavior inside one large function.

### Task 5 Result

The architecture review successfully checks the important parts of the agent and produces clear PASS or FAIL results. The completed implementation demonstrates a simple agent brain built from ordinary, testable Python components.
---

## Project Setup

### Requirements

- Python 3.11+
- pytest

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Project Architecture

The project is divided into separate modules, with each task building on the previous implementation.

```text
brain_contract/
        ↓
control_loop/
        ↓
decision_trace/
        ↓
bounded_failure/
        ↓
architecture_review/
```

### Module Responsibilities

- **Brain Contract** — Defines the agent state and the basic Brain behavior.
- **Control Loop** — Processes the plan one action at a time.
- **Decision Trace** — Records the actions selected by the brain and the reasons for its decisions.
- **Bounded Failure** — Adds controlled retry, timeout, and step-limit behavior.
- **Architecture Review** — Checks that the important parts of the architecture are present and separated.

---

## Run All Tests

Run the complete automated test suite from the project root:

```bash
pytest tests/ -v
```

To save the complete test output:

```bash
pytest tests/ -v > outputs/test_all.txt
```

---

## Output Evidence

Execution and test evidence is stored in the `outputs/` directory.

```text
outputs/
├── brain_contract.txt
├── test_brain_contract.txt
├── control_loop.txt
├── test_control_loop.txt
├── decision_trace.txt
├── test_decision_trace.txt
├── bounded_failure.txt
├── test_bounded_failure.txt
├── architecture_review.txt
├── test_architecture_review.txt
└── test_all.txt
```

---

## Guardrails

The project includes the required execution boundaries:

- **Step limit** — prevents the control loop from running indefinitely.
- **Timeout** — stops the brain when the allowed execution time is exceeded.
- **Retry limit** — retries only the defined temporary failure and limits the number of retries.
- **Validation** — rejects invalid state and empty goals.
- **Secret hygiene** — no API keys or credentials are required or stored in the source code.

The bounded-failure tests demonstrate step-limit, timeout, and retry behavior.

---

## Reflection 

This implementation focuses on the architecture of an agent brain rather than using an AI model or agent framework.
The main learning from the assessment is that an agent brain can be implemented as normal software with clear state, decisions, execution steps, and stopping conditions.


