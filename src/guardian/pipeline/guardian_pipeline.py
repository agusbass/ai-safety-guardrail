"""Guardian Pipeline -- 0-19-0 Closed Loop.

Maps directly onto guardian.core.matrix_graph.MatrixGraph:
  0      ROOT   -> core (Luar-core <-> Dalam-core link)
  1-9    Luar (mod 10)  -> front-end / observable pipeline
  10-19  Dalam (mod 20) -> back-end / internal pipeline
  0      ROOT   -> close loop (FAILSAFE always returns here)

Research grounding (see memory/feedback_research_grounding.md):
  SANITIZE     -> obfuscation stripping (arXiv 2604.01194, 2504.11358, 2510.14005)
  AUTHENTICATE -> instruction hierarchy (arXiv 2410.09102, 2511.04694)
  ISOLATE      -> sandboxing untrusted tool/code calls (Security constraint)
  DETECT       -> reward-hacking / spec-gaming (arXiv 2402.09345, 2602.01750, 2606.03238)
                  + prompt-injection rule-based reasoning (arXiv 2604.01194)
  AUDIT        -> Risk Report (Anthropic Advanced AI Framework, June 2026)
  FAILSAFE     -> loss-of-control containment (Anthropic Advanced AI Framework, Part 2)
"""

from guardian.core.matrix_graph import MatrixGraph
from guardian.pipeline.context import PipelineContext
from guardian.pipeline.sanitize import sanitize_text
from guardian.pipeline.stages import Stage


class GuardianPipeline:
    """0-19-0 closed-loop guardrail pipeline, built on the Matrix Graph core."""

    LUAR_STAGES = [Stage.INPUT, Stage.FILTER, Stage.SANITIZE, Stage.CLASSIFY,
                   Stage.POLICY, Stage.CONSTRAIN, Stage.AUTHENTICATE,
                   Stage.AUTHORIZE, Stage.ISOLATE]

    DALAM_STAGES = [Stage.RETRIEVE, Stage.VERIFY, Stage.GROUND, Stage.REASON,
                    Stage.VALIDATE, Stage.MONITOR, Stage.DETECT, Stage.BLOCK,
                    Stage.AUDIT, Stage.FAILSAFE]

    def __init__(self):
        # The Matrix Graph is the structural core: Luar (mod 10) and Dalam
        # (mod 20) layers correspond 1:1 to LUAR_STAGES and DALAM_STAGES.
        self.graph = MatrixGraph(11).build()

        self.handlers = {
            Stage.ROOT: self.root,
            Stage.INPUT: self.input_stage,
            Stage.FILTER: self.filter_stage,
            Stage.SANITIZE: self.sanitize,
            Stage.CLASSIFY: self.classify,
            Stage.POLICY: self.policy,
            Stage.CONSTRAIN: self.constrain,
            Stage.AUTHENTICATE: self.authenticate,
            Stage.AUTHORIZE: self.authorize,
            Stage.ISOLATE: self.isolate,
            Stage.RETRIEVE: self.retrieve,
            Stage.VERIFY: self.verify,
            Stage.GROUND: self.ground,
            Stage.REASON: self.reason,
            Stage.VALIDATE: self.validate,
            Stage.MONITOR: self.monitor,
            Stage.DETECT: self.detect,
            Stage.BLOCK: self.block,
            Stage.AUDIT: self.audit,
            Stage.FAILSAFE: self.failsafe,
        }

    def process(self, text: str) -> PipelineContext:
        ctx = PipelineContext(text)
        order = [Stage.ROOT] + self.LUAR_STAGES + self.DALAM_STAGES + [Stage.ROOT]
        for i, stage in enumerate(order):
            is_last_root = (i == len(order) - 1)
            if ctx.blocked and stage not in (Stage.AUDIT, Stage.FAILSAFE) and not is_last_root:
                continue
            self.handlers[stage](ctx)
            if ctx.escalated and stage != Stage.FAILSAFE and not is_last_root:
                self._jump_to_failsafe(ctx)
                break
        return ctx

    def _jump_to_failsafe(self, ctx: PipelineContext):
        for stage in (Stage.AUDIT, Stage.FAILSAFE, Stage.ROOT):
            self.handlers[stage](ctx)

    # ---- 0 / ROOT : core, links Luar <-> Dalam ----
    def root(self, ctx: PipelineContext):
        luar_core = self.graph.get_node('luar_core_0')
        dalam_core = self.graph.get_node('dalam_core_0')
        ms_core = self.graph.get_node('ms_core_5')
        linked = (ms_core in luar_core.edges) and (ms_core in dalam_core.edges)
        ctx.log(Stage.ROOT, f"core checkpoint (luar<->ms<->dalam linked={linked})")

    # ---- 1-9 Luar (mod 10): front-end / observable pipeline ----
    def input_stage(self, ctx: PipelineContext):
        ctx.log(Stage.INPUT, f"received {len(ctx.text)} chars")

    def filter_stage(self, ctx: PipelineContext):
        ctx.log(Stage.FILTER, "TODO: pre-filter pass")

    def sanitize(self, ctx: PipelineContext):
        text, flags = sanitize_text(ctx.text)
        ctx.text = text
        ctx.flags['sanitize'] = flags
        ctx.log(Stage.SANITIZE, f"flags={flags}" if flags else "clean")

    def classify(self, ctx: PipelineContext):
        ctx.log(Stage.CLASSIFY, "TODO: intent classification")

    def policy(self, ctx: PipelineContext):
        # 9 constitutional constraints (Lo Shu) live here -> guardian.constraints
        ctx.log(Stage.POLICY, "TODO: run 9 constitutional constraints")

    def constrain(self, ctx: PipelineContext):
        ctx.log(Stage.CONSTRAIN, "TODO: apply constraint outcomes")

    def authenticate(self, ctx: PipelineContext):
        # arXiv 2410.09102 / 2511.04694 - instruction hierarchy / privilege levels
        ctx.log(Stage.AUTHENTICATE, "TODO: classify instruction privilege level")

    def authorize(self, ctx: PipelineContext):
        ctx.log(Stage.AUTHORIZE, "TODO: permission check for requested action")

    def isolate(self, ctx: PipelineContext):
        ctx.log(Stage.ISOLATE, "TODO: sandbox untrusted tool/code calls")

    # ---- 10-19 Dalam (mod 20): back-end / internal pipeline ----
    def retrieve(self, ctx: PipelineContext):
        ctx.log(Stage.RETRIEVE, "TODO: retrieve relevant context")

    def verify(self, ctx: PipelineContext):
        ctx.log(Stage.VERIFY, "TODO: cross-check retrieved facts")

    def ground(self, ctx: PipelineContext):
        ctx.log(Stage.GROUND, "TODO: grounding / hallucination check")

    def reason(self, ctx: PipelineContext):
        ctx.log(Stage.REASON, "TODO: response generation")

    def validate(self, ctx: PipelineContext):
        ctx.log(Stage.VALIDATE, "TODO: output-side constraint re-check")

    def monitor(self, ctx: PipelineContext):
        ctx.log(Stage.MONITOR, "TODO: behavior pattern monitoring over time")

    def detect(self, ctx: PipelineContext):
        # arXiv 2402.09345 (InfoRM) / 2602.01750 / 2606.03238 - reward hacking
        # arXiv 2604.01194 (AgentWatcher) - prompt injection rule-based reasoning
        ctx.log(Stage.DETECT, "TODO: spec-gaming / prompt-injection detection")

    def block(self, ctx: PipelineContext):
        ctx.log(Stage.BLOCK, "TODO: enforce block decision")

    def audit(self, ctx: PipelineContext):
        # Anthropic Advanced AI Framework (June 2026) - Risk Report
        ctx.log(Stage.AUDIT, "TODO: append-only risk report entry")

    def failsafe(self, ctx: PipelineContext):
        # Mathematical tie back to ROOT: digital_root(20) = 2, and
        # 20 % 10 == 20 % 20 == 0, so stage index 20 (one past FAILSAFE=19)
        # collapses to ROOT=0 in both the Luar (mod 10) and Dalam (mod 20)
        # layers. This is the deterministic, non-AI killswitch loop closure.
        dr = self.graph.digital_root(20)
        ctx.log(Stage.FAILSAFE, f"TODO: containment / shutdown trigger (digital_root(20)={dr} -> ROOT)")
