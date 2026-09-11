"""Deterministic, single-output FIFO packet model with finite capacity."""

from collections import deque
from dataclasses import asdict, dataclass
from math import ceil, isfinite


@dataclass(frozen=True)
class Config:
    senders: int = 8
    packets_per_sender: int = 64
    packet_bytes: int = 1000
    link_gbps: float = 8.0
    interval_us: float = 16.0
    capacity_packets: int = 4
    staggered: bool = False

    def validate(self):
        for name in ("senders", "packets_per_sender", "packet_bytes", "capacity_packets"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        for name in ("link_gbps", "interval_us"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")
        if type(self.staggered) is not bool:
            raise ValueError("staggered must be a boolean")
        if self.senders * self.packets_per_sender > 1_000_000:
            raise ValueError("educational model limited to 1,000,000 packets")


def percentile(values, percent):
    """Nearest-rank percentile. Empty populations return None."""
    if not 0 < percent <= 100:
        raise ValueError("percent must be in (0, 100]")
    return sorted(values)[ceil(len(values) * percent / 100) - 1] if values else None


def simulate(config):
    config.validate()
    service_us = config.packet_bytes * 8 / (config.link_gbps * 1000)
    arrivals = sorted(
        (packet * config.interval_us +
         (sender * config.interval_us / config.senders if config.staggered else 0), sender)
        for sender in range(config.senders)
        for packet in range(config.packets_per_sender)
    )
    # Contains departure timestamps, including the packet currently in service.
    departures = deque()
    latencies = []
    per_sender = [0] * config.senders
    peak = 0
    last_departure = 0.0
    for arrival, sender in arrivals:
        # Departures at the same instant happen before arrivals.
        while departures and departures[0] <= arrival:
            departures.popleft()
        if len(departures) >= config.capacity_packets:
            continue
        departure = max(arrival, departures[-1] if departures else arrival) + service_us
        departures.append(departure)
        latencies.append(departure - arrival)
        per_sender[sender] += 1
        last_departure = departure
        peak = max(peak, len(departures))
    sent = len(arrivals)
    received = len(latencies)
    dropped = sent - received
    duration = last_departure - arrivals[0][0]
    return {
        "evidence_type": "synthetic_single_fifo_model",
        "config": asdict(config),
        "sent_packets": sent,
        "received_packets": received,
        "dropped_packets": dropped,
        "drop_fraction": dropped / sent,
        "received_per_sender": per_sender,
        "peak_system_packets": peak,
        "p50_delivered_packet_latency_us": percentile(latencies, 50),
        "p99_delivered_packet_latency_us": percentile(latencies, 99),
        "last_successful_delivery_us": last_departure,
        "all_packets_delivered_at_us": last_departure if dropped == 0 else None,
        "payload_goodput_gbps": received * config.packet_bytes * 8 / (duration * 1000),
    }
