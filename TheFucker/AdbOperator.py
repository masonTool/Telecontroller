#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mason created

"""
import subprocess
import platform
import GlobalValue
import re

adb = './adb/%s_adb' % platform.system()


def executeCommand(cmd):
    return str(subprocess.check_output(cmd.split(' ')))


def getDevices():
    result = executeCommand('%s devices' %adb).split('\\n')[1:-2]
    return list(map(lambda it: it.split('\\t')[0], result))

def inputEvent(keycode):
    executeCommand('%s -s %s shell input keyevent %s' %(adb, GlobalValue.connectedDevice, keycode))
    pass

def getPhoneSize():
    result = executeCommand('%s -s %s shell wm size' %(adb, GlobalValue.connectedDevice))
    # result = executeCommand(adbPath + ' shell wm size')
    groups = re.match(r'.*?(?P<width>\d+)x(?P<height>\d+)', result)
    return [int(groups['width']), int(groups['height'])]

def buildBridge(pc_port, phone_port):
    # executeCommand('%s forward tcp:%s tcp:9999' % (adb, port))
    executeCommand('%s -s %s forward tcp:%s tcp:%s' % (adb, GlobalValue.connectedDevice, pc_port, phone_port))
    pass


if __name__ == '__main__':
    print(getDevices())
    # print(getPhoneSize())
    buildBridge(GlobalValue.pc_port, GlobalValue.phone_port)
