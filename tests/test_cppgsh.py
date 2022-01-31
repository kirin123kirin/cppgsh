#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from timeit import timeit
from psutil import Process

from os.path import dirname, abspath, join as pjoin
shome = abspath(pjoin(dirname(__file__), ".."))
sys.path.insert(0, pjoin(shome, "build"))
try:
    from cppgsh import *
except (ImportError, ModuleNotFoundError):
    from cppgsh.cppgsh import *

process = Process(os.getpid())
def memusage():
    return process.memory_info()[0] / 1024

def runtimeit(funcstr, number=10000):
    i = 0

    for fc in funcstr.strip().splitlines():
        fc = fc.strip()
        if i == 0:
            timeit(fc, globals=globals(), number=number)
        bm = memusage()
        p = timeit(fc, globals=globals(), number=number)

        am = (memusage() - bm)
        assert am < 1000, "{} function {}KB Memory Leak Error".format(fc, am)
        try:
            print("{}: {} ns (mem after {}KB)".format(fc, int(1000000000 * p / number), am))
        except UnicodeEncodeError:
            print("<UnicodeError text>: {} ns (mem after {}KB)".format(int(1000000000 * p / number), am))
        i += 1

def test_cppgsh():
    assert(True)

if __name__ == '__main__':
    import os
    import traceback

    curdir = os.getcwd()
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        for fn, func in dict(locals()).items():
            if fn.startswith("test_"):
                print("Runner: %s" % fn)
                func()
    except Exception as e:
        traceback.print_exc()
        raise (e)
    finally:
        os.chdir(curdir)
