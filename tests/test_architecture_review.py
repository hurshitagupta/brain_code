from architecture_review.architecture_review import ArchitectureReview
from bounded_failure.bounded_failure import BoundedFailure


def test_complete_architecture_passes():
    brain = BoundedFailure(max_steps=3,timeout_seconds=2.0,max_retries=1)

    reviewer = ArchitectureReview(brain)

    results = reviewer.review()

    assert len(results) == 5
    assert reviewer.passed() is True

    assert all(result.passed for result in results)


def test_incomplete_architecture_fails():
    class IncompleteBrain:
        max_steps = 3
        timeout_seconds = 2.0
        max_retries = 1

    brain = IncompleteBrain()

    reviewer = ArchitectureReview(brain)

    results = reviewer.review()

    assert reviewer.passed() is False

    failed_checks = [result.check for result in results if not result.passed]

    assert "state validation" in failed_checks
    assert "planning" in failed_checks
    assert "action execution" in failed_checks
    assert "decision trace" in failed_checks