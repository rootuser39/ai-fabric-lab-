# Model contract

## Included

One FIFO output server; fixed payload size and service rate; finite system
capacity; deterministic periodic arrivals; synchronous or uniformly phased
senders; tail drop; complete draining of accepted traffic. Departure events win
ties with arrival events. Simultaneous arrivals are ordered by sender ID.

That deterministic tie-break can repeatedly favor low-numbered senders. The
per-sender receive counters expose this artifact; it is not a fairness model.

## Units and metrics

- Service time in us = payload bytes * 8 / (link Gbit/s * 1000).
- Capacity includes the packet in service, not just packets waiting.
- Packet latency runs from arrival to departure, excluding propagation.
- p50/p99 use nearest rank over **accepted packets only**.
- Goodput uses delivered payload bits / (last delivery - first offered arrival).
  This interval excludes an unobserved idle period after the final arrival.
- `all_packets_delivered_at_us` is null if any packet is lost. It is a delivery
  barrier for this model, not an NCCL collective runtime estimate.

## Excluded

Ethernet framing, ECN, PFC, congestion-control feedback, retransmissions, RDMA,
PCIe, NVLink, NCCL algorithms, switch pipelines, multi-hop topology, adaptive
routing, GPU computation and wall-clock timing of real networks.

It cannot determine whether Spectrum-X outperforms InfiniBand, predict GPU
utilization or choose a production congestion-control configuration.

## NCCL parser contract

Accepts the classic 13-column stdout table with its column header. Preserves
out-of-place and in-place results separately. `N/A` correctness is unknown, not
zero. Non-finite values, negative metrics, unsupported headers and malformed
data rows fail explicitly. Extended/timestamped tables and interleaved logs
need preprocessing or a future version-specific adapter.

`time_reported` is deliberately not assigned a guessed unit; retain the source
log and read its units header. Reported averages across iterations or ranks do
not establish per-iteration p99. Zero reported errors alone does not prove
that correctness checking was enabled; retain the exact command.

NCCL algorithm bandwidth and bus bandwidth are different reported quantities;
bus bandwidth is not a switch-port counter. Interpretation depends on the
collective and topology. See the upstream [performance explanation](https://github.com/NVIDIA/nccl-tests/blob/master/doc/PERFORMANCE.md).
