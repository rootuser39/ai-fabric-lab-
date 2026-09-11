import unittest
from dataclasses import replace
from pathlib import Path

from fabriclab.incast import Config, percentile, simulate
from fabriclab.nccl import parse


class IncastTests(unittest.TestCase):
    def test_conservation_and_capacity(self):
        for senders in (1, 2, 8, 16):
            for capacity in (1, 4, 8):
                for staggered in (False, True):
                    result = simulate(Config(senders=senders, capacity_packets=capacity, staggered=staggered))
                    self.assertEqual(result['sent_packets'], result['received_packets'] + result['dropped_packets'])
                    self.assertEqual(result['received_packets'], sum(result['received_per_sender']))
                    self.assertLessEqual(result['peak_system_packets'], capacity)
                    self.assertLessEqual(result['payload_goodput_gbps'], 8.00000001)

    def test_exact_default(self):
        result = simulate(Config())
        self.assertEqual(result['dropped_packets'], 256)
        self.assertEqual(result['p99_delivered_packet_latency_us'], 4)
        self.assertIsNone(result['all_packets_delivered_at_us'])

    def test_staggered(self):
        result = simulate(Config(staggered=True))
        self.assertEqual(result['dropped_packets'], 0)
        self.assertEqual(result['p99_delivered_packet_latency_us'], 1)
        self.assertEqual(result['all_packets_delivered_at_us'], 1023)

    def test_large_buffer(self):
        result = simulate(Config(capacity_packets=8))
        self.assertEqual(result['dropped_packets'], 0)
        self.assertEqual(result['p99_delivered_packet_latency_us'], 8)

    def test_staggering_cannot_fix_overload(self):
        self.assertGreater(simulate(Config(interval_us=4, staggered=True))['dropped_packets'], 0)

    def test_single_sender(self):
        result = simulate(Config(senders=1, capacity_packets=1))
        self.assertEqual(result['dropped_packets'], 0)
        self.assertEqual(result['p99_delivered_packet_latency_us'], 1)

    def test_equal_time_departure_precedes_arrival(self):
        result = simulate(Config(senders=1, interval_us=1, capacity_packets=1))
        self.assertEqual(result['dropped_packets'], 0)

    def test_repeatability(self):
        self.assertEqual(simulate(Config()), simulate(Config()))

    def test_invalid_config(self):
        for field, value in [('senders', 0), ('senders', True), ('packets_per_sender', -1),
                             ('capacity_packets', 0), ('packet_bytes', 1.5), ('link_gbps', 0),
                             ('link_gbps', float('nan')), ('interval_us', float('inf')),
                             ('staggered', 1), ('senders', 1_000_001)]:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                simulate(replace(Config(), **{field: value}))

    def test_nearest_rank(self):
        self.assertEqual(percentile([4, 1, 3, 2], 50), 2)
        self.assertEqual(percentile([4, 1, 3, 2], 99), 4)
        self.assertIsNone(percentile([], 99))
        with self.assertRaises(ValueError):
            percentile([1], 0)


class NcclTests(unittest.TestCase):
    def setUp(self):
        self.log = (Path(__file__).resolve().parents[1] / 'examples/nccl_synthetic.txt').read_text()

    def test_valid(self):
        result = parse(self.log)
        self.assertEqual(len(result['rows']), 2)
        self.assertEqual(result['correctness_status'], 'zero_errors_reported')
        self.assertEqual(result['rows'][1]['out_of_place']['busbw_GBps'], 160)

    def test_unknown_is_not_pass(self):
        self.assertEqual(parse(self.log.replace('160.00 0', '160.00 N/A'))['correctness_status'], 'unknown')

    def test_errors_surface(self):
        self.assertEqual(parse(self.log.replace('160.00 0', '160.00 7'))['correctness_status'], 'errors_reported')

    def test_bad_number(self):
        for value in ('nan', 'inf', '-1', 'oops'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse(self.log.replace('160.00', value))

    def test_missing_header(self):
        with self.assertRaises(ValueError):
            parse('\n'.join(line for line in self.log.splitlines() if not line.startswith('#')))

    def test_unsupported_header(self):
        with self.assertRaises(ValueError):
            parse(self.log.replace('#wrong', 'i_p99'))

    def test_extra_column(self):
        with self.assertRaises(ValueError):
            parse(self.log.replace('160.00 0', '160.00 0 99'))

    def test_empty(self):
        with self.assertRaises(ValueError):
            parse('# nothing here')


if __name__ == '__main__':
    unittest.main()
