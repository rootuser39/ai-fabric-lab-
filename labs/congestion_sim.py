"""Tiny queue/congestion experiment for AI-fabric intuition.

This is intentionally simple. It is not a packet-accurate RoCE/DCQCN simulator.
It exists to make synchronized fan-in, queue growth, ECN-style marking, and
packet drops visible with almost no machinery.
"""

from dataclasses import dataclass


@dataclass
class FabricConfig:
    senders: int = 8
    sender_rate: int = 12       # packets per tick, per sender
    link_capacity: int = 64     # packets drained per tick
    buffer_size: int = 256      # packets
    ecn_threshold: int = 128    # queue depth where marking begins
    ticks: int = 30


def run(config: FabricConfig) -> None:
    queue = 0
    total_dropped = 0
    total_marked = 0

    print("tick arrivals drained queue marked dropped")
    print("---- -------- ------- ----- ------ -------")

    for tick in range(1, config.ticks + 1):
        arrivals = config.senders * config.sender_rate
        queue += arrivals

        marked = max(queue - config.ecn_threshold, 0)
        marked = min(marked, arrivals)
        total_marked += marked

        dropped = max(queue - config.buffer_size, 0)
        if dropped:
            queue = config.buffer_size
            total_dropped += dropped

        drained = min(queue, config.link_capacity)
        queue -= drained

        print(
            f"{tick:>4} {arrivals:>8} {drained:>7} {queue:>5} "
            f"{marked:>6} {dropped:>7}"
        )

    print("\nsummary")
    print(f"ECN-style marked packets: {total_marked}")
    print(f"dropped packets:          {total_dropped}")

    offered_load = config.senders * config.sender_rate
    if offered_load > config.link_capacity:
        print(
            "\nObservation: aggregate offered load exceeds bottleneck capacity. "
            "Without sender adaptation, queue growth is inevitable."
        )
    else:
        print("\nObservation: bottleneck capacity can absorb the steady offered load.")


if __name__ == "__main__":
    run(FabricConfig())
