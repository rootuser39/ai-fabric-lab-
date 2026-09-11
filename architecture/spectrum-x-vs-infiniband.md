# Spectrum-X vs InfiniBand

## The problem both are solving

Distributed AI is synchronization-heavy. GPUs frequently exchange large tensors, gradients, activations, and collective-operation traffic. The useful question is therefore not simply "which network is faster?" but:

> Which fabric preserves predictable communication under synchronized, high-bandwidth, many-to-many load?

## InfiniBand

InfiniBand was designed as a high-performance interconnect rather than adapted from conventional Ethernet.

Key properties:

- Native RDMA semantics
- Credit-based link-level flow control
- Strong congestion-management mechanisms
- Subnet-manager-driven fabric control
- Service Levels and Virtual Lanes for traffic separation
- Mature integration with HPC and distributed AI

The operational consequence is that losslessness and low latency are fundamental design assumptions rather than features bolted onto a general-purpose network.

## Spectrum-X

Spectrum-X uses Ethernet as the transport foundation but optimizes the fabric for AI workloads through tightly integrated switching, NIC/SuperNIC behavior, congestion control, telemetry, and routing.

Important ideas include:

- RoCEv2 for RDMA over routable Ethernet
- ECN-based congestion signaling
- Sender-side rate adaptation
- Adaptive routing and traffic engineering
- Deep telemetry and coordinated endpoint/fabric behavior

The important architectural point is that Ethernet alone is not the product. The useful system is the coordinated switch + endpoint + control behavior.

## Conceptual comparison

| Dimension | InfiniBand | Spectrum-X |
|---|---|---|
| Transport foundation | Purpose-built fabric | Ethernet |
| RDMA | Native | RoCEv2 |
| Loss behavior | Designed around lossless operation | Engineered toward lossless behavior |
| Congestion control | Fabric-native mechanisms | ECN + endpoint/fabric coordination |
| Interoperability | Specialized ecosystem | Ethernet ecosystem |
| Operational model | HPC-style fabric | Ethernet operational model with AI-specific enhancements |

## Failure lens

When performance degrades, ask:

1. Are GPUs waiting on communication or compute?
2. Is congestion localized or fabric-wide?
3. Are queues building at a fan-in point?
4. Are ECN marks appearing before drops?
5. Is PFC creating pause propagation or head-of-line blocking?
6. Are flows being distributed poorly across equal-cost paths?
7. Is one endpoint or link becoming a straggler?
8. Is the collective algorithm mismatched to topology?

That is the level at which AI-fabric comparison becomes useful. Benchmark numbers without failure behavior are mostly decorative numerology.
