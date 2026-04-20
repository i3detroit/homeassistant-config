#!/usr/bin/env python3

import sys
from telnetlib import Telnet

msg = sys.stdin.readline()

tn = Telnet('10.13.107.44')
tn.write(msg.encode('ascii') + b'\n')
tn.close()