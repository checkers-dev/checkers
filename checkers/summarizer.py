from .runner import Runner
from .contracts import CheckResult, CheckResultStatus


class Summarizer:
    def __init__(self, runner: Runner):
        self.runner = runner

    @property
    def config(self):
        return self.runner.config

    def failures(self):
        return [c for c in self.runner.results if c.status == CheckResultStatus.failure]

    def errors(self):
        return [c for c in self.runner.results if c.status == CheckResultStatus.error]

    def exit_code(self):
        if any(self.failures()) or any(self.errors()):
            return 1
        else:
            return 0
