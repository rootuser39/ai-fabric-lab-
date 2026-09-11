# Path to real NVIDIA measurements

Status: protocol only. No GPU, NCCL, Spectrum-X or InfiniBand hardware run has
been performed as part of this repository enhancement.

## Stage A — establish a trustworthy baseline

Use an authorized lab. Record GPU model/count, host count, physical topology,
NIC/switch models, firmware, driver, CUDA, NCCL, nccl-tests commit and MPI
versions. Record resource contention, power settings and topology placement.
Keep public reports sanitized and original evidence in an approved location.

Build and run [NVIDIA nccl-tests](https://github.com/NVIDIA/nccl-tests) according
to the selected commit's README. Multi-process/multi-node tests require its MPI
build path. Begin with two GPUs on one machine when available; that does not
exercise an inter-node fabric. Do not spend cloud credits without authorization.

## Stage B — repeat, then isolate

Choose a collective and fixed message size; record the exact invocation,
warmup and iteration counts, datatype, ranks, correctness configuration,
environment variables and both result modes. Repeat the same condition before
changing one factor. Retain failures, not only best runs.

Next compare authorized intra-node and inter-node conditions. Record NCCL's
selected paths; do not assume a NIC was used because one exists. Collect
time-aligned port counters and application observations where permitted.

## Stage C — establish cause carefully

Use a dedicated test system, approval and rollback before injecting congestion
or changing configuration. Check transport selection, CPU/NUMA placement,
competing workloads and link health before attributing slowdowns to the fabric.
An isolated bandwidth number is insufficient to diagnose a network fault.

## Evidence manifest for every published run

Include date, exact source revision, equipment, software versions, topology,
command, units, repeated-run count, correctness outcome, raw-log reference,
sanitization notes and known confounders. Label synthetic and measured data
separately. Never infer per-iteration p99 from a series of averages at different
message sizes. Follow the pinned tool version's timing-output documentation.

Use `python -m fabriclab nccl PATH_TO_SANITIZED_LOG` only for supported classic
stdout tables. The reader does not authenticate hardware provenance.
