"""Validate the bundled entry.png and copy it to the grader output dir.

Stdlib only (no PIL). Parses the PNG header and chunk structure by hand
with struct/zlib, verifies dimensions, integrity (CRC per chunk, IDAT
payload, IEND as the final chunk), size limits and the expected sha256/size,
then writes the bytes to os.path.join(MAKEFUN_OUTPUT_DIR, "entry.png").

Usage: python3 -P -s main.py   (MAKEFUN_OUTPUT_DIR must point at an
existing, empty directory outside this repository)
"""
import hashlib
import os
import struct
import sys
import zlib

# Filled in by the revision pass below after the first verified render.
EXPECTED_SHA256 = "9424cb296e12a8f1c2c10770e48ec1a39f05d00ad353cf0abc39aa39e5752a2f"
EXPECTED_SIZE = 147127

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MIN_SIZE = 10_000
MAX_SIZE = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def read_source():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail("cannot read bundled entry.png: %s" % exc)
    return path, data


def validate_png(data):
    if len(data) < MIN_SIZE:
        fail("PNG too small (%d bytes)" % len(data))
    if len(data) > MAX_SIZE:
        fail("PNG too large (%d bytes, limit %d)" % (len(data), MAX_SIZE))
    if data[:8] != PNG_SIGNATURE:
        fail("bad PNG signature")
    # First chunk must be IHDR, 13 bytes: 1024x1024, bit depth 8,
    # colour type 2 (RGB) or 6 (RGBA), compression/filter/interlace 0.
    if len(data) < 33:
        fail("truncated PNG (no IHDR)")
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk is not a 13-byte IHDR")
    width, height, depth, colour, comp, filt, inter = struct.unpack(
        ">IIBBBBB", data[16:29])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        fail("unexpected dimensions %dx%d" % (width, height))
    if depth != 8 or colour not in (2, 6):
        fail("unexpected bit depth %d / colour type %d" % (depth, colour))
    if comp != 0 or filt != 0 or inter != 0:
        fail("unexpected compression/filter/interlace flags")
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != ihdr_crc:
        fail("CRC mismatch in chunk b'IHDR'")
    # Walk the remaining chunks: CRC each, IDAT non-empty with a
    # meaningful payload, IEND 0-byte and the final chunk, no trailing data.
    pos = 33
    idat_total = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header at offset %d" % pos)
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            fail("truncated chunk %r at offset %d" % (ctype, pos))
        crc_stored = struct.unpack(">I", data[pos + 8 + length:end])[0]
        if zlib.crc32(ctype + data[pos + 8:pos + 8 + length]) & 0xFFFFFFFF != crc_stored:
            fail("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if length == 0:
                fail("empty IDAT chunk")
            idat_total += length
        if ctype == b"IEND":
            if length != 0:
                fail("IEND chunk must be empty")
            if end != len(data):
                fail("trailing data after IEND")
            saw_iend = True
            pos = end
            break
        pos = end
    if not saw_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small (%d bytes)" % idat_total)


def main():
    src_path, data = read_source()
    validate_png(data)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "PLACEHOLDER" and sha != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s" % sha)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        fail("size mismatch: got %d, expected %d" % (len(data), EXPECTED_SIZE))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    repo_abs = os.path.dirname(os.path.abspath(__file__))
    if out_dir_abs == repo_abs or out_dir_abs.startswith(repo_abs + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repository")
    if not os.path.isdir(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR does not exist or is not a directory: %s" % out_dir)
    if os.path.exists(os.path.join(out_dir_abs, "entry.png")):
        fail("output entry.png already exists (refusing to overwrite)")
    if os.path.abspath(src_path) == os.path.join(out_dir_abs, "entry.png"):
        fail("output would overwrite the source image")
    out_path = os.path.join(out_dir_abs, "entry.png")
    with open(out_path, "wb") as fh:
        fh.write(data)
    # Re-read and confirm byte-identical output.
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        fail("written output differs from source")
    print("OK entry.png %d bytes sha256 %s -> %s" % (len(data), sha, out_path))


if __name__ == "__main__":
    main()
