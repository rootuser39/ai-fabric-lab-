# AI Fabric Lab — from packets to evidence

An independent, early-stage educational project. Learn to explain an experiment,
reproduce it, and identify what it cannot establish. No NVIDIA affiliation or
hardware validation is claimed.

## Runnable now

Python 3.10 or newer; standard library only. Run from the repository root:

```bash
python -m unittest discover -s tests -v
python -m fabriclab suite
python -m fabriclab incast --staggered
python -m fabriclab incast --capacity 8
python -m fabriclab nccl examples/nccl_synthetic.txt
```

| Component | What it does | Evidence boundary |
|---|---|---|
| FIFO incast model | Tests synchronization, finite buffering and overload | Synthetic single bottleneck; no RDMA or vendor behavior |
| Experiment suite | Four deterministic counterfactuals | Not a GPU performance comparison |
| NCCL stdout reader | Preserves both measurement modes and correctness counts | Classic 13-column table only; fixture is invented |
| Workshop | Prediction, experiment, explanation, review | Ready to teach; no completed workshop claimed |
| Hardware protocol | Defines what to collect when hardware is available | Planned validation; no real runs included |

The existing `labs/`, `architecture/`, `networking/` and `collectives/` starter
material is preserved. The automated tests added here cover `fabriclab/`, not a
validation of every statement or model in those earlier notes.

## First experiment: same offered load, different synchronization

Eight senders each emit 64 packets, one every 16 microseconds. Packets contain
1,000 payload bytes. The abstract 8 Gbit/s server takes one microsecond per
packet. Its capacity includes the packet being transmitted.

| Scenario | Drops / 512 | Delivered packet p99 | All packets delivered? |
|---|---:|---:|---|
| Synchronized, capacity 4 | 256 | 4 us | No |
| Staggered, capacity 4 | 0 | 1 us | Yes |
| Synchronized, capacity 8 | 0 | 8 us | Yes |

These are exact expectations of the stated synthetic model, not observations
from Spectrum-X, InfiniBand, RoCE or GPUs. Staggering shifts sender start times;
it is not a free optimization available to every real workload. Compare total
completion as well as per-packet latency. The suite also includes sustained
overload, where staggering cannot create extra capacity.

**Trap:** dropping slow traffic can improve the measured tail of the surviving
traffic. This tool reports drops separately and refuses to report a successful
all-packet completion time if any packet was lost.

## Read next

- [Model contract](MODEL.md)
- [Hands-on workshop](WORKSHOP.md)
- [Hardware validation protocol](HARDWARE_VALIDATION.md)
- [Community roadmap](COMMUNITY.md)

## Contribution standard

Every experiment needs a hypothesis, exact command, assumptions, test, observed
result and one limitation. Label evidence **synthetic**, **measured**, or
**planned**. Do not publish employer information, credentials, host identities
or private architecture. Review AI-assisted code and verify its outputs.
