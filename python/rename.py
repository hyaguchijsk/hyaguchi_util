#!/usr/bin/env python

import os
import re

def rename(dir):

    files=os.listdir(dir)
    for fname in files:
        print fname


