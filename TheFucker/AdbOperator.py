#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mason created

"""
import subprocess
import platform
import GlobalValue

adbPath = './adb/' + platform.system() + '_adb'


def executeCommand(cmd):
    return str(subprocess.check_output(cmd.split(' ')))


def getDevices():
    result = executeCommand(adbPath + ' devices').split('\\n')[1:-2]
    return list(map(lambda it:it.split('\\t')[0], result))

def inputEvent(keycode):
    executeCommand(adbPath + ' -s ' +  GlobalValue.connectedDevice + ' shell input keyevent ' + keycode)
    pass

def getPhoneSize():
    return list(map(lambda it:int(it), executeCommand(adbPath + ' -s ' + GlobalValue.connectedDevice + ' shell wm size').split('x')))


if __name__ == '__main__':
    print(getDevices())
