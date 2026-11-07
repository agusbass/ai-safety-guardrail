# AI Safety Guardrail — 0-19-0 Closed-Loop Pipeline

> **English summary:** an auditable, closed-loop AI safety guardrail — a 20-stage
> pipeline (0 → 19 → 0) built on the Matrix Graph (3D+1D) architecture. Every stage,
> including internal reasoning and the guardrail's own decisions, is logged to a
> shared audit trail with a mathematically convergent FAILSAFE.

**"Siapa yang menjaga sang penjaga?"** — guardrail yang dirancang agar
keputusannya sendiri bisa diaudit, bukan hanya filter input/output satu arah.

Dibangun di atas **Matrix Graph Architecture (3D+1D)** dari
[matrik-core](../matrik-core): 3 layer (Luar/mod-10, Magic Square Lo Shu,
Dalam/mod-20) menjadi struktur literal dari pipeline 20 tahap di bawah —
bukan sekadar metafora.

## Pipeline (0 → 19 → 0)

```
0  ROOT          (core, link Luar <-> Dalam)
── Luar / mod-10 (front-end, observable) ──
1  INPUT         6  CONSTRAIN
2  FILTER        7  AUTHENTICATE
3  SANITIZE      8  AUTHORIZE
4  CLASSIFY      9  ISOLATE
5  POLICY
── Dalam / mod-20 (back-end, internal) ──
10 RETRIEVE      15 MONITOR
11 VERIFY        16 DETECT
12 GROUND        17 BLOCK
13 REASON        18 AUDIT
14 VALIDATE      19 FAILSAFE
0  ROOT          (loop closes)
```

`digital_root(20) = 2`, dan `20 % 10 == 20 % 20 == 0` — secara matematis,
stage setelah FAILSAFE selalu kembali ke ROOT di kedua layer. Ini adalah
killswitch deterministik (non-AI) yang menutup loop, bukan AI yang mengaudit
dirinya sendiri secara rekursif.

## Struktur Proyek

```
src/guardian/
  core/matrix_graph.py     # Matrix Graph 3D+1D (inti struktural)
  pipeline/
    stages.py               # Stage enum (0-19)
    context.py               # PipelineContext (state + audit log)
    sanitize.py               # SANITIZE: strip obfuscation
    guardian_pipeline.py       # GuardianPipeline (orchestrator)
  constraints/               # 9 constitutional constraints (POLICY/CONSTRAIN) - WIP
tests/                        # pytest
legacy/                        # prototipe lama (dummy, akan dihapus)
```

## Instalasi & Pemakaian

```bash
pip install -e ".[dev]"
pytest -v
```

```python
from guardian import GuardianPipeline

pipeline = GuardianPipeline()
ctx = pipeline.process("user input here")

for stage_name, note in ctx.audit_log:
    print(stage_name, note)
```

## Status Implementasi

| Stage | Status | Grounding |
|---|---|---|
| 0 ROOT | ✅ | Matrix Graph core link |
| 1 INPUT | ✅ | — |
| 3 SANITIZE | ✅ | arXiv 2604.01194 (AgentWatcher), 2504.11358 (DataSentinel), 2510.14005 (PIShield) |
| 7 AUTHENTICATE | 🚧 | arXiv 2410.09102, 2511.04694 (instruction hierarchy) |
| 16 DETECT | 🚧 | arXiv 2402.09345 (InfoRM), 2602.01750, 2606.03238 (reward hacking) |
| 18 AUDIT | 🚧 | Anthropic Advanced AI Framework (Jun 2026) — Risk Report |
| 19 FAILSAFE | 🚧 | Anthropic Advanced AI Framework Part 2 — loss-of-control containment |
| sisanya | 📋 TODO | — |

Setiap detector wajib punya sitasi nyata (arXiv ID atau dokumen kebijakan) —
tidak ada keyword-list dummy.

## Posisi vs Produk Guardrail Lain (per Jun 2026)

EU AI Act mulai berlaku pertengahan 2026 — guardrail kini wajib bagi
Agentic AI yang bisa bertindak (kirim email, hapus file, transaksi).

| Produk | Pendekatan | Lapisan |
|---|---|---|
| NVIDIA NeMo Guardrails | Scripted rules (Colang) | Input/output filter |
| Llama Guard (Meta) | Model klasifier khusus | Input/output filter |
| Guardrails AI | Schema/structure validation | Output validation |
| Lakera Guard / HiddenLayer | Prompt-injection & PII detection | Input/output filter |
| Galileo | Small-LM real-time moderation | Input/output filter |
| AWS Bedrock Guardrails | Policy toggle bawaan cloud | Input/output filter |
| **Guardian (proyek ini)** | Closed-loop 20-stage, audit-trail tiap stage, FAILSAFE konvergen matematis | Seluruh siklus: input → reasoning → output → audit |

**Beda kami**: produk di atas mayoritas adalah filter satu arah (input atau
output saja). Guardian membuat *setiap* stage — termasuk reasoning internal
(RETRIEVE/VERIFY/REASON) dan keputusan guardrail itu sendiri (DETECT/BLOCK) —
masuk audit log yang sama, dengan jalur FAILSAFE yang strukturnya berasal
dari Matrix Graph (bukan ditambahkan belakangan).
