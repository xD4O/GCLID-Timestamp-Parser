#!/usr/bin/env python3
# 'python gclid_timestamp.py' to run. Enter the Google Click ID Parameter, typically found after the URL.
# Example: www.example.com/running-shoes?gclid=123xyz
# The 'gclid=123xyz' part is the GCLID. Paste in 123xyz when it asks for the Google Click ID.
import base64
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/New_York")

def add_padding(s: str) -> str:
    # Base64 length must be a multiple of 4
    return s + "=" * ((4 - len(s) % 4) % 4)

def b64url_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(add_padding(s))

def parse_varints(data: bytes):
    """
    Yield (start_offset, end_offset, value) for each Protobuf-style varint.
    Varint = 7 bits per byte, MSB=1 means continue, MSB=0 is last byte.
    """
    i = 0
    n = len(data)
    while i < n:
        start = i
        val = 0
        shift = 0
        while i < n:
            b = data[i]
            i += 1
            val |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7
        yield (start, i, val)

def classify_epoch_units(v: int):
    """
    Heuristic classification by magnitude:
      - microseconds: ~1e15 range for current dates
      - milliseconds: ~1e12
      - seconds:      ~1e9
    Returns (unit_name, seconds_float) or (None, None) if not plausible.
    """
    if 10**14 <= v <= 10**16:
        return "microseconds", v / 1_000_000.0
    if 10**11 <= v <= 10**13:
        return "milliseconds", v / 1_000.0
    if 10**9 <= v <= 10**10:
        return "seconds", float(v)
    return None, None

def find_best_timestamp_varint(raw: bytes):
    """
    Scan all varints and pick the best timestamp-like one.
    Preference order by unit: microseconds > milliseconds > seconds.
    Within same unit, pick the largest (usually most recent).
    """
    buckets = {"microseconds": [], "milliseconds": [], "seconds": []}
    for start, end, val in parse_varints(raw):
        unit, secs = classify_epoch_units(val)
        if unit:
            buckets[unit].append((start, end, val, secs))

    for unit in ("microseconds", "milliseconds", "seconds"):
        if buckets[unit]:
            # pick the largest value (most recent)
            start, end, val, secs = max(buckets[unit], key=lambda x: x[3])
            return unit, start, end, val, secs

    return None

def main():
    gclid = input("Enter GCLID: ").strip()
    if not gclid:
        print("No GCLID provided.")
        return

    print(f"\nCharacter length: {len(gclid)}")

    try:
        raw = b64url_decode(gclid)
    except Exception as e:
        print(f"Decode error: {e}")
        return

    result = find_best_timestamp_varint(raw)
    if not result:
        print("No plausible timestamp-like varint found in this GCLID.")
        return

    unit, start, end, val, secs = result
    dt_utc = datetime.fromtimestamp(secs, tz=timezone.utc)
    dt_local = dt_utc.astimezone(LOCAL_TZ)

    print("Timestamp (raw integer):", val)
    print("Assumed units:", unit)
    print("UTC datetime:", dt_utc.isoformat())
    print("Local (America/New_York):", dt_local.isoformat())

if __name__ == "__main__":
    main()
