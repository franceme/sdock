#!/usr/bin/env python3

import os,sys
sys.path.insert(0, '../')

from sdock.vagrant import vagrant as v

if os.path.exists("Vagrantfile"):
    os.remove("Vagrantfile")

box = v(
    headless = False
)
box.prep()