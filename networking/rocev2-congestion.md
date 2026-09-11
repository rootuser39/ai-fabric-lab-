# RoCEv2 Congestion: The Operational Model

RoCEv2 carries RDMA traffic over UDP/IP. That gives routability, but it also means the network must be engineered carefully because RDMA workloads are unusually sensitive to congestion and loss.

## Why congestion hurts AI workloads

Distributed training often uses collective operations. One slow participant can delay an entire synchronization step. Average latency therefore tells only part of the story; tail latency and straggler behavior matter disproportionately.

## The basic control loop

A simplified Ethernet AI-fabric congestion loop is:

1. Multiple senders drive traffic toward a bottleneck.
2. The egress queue begins to grow.
3. The switch marks packets using ECN before the queue overflows.
4. The receiver reflects congestion information back to the sender.
5. The sender reduces its transmission rate.
6. When congestion subsides, rate can recover.

In NVIDIA-oriented RoCE environments, DCQCN-style endpoint rate control is a key concept in understanding this loop.

## Where PFC fits

Priority Flow Control can pause a traffic class on a link when buffering crosses a threshold.

That can prevent packet loss, but it is not free magic. Poorly designed PFC domains can create:

- pause propagation
- head-of-line blocking
- congestion spreading upstream
- pathological interactions with oversubscription

PFC should therefore be treated as a safety mechanism inside a broader congestion-control design, not as the congestion-control strategy itself.

## ECN vs PFC

A useful mental model:

- **ECN:** warn early and slow the sender.
- **PFC:** stop traffic locally before buffers overflow.

One is preventive feedback. The other is an emergency brake.

## Troubleshooting sequence

When RoCE throughput or latency collapses:

1. Check interface utilization and oversubscription.
2. Inspect queue occupancy.
3. Look for ECN marking rates.
4. Look for PFC pause frames and pause duration.
5. Check packet drops and retransmission indicators.
6. Determine whether congestion is persistent or microburst-driven.
7. Correlate network behavior with NCCL collective phases.
8. Identify whether one receiver is attracting synchronized fan-in traffic.

The mistake is debugging each counter independently. The counters describe one feedback system.
