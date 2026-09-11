# NCCL All-Reduce: Network-Centric View

All-reduce is one of the defining traffic patterns in distributed AI training. Each participant contributes data and all participants receive the reduced result.

The algorithm matters because communication structure determines how much data crosses each link, when links become hot, and how badly a straggler can delay the step.

## Ring all-reduce

A ring commonly decomposes all-reduce into:

1. reduce-scatter
2. all-gather

Each participant sends chunks around a logical ring. For large messages, this can use bandwidth efficiently because traffic is spread over a sequence of point-to-point transfers.

A simplified communication-volume intuition per participant is approximately:

`2 * (N - 1) / N * message_size`

where `N` is the number of participants.

The cost is multiple sequential communication steps, so latency matters more as the participant count grows.

## Tree all-reduce

Tree-based reductions reduce values toward a root or intermediate nodes and then distribute the result back down the tree.

The number of communication stages grows roughly with `log2(N)`, which can be attractive for smaller messages or latency-sensitive operations.

## Why topology matters

A logical collective does not exist in a vacuum. It maps onto:

- NVLink/NVSwitch inside a node
- PCIe paths
- NIC placement
- leaf/spine topology
- rail design
- routing choices
- link speed and oversubscription

A mathematically elegant ring mapped badly onto physical topology can produce avoidable hotspots.

## Operational questions

When an all-reduce underperforms, ask:

1. Is the bottleneck intra-node or inter-node?
2. Are all GPUs attached symmetrically to high-speed paths?
3. Is NCCL selecting the expected interfaces and topology?
4. Are multiple collective flows colliding on the same fabric links?
5. Is one endpoint slower and forcing synchronization waits?
6. Are packet loss, ECN, or PFC events correlated with collective phases?
7. Would another collective topology better fit the message size or network shape?

## Key idea

A collective is both an algorithm and a traffic generator. To troubleshoot distributed AI, learn to see the communication algorithm as a temporary network topology imposed on top of the physical one.
