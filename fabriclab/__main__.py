import argparse
import json
from pathlib import Path

from .incast import Config, simulate
from .nccl import parse


def main():
    parser = argparse.ArgumentParser(description="AI Fabric Lab: synthetic experiments and NCCL log reading")
    commands = parser.add_subparsers(dest="command", required=True)
    experiment = commands.add_parser("incast")
    experiment.add_argument("--senders", type=int, default=8)
    experiment.add_argument("--packets", type=int, default=64)
    experiment.add_argument("--capacity", type=int, default=4)
    experiment.add_argument("--interval-us", type=float, default=16)
    experiment.add_argument("--link-gbps", type=float, default=8)
    experiment.add_argument("--staggered", action="store_true")
    commands.add_parser("suite")
    logs = commands.add_parser("nccl")
    logs.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "incast":
            result = simulate(Config(senders=args.senders, packets_per_sender=args.packets,
                                     capacity_packets=args.capacity, interval_us=args.interval_us,
                                     link_gbps=args.link_gbps, staggered=args.staggered))
        elif args.command == "suite":
            result = {"synchronized": simulate(Config()),
                      "staggered": simulate(Config(staggered=True)),
                      "larger_buffer": simulate(Config(capacity_packets=8)),
                      "sustained_overload": simulate(Config(interval_us=4, staggered=True))}
        else:
            result = parse(args.path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
