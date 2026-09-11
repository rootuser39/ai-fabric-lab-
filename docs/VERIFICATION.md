# Verification record — 2026-09-11

Local verification of the added `fabriclab/` suite:

- `python -m unittest discover -s tests -v`: 18 tests passed.
- `python -m fabriclab suite`: four scenarios completed and emitted JSON.
- `python -m fabriclab nccl examples/nccl_synthetic.txt`: two synthetic rows parsed.

Tests include 24 sender/capacity/phasing combinations checking packet
conservation, receive totals, capacity and the output-rate bound. Other checks
cover exact reference outcomes, event ordering, invalid configurations, repeatability,
correctness-error handling, unknown correctness and unsupported log formats.

| Synthetic case | Sent | Received | Dropped | Delivered p99 (us) | All-packet completion (us) |
|---|---:|---:|---:|---:|---:|
| Synchronized | 512 | 256 | 256 | 4 | Not completed |
| Staggered | 512 | 512 | 0 | 1 | 1023 |
| Larger buffer | 512 | 512 | 0 | 8 | 1016 |
| Sustained overload | 512 | 259 | 253 | 4 | Not completed |

These tests establish properties of this implementation, not fidelity to
production switches or NVIDIA products. No GPU benchmark or live workshop was
executed. The previously existing starter labs and notes were not revalidated.
