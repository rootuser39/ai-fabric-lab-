# Tail Latency and Incast in AI Fabrics

Average latency is comforting and frequently misleading.

Distributed AI jobs synchronize. That means the slowest communication path can determine when the entire group advances. A small number of delayed flows can therefore have an outsized effect on accelerator utilization.

## Tail latency

Tail latency describes the slow end of the latency distribution, commonly examined through percentiles such as p95, p99, or p99.9.

Two fabrics can have the same average latency while behaving very differently at the tail. For tightly synchronized collectives, the fabric with the more predictable tail can deliver better application performance even when its average looks similar.

## Incast

Incast occurs when many senders transmit toward one receiver or one bottleneck over a short interval.

AI workloads naturally create this kind of behavior during synchronized communication phases.

A simplified failure sequence:

1. many workers become ready at nearly the same time
2. they send toward a common endpoint or set of links
3. queue occupancy rises rapidly
4. ECN marking begins
5. if feedback is too slow, buffers continue filling
6. PFC may trigger or packets may drop
7. one or more flows become stragglers
8. the collective waits
9. GPUs idle despite having compute available

## Elephant flows vs mice flows

AI traffic is often dominated by large transfers, or "elephant" flows. Traditional enterprise networks frequently optimize for mixed workloads that include many short "mice" flows.

The distinction matters because large synchronized transfers can sustain pressure on queues for much longer and can interact badly with static path selection.

## What to measure

Useful signals include:

- p50 / p95 / p99 latency
- queue depth over time
- ECN marks
- PFC pause events and duration
- link utilization
- packet drops
- flow completion time
- path imbalance
- NCCL operation duration
- GPU idle time during collective phases

The useful unit of analysis is the chain from network event to application stall, not the isolated counter.
