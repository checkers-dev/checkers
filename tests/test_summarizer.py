from checkers.summarizer import Summarizer


def test_summarizer_exit_code_with_passing_check(
    summary: Summarizer, check_result_passing
):
    summary.runner.results.append(check_result_passing)
    assert summary.exit_code() == 0


def test_summarizer_exit_code_with_failing_check(
    summary: Summarizer, check_result_failure
):
    summary.runner.results.append(check_result_failure)
    assert summary.exit_code() == 1


def test_summarizer_exit_code_with_error_check(summary: Summarizer, check_result_error):
    summary.runner.results.append(check_result_error)
    assert summary.exit_code() == 1
