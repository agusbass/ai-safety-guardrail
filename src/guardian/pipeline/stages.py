"""Stage enum for the 0-19-0 closed-loop Guardian Pipeline.

Maps directly onto guardian.core.matrix_graph.MatrixGraph:
  0      ROOT   -> core (Luar-core <-> Dalam-core link)
  1-9    Luar (mod 10)  -> front-end / observable pipeline
  10-19  Dalam (mod 20) -> back-end / internal pipeline
  0      ROOT   -> close loop (FAILSAFE always returns here)
"""

from enum import Enum


class Stage(Enum):
    ROOT = 0
    INPUT = 1
    FILTER = 2
    SANITIZE = 3
    CLASSIFY = 4
    POLICY = 5
    CONSTRAIN = 6
    AUTHENTICATE = 7
    AUTHORIZE = 8
    ISOLATE = 9
    RETRIEVE = 10
    VERIFY = 11
    GROUND = 12
    REASON = 13
    VALIDATE = 14
    MONITOR = 15
    DETECT = 16
    BLOCK = 17
    AUDIT = 18
    FAILSAFE = 19
