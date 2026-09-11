"""Simplified ring-vs-tree all-reduce communication model.

The model is educational, not a replacement for NCCL benchmarking. It exposes
how participant count, message size, bandwidth, and per-step latency interact.
"""

from math import ceil, log2


def seconds_for_bytes(byte_count: float, gbps: float) -> float:
    bits = byte_count * 8
    return bits / (gbps * 1e9)


def ring_allreduce_time(n: int, message_bytes: int, gbps: float, latency_us: float) -> float:
    if n < 2:
        return 0.0

    # reduce-scatter + all-gather, N-1 steps each
    steps = 2 * (n - 1)
    bytes_per_step = message_bytes / n
    transfer = steps * seconds_for_bytes(bytes_per_step, gbps)
    latency = steps * latency_us * 1e-6
    return transfer + latency


def tree_allreduce_time(n: int, message_bytes: int, gbps: float, latency_us: float) -> float:
    if n < 2:
        return 0.0

    depth = ceil(log2(n))
    # simplified reduce + broadcast
    steps = 2 * depth
    transfer = steps * seconds_for_bytes(message_bytes, gbps)
    latency = steps * latency_us * 1e-6
    return transfer + latency


def main() -> None:
    message_mib = 256
    message_bytes = message_mib * 1024 * 1024
    bandwidth_gbps = 400
    latency_us = 2.0

    print(
        f"message={message_mib} MiB, link={bandwidth_gbps} Gb/s, "
        f"step-latency={latency_us} us\n"
    )
    print("GPUs   ring_ms   tree_ms   faster")
    print("----   -------   -------   ------")

    for n in (2, 4, 8, 16, 32, 64):
        ring = ring_allreduce_time(n, message_bytes, bandwidth_gbps, latency_us) * 1e3
        tree = tree_allreduce_time(n, message_bytes, bandwidth_gbps, latency_us) * 1e3
        faster = "ring" if ring < tree else "tree"
        print(f"{n:>4}   {ring:>7.3f}   {tree:>7.3f}   {faster}")

    print(
        "\nInterpretation: this deliberately crude model shows why no collective "
        "algorithm is universally best. Message size, latency, topology, and "
        "effective bandwidth all change the result."
    )


if __name__ == "__main__":
    main()
