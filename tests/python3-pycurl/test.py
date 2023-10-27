#!/usr/bin/env python3

import pycurl
from io import BytesIO

c = pycurl.Curl()
buf = BytesIO()
c.setopt(pycurl.URL, 'https://github.com/essentialkaos')
c.setopt(pycurl.WRITEFUNCTION, buf.write)
c.perform()

print(c.getinfo(pycurl.HTTP_CODE))
