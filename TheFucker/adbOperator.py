#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Mason created

"""
import subprocess

def executeCommand(cmd):
    return str(subprocess.check_output(cmd.split(' ')))

def getDevices():
    result = executeCommand('./adb devices').split('\\n')[1:-2]
    return list(map(lambda it:it.split('\\t')[0], result))



if __name__ == '__main__':
    print(getDevices())
