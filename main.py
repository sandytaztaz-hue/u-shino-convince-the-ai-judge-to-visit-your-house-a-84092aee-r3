#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House — Round 3 entry.

Writes the finished invitation photograph to /output/entry.png.

The photograph itself (invitation.png, shipped beside this file) is the
entry: a warm, photorealistic shot of the printed invitation letter on a
wooden table in evening light, with a steaming cup of tea and a sleeping
dog's paw at the frame's edge. Nothing in the frame touches the text.

This program does one small, deterministic job: it checks the shipped
image against the competition gate (whole PNG, at most 1 MiB, at most
1024 by 1024 pixels) and copies its exact bytes to the output path the
grader reads. Two runs write byte-identical files.

Standard library only — the grading sandbox installs nothing.
"""

import os
import struct
import sys

ASSET_NAME = "invitation.png"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def read_png_size(blob):
    """Return (width, height) from a PNG byte string, or None if malformed."""
    if len(blob) < 24 or blob[:8] != PNG_SIGNATURE:
        return None
    if blob[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def check_asset(blob):
    """Check the shipped image against the gate. Return (w, h) or None."""
    if len(blob) > MAX_BYTES:
        print("error: image is %d bytes, over the 1 MiB gate" % len(blob),
              file=sys.stderr)
        return None
    size = read_png_size(blob)
    if size is None:
        print("error: shipped image is not a whole PNG", file=sys.stderr)
        return None
    width, height = size
    if width > MAX_SIDE or height > MAX_SIDE:
        print("error: image is %dx%d, over the 1024x1024 gate"
              % (width, height), file=sys.stderr)
        return None
    return size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.join(here, ASSET_NAME)
    try:
        with open(asset_path, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        return fail("cannot read %s: %s" % (ASSET_NAME, exc))

    size = check_asset(blob)
    if size is None:
        return 1
    width, height = size

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        return fail("cannot create output dir %s: %s" % (out_dir, exc))
    out_path = os.path.join(out_dir, OUTPUT_NAME)
    try:
        with open(out_path, "wb") as handle:
            handle.write(blob)
    except OSError as exc:
        return fail("cannot write %s: %s" % (out_path, exc))

    print("wrote %s: %dx%d PNG, %d bytes" % (out_path, width, height,
                                             len(blob)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
