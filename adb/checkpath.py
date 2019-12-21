# encoding: utf-8

import  platform,subprocess
from tools.HandleLogging import logger

@logger('判断系统，使用相应的命令')
def get_sys_env():#获取系统的名称，使用对应的指令
    system=platform.system()
    if system=='Windows':
        find_manage='findstr'
        # find_manage='grep'
    else:
        find_manage='grep'
    return  find_manage

@logger('获取设备列表')
def get_device_list():#获取设备列表
    devices = []
    result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result.reverse()
    for line in result[1:]:
        if "attached" not in line.strip():
            devices.append(line.split()[0])
        else:
            break
    return devices


