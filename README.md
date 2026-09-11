# AI Fabric Lab

**Understand the network beneath distributed AI. Predict. Run. Measure. Explain.**

## Start with the tested experiment suite

New: deterministic incast experiments, a classic NCCL log reader, 18 unit tests,
and a hands-on workshop. Python 3.10+; no third-party packages or GPU required.

```bash
python -m unittest discover -s tests -v
python -m fabriclab suite
python -m fabriclab nccl examples/nccl_synthetic.txt
```

- [Start here: experiments and expected results](docs/START_HERE.md)
- [45-minute community workshop](docs/WORKSHOP.md)
- [Model assumptions and limits](docs/MODEL.md)
- [Path to real NVIDIA measurements](docs/HARDWARE_VALIDATION.md)
- [Community execution roadmap](docs/COMMUNITY.md)
- [Verification record](docs/VERIFICATION.md)

**Evidence boundary:** these new congestion results are synthetic. The NCCL
fixture is invented parser-test data. No NVIDIA hardware performance, existing
community adoption, NVIDIA affiliation or program acceptance is claimed.
Implementation and documentation were AI-assisted and locally tested; maintainer
review and independent reproduction remain important.

## Original project overview

A practical systems lab for understanding the infrastructure beneath distributed AI.

This repository focuses on the network and systems behavior that determines whether large-scale GPU workloads run efficiently or collapse under congestion, synchronization delay, packet loss, or poor topology decisions.

## Scope

- NVIDIA Spectrum-X and accelerated Ethernet
- InfiniBand architecture and operations
- RoCEv2, RDMA, PFC, ECN, and DCQCN
- NCCL collective communication patterns
- Tail latency, incast, elephant flows, and congestion
- ConnectX and BlueField DPU roles
- DGX/HGX communication paths
- Observability and troubleshooting of AI fabrics

## Core Question

> What actually happens between GPUs when a distributed AI job scales beyond one machine?

The lab approaches that question from first principles and then turns the theory into experiments.

## Repository Map

```text
ai-fabric-lab/
├── architecture/
│   ├── spectrum-x-vs-infiniband.md
│   └── dgx-network-path.md
├── networking/
│   ├── rocev2-congestion.md
│   └── tail-latency-and-incast.md
├── collectives/
│   └── nccl-allreduce.md
├── labs/
│   ├── congestion_sim.py
│   └── allreduce_model.py
└── README.md
```

## Design Principle

The network is not merely connectivity for AI systems. At scale, it becomes part of the compute architecture.

A fabric that introduces unpredictable latency, head-of-line blocking, packet loss, or unfair flow behavior can leave expensive accelerators idle while they wait at synchronization barriers.

## Labs

### Congestion simulator

A small discrete-time experiment for observing queue growth, ECN-style marking, packet drops, and the effect of multiple senders converging on one receiver.

```bash
python labs/congestion_sim.py
```

### All-reduce model

A simplified model comparing ring and tree collective communication cost as GPU count and message size increase.

```bash
python labs/allreduce_model.py
```

## Roadmap

- Add telemetry visualizations
- Model PFC pause propagation
- Add DCQCN-style rate adaptation
- Simulate ECMP versus adaptive routing
- Add NCCL topology experiments
- Build a troubleshooting playbook for AI fabric incidents
- Add containerized reproducible labs

## Status

Active research and experimentation repository. The goal is operational understanding, not vendor brochure memorization.

