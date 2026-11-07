"""Guardian — AI Safety Guardrail (0-19-0 closed-loop pipeline).

Built on top of the Matrix Graph Architecture (3D+1D) from matrik-core,
which provides the structural core (Luar/mod-10, Magic Square gateway,
Dalam/mod-20, Vortex Rings, Infinity Portal).
"""

from guardian.core.matrix_graph import MatrixGraph, Node
from guardian.pipeline.context import PipelineContext
from guardian.pipeline.guardian_pipeline import GuardianPipeline
from guardian.pipeline.stages import Stage

__all__ = [
    "GuardianPipeline",
    "PipelineContext",
    "Stage",
    "MatrixGraph",
    "Node",
]

__version__ = "0.1.0"
