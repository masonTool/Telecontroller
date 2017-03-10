#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mason created

"""
import subprocess
import platform

adbPath = './adb/' + platform.system() + '_adb'


def executeCommand(cmd):
    return str(subprocess.check_output(cmd.split(' ')))


def getDevices():
    result = executeCommand(adbPath + ' devices').split('\\n')[1:-2]
    return list(map(lambda it:it.split('\\t')[0], result))

if __name__ == '__main__':
    print(getDevices())
