"""Strict reader for the classic 13-column nccl-tests stdout table."""

from math import isfinite


HEADER = ["size", "count", "type", "redop", "root", "time", "algbw", "busbw", "#wrong",
          "time", "algbw", "busbw", "#wrong"]


def parse(text):
    rows = []
    recognized_header = False
    for line_number, line in enumerate(text.splitlines(), 1):
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "#" and len(fields) > 1 and fields[1] == "size":
            if fields[1:] != HEADER:
                raise ValueError(f"line {line_number}: unsupported NCCL table header")
            recognized_header = True
            continue
        if line.lstrip().startswith("#"):
            continue
        if not fields[0].lstrip("+-").isdigit():
            if recognized_header:
                raise ValueError(f"line {line_number}: unexpected output after table header")
            continue
        if not recognized_header or len(fields) != 13:
            raise ValueError(f"line {line_number}: expected classic 13-column table with header")
        try:
            size, count, root = int(fields[0]), int(fields[1]), int(fields[4])
            if size < 0 or count < 0:
                raise ValueError("negative size/count")
            row = {"size_bytes": size, "count": count, "datatype": fields[2],
                   "operation": fields[3], "root": root}
            for mode, offset in (("out_of_place", 5), ("in_place", 9)):
                timing, algbw, busbw = map(float, fields[offset:offset + 3])
                if any(not isfinite(x) or x < 0 for x in (timing, algbw, busbw)):
                    raise ValueError("invalid performance value")
                wrong = None if fields[offset + 3] == "N/A" else int(fields[offset + 3])
                if wrong is not None and wrong < 0:
                    raise ValueError("negative correctness count")
                row[mode] = {"time_reported": timing, "algbw_GBps": algbw,
                             "busbw_GBps": busbw, "wrong": wrong}
            rows.append(row)
        except ValueError as error:
            raise ValueError(f"line {line_number}: {error}") from error
    if not rows:
        raise ValueError("no supported NCCL results found")
    counts = [row[mode]["wrong"] for row in rows for mode in ("out_of_place", "in_place")]
    status = ("errors_reported" if any(x is not None and x > 0 for x in counts)
              else "unknown" if any(x is None for x in counts) else "zero_errors_reported")
    return {"evidence_type": "user_supplied_nccl_text_not_hardware_verified",
            "correctness_status": status,
            "timing_unit": "read_from_original_log_units_header",
            "note": "Rows summarize runs; no per-iteration p99 inferred. Retain the original log.",
            "rows": rows}
