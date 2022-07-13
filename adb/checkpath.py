# encoding: utf-8

import platform
import subprocess

from utils.logger import logger

__author__ = "joe-tester"


@logger('Use the corresponding command according to the current system')
def get_sys_env():
    system = platform.system()
    find_manage = 'findstr'
    if system != 'Windows':
        find_manage = 'grep'
    return find_manage


@logger('get devices')
def get_device_list():
    result = subprocess.Popen(
        "adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    devices = [line.split()[0].decode("utf-8") for line in result[1:-1]]
    return devices
