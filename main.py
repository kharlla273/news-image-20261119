#!/usr/bin/env python3
"""news-image-20261119: the entry image is drawn by draw.py and held in
this repository as entry.png. This program copies it into the output
directory the grader provides, so both runs write byte-identical files.
(draw.py runs at build time only; the grader runs this file with no
network, standard library only, so the image ships in the repo.)
"""
import os
import shutil
import sys

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)

here = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(out_dir, "entry.png")
shutil.copyfile(os.path.join(here, "entry.png"), dest)

with open(dest, "rb") as f:
    magic = f.read(8)
if magic != b"\x89PNG\r\n\x1a\n":
    print("error: copied entry.png has an invalid PNG signature", file=sys.stderr)
    sys.exit(1)

size = os.path.getsize(dest)
src_size = os.path.getsize(os.path.join(here, "entry.png"))
if size != src_size:
    print(f"error: copied entry.png is {size} bytes, expected {src_size} bytes", file=sys.stderr)
    sys.exit(1)
if size > 1048576:
    sys.exit(f"entry.png is {size} bytes, over the 1 MiB limit")
print(f"wrote {dest} ({size} bytes)")
