#!/usr/bin/env python3

import zstd
import sys

data = b"TEST1234TEST1234TEST1234TEST1234TEST1234TEST1234"
zdata = zstd.compress(data, 1)

if data != zstd.decompress(zdata):
  sys.exit(1)

if len(zdata) >= len(data):
  sys.exit(2)

sys.exit(0)
