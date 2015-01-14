#!/usr/bin/python
#coding=utf-8

import os
import subprocess
import sys

import leo.core.leoBridge as leoBridge

Target = 'foo.leo'

def main():
    if os.path.isfile(Target):
        os.remove(Target)
    idxList = range(4)
    if sys.version_info.major == 2:
        pyVer = 'python2'
    else:
        pyVer = 'python3'
    for idx in idxList:
        returnCode = subprocess.call([pyVer, 'slave.py', str(idx)])
        if returnCode:
            print('subprocess return code = {0}'.format(returnCode))

    bridge = leoBridge.controller(gui='nullGui', verbose=False,
        loadPlugins=False, readSettings=False)
    leoG = bridge.globals()
    cmdr1 = bridge.openLeoFile('foo.leo')
    expList = ['NewHeadline'] + [str(idx) for idx in idxList]
    for idx, posx in enumerate(cmdr1.all_positions_iter()):
        if posx.h != expList[idx]:
            print('*** Problem:  Probably duplicate GNXs ***')
            for posx in cmdr1.all_positions_iter():
                print ('headline "{hdl}" gnx {gnx}'.format(
                        hdl=posx.h, gnx=posx.v.gnx))
            break
    else:
        print('Test Passed.  No Error Detected.')

if __name__ == "__main__":
    main()
