# Main-thread scoring repair: staged and running

The original cohort callback called the frozen Math-Verify scorer from a ThreadPool worker. Math-Verify returned a technical error because its timeout uses signal.alarm. The old controller stopped on a child error; other GPU workers continued. Original sources, logs, grades and raw files are retained.

Attempt2 invokes grading only on the OS main thread, after server.run returns. Each completed callback writes its complete ungraded trace to raw-rank-N.jsonl under a lock and fsync before returning. It retains generated IDs, loss masks, behavior logprobs, policy-call contexts, physical forward accounting and seed. Global cohort forward ledgers remain written by the model owner after each completed batch. No callbacks grade or change scorer timeout semantics.

The durable controller checks ROOT-REPAIR-HOLD, the complete original source/config/data hash manifest, and CPU proof hashes. It waits independently per rank for the original child PID to terminate, checks start ticks against its ownership snapshot to reject PID reuse, and verifies that GPU is empty. It never signals GPU workers. Existing saved answers are copied to new output paths; only the known thread-scoring error is regraded. Original error/grade is retained alongside the new grade. Other technical unknowns remain explicit unknowns. Missing, uncommitted traces are regenerated with their original question seeds and input order; those traces are not claimed recoverable.

The model, system, frozen scorer, selected data, FP32 decoding, response32768/path768/context40960, n1 and two-question cohort budgets are unchanged. RL config differs only in output destination. Removing saved questions can change a subsequent cohort partner; no exact bitwise comparison to the interrupted original workload is claimed.

CPU-PROOF.json passed real answer70 main-thread grading, worker-thread grading guard, AST callback-without-grader assertion, concurrent eight-record raw writes, idempotent recovery, and compilation of seven runtime Python files. macOS AppleDouble metadata from tar is ignored by the compile test; the seven Python files themselves are hash bound.

Live early snapshot: controller PID2694 on the existing mpiworker-2; repaired child PIDs2700/2705/2710/2715/2720/2725 for ranks0/1/2/5/6/7. Ranks3/4 were still draining original workers. Six original saved answers recovered without resampling and without technical errors; old error grades are preserved. This snapshot is not terminal benchmark completion.

Original native Qwen/Qwen3-4B revision1cfa9a7208912126459214e8b04321603b3df60c files, including all three weight shards, were stream-hashed once and matched the pinned source proof. Native runs launch per GPU only after repaired RL exit0 and GPU emptiness. CountingWorker increments a GPU tensor through the actual model forward hook; its measured counter must equal the execute-model event ledger. Import alone is not proof of successful actual vLLM startup.

Finalization requires all eight repaired RL children and all eight native children exit0; exact53 retry IDs plus77 retained IDs; native130 IDs; no duplicates or missing IDs. Any remaining scorer error is retained in coverage.json and blocks scored success summary rather than being counted as wrong. Result artifacts stay under this attempt2 namespace.

ACTUAL-REPAIR-PROOF.json subsequently confirmed four new GPU-completed traces: raw values retained exactly after MainThread grading, no technical unknowns. Two measured backend batches counted3629 and5043 physical forwards, distinct from sums of episode participation6395 and8583. These canonical selected rows and ledgers are SHA bound, avoiding hashes of still-appending rank files.
