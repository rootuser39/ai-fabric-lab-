# DGX / HGX Communication Path

Distributed AI performance depends on the full communication path, not merely GPU FLOPS.

A useful mental model is:

```text
GPU
  ↓
NVLink / NVSwitch (intra-node fast path)
  ↓
PCIe / CPU-root-complex relationship
  ↓
ConnectX / SuperNIC
  ↓
Leaf switch
  ↓
Spine fabric
  ↓
Leaf switch
  ↓
Remote NIC
  ↓
Remote GPU
```

## Intra-node

Inside a multi-GPU system, NVLink and NVSwitch can provide much higher GPU-to-GPU bandwidth than traversing conventional host I/O paths. Collective libraries try to exploit this topology rather than treating all peers as equivalent.

## Inter-node

Once traffic leaves the node, NIC placement, PCIe locality, link speed, rail design, routing, and congestion behavior become decisive.

A nominally fast NIC can still underperform if:

- GPU-to-NIC affinity is poor
- traffic crosses an unfavorable NUMA boundary
- multiple GPUs contend for the same path
- the fabric hashes synchronized flows onto the same links
- congestion introduces tail latency

## DPU role

BlueField-class DPUs can move infrastructure work away from the host CPU and provide programmable networking, security, telemetry, and service isolation capabilities. The architectural value is not simply "another processor"; it is relocating control and data-plane work closer to the network boundary.

## Operator's rule

When a job is slow, map the path before blaming the component.

The observable symptom may be "GPU utilization dropped," while the actual fault sits several layers away in queueing, topology, affinity, or transport behavior.
