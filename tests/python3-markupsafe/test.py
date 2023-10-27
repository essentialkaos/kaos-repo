#!/usr/bin/env python3

import sys
from markupsafe import escape

print(escape("<script>alert(document.cookie);</script>"))

sys.exit(0)
