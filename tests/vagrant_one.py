#!/usr/bin/env python3

import os,sys
sys.path.insert(0, '../')

from sdock import vagrant as v

box = v()
box.prep()