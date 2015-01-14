#!/usr/bin/python
#coding=utf-8

import sys

import leo.core.leoBridge as leoBridge

Target = 'foo.leo'

def main():
    idx = sys.argv[1]
    bridge = leoBridge.controller(gui='nullGui', verbose=False,
        loadPlugins=False, readSettings=False)
    leoG = bridge.globals()
    cmdr1 = bridge.openLeoFile(Target)
    rp = cmdr1.rootPosition()
    posx = rp.insertAsLastChild()
    posx.h = '{idx}'.format(idx=idx)
    cmdr1.save()
    cmdr1.close()

if __name__ == "__main__":
    main()
