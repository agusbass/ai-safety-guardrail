"""Shared mutable state threaded through every pipeline stage."""

from guardian.pipeline.stages import Stage


class PipelineContext:
    """Carries text, derived state, and the audit trail across stages."""

    def __init__(self, text: str):
        self.text = text
        self.output = None
        self.flags = {}
        self.scores = {}
        self.audit_log = []
        self.blocked = False
        self.escalated = False

    def log(self, stage: Stage, note: str):
        self.audit_log.append((stage.name, note))
