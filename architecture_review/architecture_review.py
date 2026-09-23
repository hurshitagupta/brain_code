from dataclasses import dataclass

from bounded_failure.bounded_failure import BoundedFailure


@dataclass
class ReviewResult:
    check: str
    passed: bool
    message: str


class ArchitectureReview:

    def __init__(self, brain: BoundedFailure):
        self.brain = brain
        self.results: list[ReviewResult] = []

    def add_result(self,check: str,passed: bool,message: str,) -> None:
        self.results.append(
            ReviewResult(check=check,passed=passed,message=message,)
        )

    def review(self) -> list[ReviewResult]:
        self.results = []

        self.add_result(
            check="state validation",
            passed=callable(
                getattr(self.brain, "validate_state", None)
            ),
            message="Brain has a separate state validation method.",
        )

        self.add_result(
            check="planning",
            passed=callable(
                getattr(self.brain, "create_plan", None)
            ),
            message="Planning is kept behind a separate method.",
        )

        self.add_result(
            check="action execution",
            passed=callable(
                getattr(self.brain, "execute_action", None)
            ),
            message="Action execution is kept behind a separate method.",
        )

        self.add_result(
            check="decision trace",
            passed=hasattr(self.brain, "decisions"),
            message="Brain keeps a reviewable decision trace.",
        )

        limits_present = (
            self.brain.max_steps > 0
            and self.brain.timeout_seconds > 0
            and self.brain.max_retries >= 0
        )

        self.add_result(
            check="safety limits",
            passed=limits_present,
            message="Step, timeout, and retry limits are configured.",
        )

        return self.results

    def passed(self) -> bool:
        return all(result.passed for result in self.results)


if __name__ == "__main__":
    brain = BoundedFailure(max_steps=3,timeout_seconds=2.0,max_retries=1)

    reviewer = ArchitectureReview(brain)

    results = reviewer.review()

    print("=== ARCHITECTURE REVIEW ===")

    for result in results:
        status = "PASS" if result.passed else "FAIL"

        print(
            f"{status} | "
            f"{result.check} | "
            f"{result.message}"
        )

    print("\nOverall:","PASS" if reviewer.passed() else "FAIL")