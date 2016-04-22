#!/usr/bin/env python

import fileinput

for line in fileinput.input():
    print ' '.join(sorted(line.split()))

