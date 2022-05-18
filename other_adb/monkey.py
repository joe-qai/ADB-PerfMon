# coding:utf-8

import os, time
import random
import subprocess
import re


device = ""
package = "com.hcp.flaget"
number = 0
result_true = []
result_false = []
crash_flag = 0
anr_flag = 0


# 获取设备名称
def devices():
    global device, flag
    cmd1 = "adb devices > content/devices.csv"
    os.system(cmd1)
    with open("content/devices.csv", encoding="utf-8", mode="r") as f:  # 筛选出进程包名和activity
        lines = f.readlines()
        for line in lines:
            if "device" in line:
                device = line.split('	')[0]


# 获取包名
def get_package():
    global package
    cmd = 'adb shell dumpsys window | findstr mCurrentFocus > content/info.csv'  # info.csv文件中是当前activity概括信息
    os.system(cmd)
    with open("content/info.csv", encoding="utf-8", mode="r") as f:  # 筛选出进程包名和activity
        lines = f.readlines()
        for line in lines:
            if "mCurrentFocus" in line:
                if "null" in line:
                    continue
                value1 = line.split('{')[1]
                if 'mode' in value1:
                    value2 = value1.split(' ')[4]
                else:
                    value2 = value1.split(' ')[2]
                if "\n" in value2:
                    value = value2.strip("}\n")
                    package = value.split('/')[0]
                else:
                    value = value2.strip("}")
                    package = value.split('/')[0]
                # print(value)
            else:  # 未获取到包名信息则停止脚本
                print("未获取到package信息！脚本终止执行！")


# 开始执行monkey并获取log
def start_monkey():
    global device, package, number
    number = random.randint(1, 500)
    
    cmd1 = "adb -s {} shell monkey -p {} -v -v -v --throttle 10 \
        -s {} --ignore-crashes --ignore-timeouts --ignore-native-crashes \
        --pct-syskeys 0 --pct-anyevent 0 8000000 > log/monkeylog.txt".format(device,package,number)
        
    cmd2 = "adb -s {} logcat -v time *:E > log/logcat.txt".format(device)
    
    print("包名：{}".format(package))
    
    subprocess.Popen(cmd2, shell=True)
    time.sleep(1)
    subprocess.Popen(cmd1, shell=True)
    time.sleep(1)


# 判断monkey是否已经执行结束
def is_finish():
    global result_true, result_false
    with open('log/monkeylog.txt', encoding='utf-8', mode='r') as f:
        lines = f.read()
        pattern1 = re.compile('Monkey finished', re.IGNORECASE)
        pattern2 = re.compile('System appears to have crashed', re.IGNORECASE)
        result_true = pattern1.findall(lines)
        result_false = pattern2.findall(lines)



# 筛选出monkey日志中crash和anr的数量
def select():
    global crash_flag, anr_flag
    with open('log/monkeylog.txt', encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        for line in lines:
            if "crash" in line.lower():
                crash_flag += 1
            if "anr" in line:
                anr_flag += 1


if __name__ == '__main__':
    devices()
    get_package()
    start_monkey()
    while True:
        is_finish()
        if "Monkey finished" in result_true:  # 结果含有"Monkey finished"结果为pass
            print("本次稳定性测试种子值为:{}".format(number))
            select()
            print("monkey日志中存在{}处crash".format(crash_flag))
            print("monkey日志中存在{}处anr".format(anr_flag))
            exit("pass")
        elif "System appears to have crashed" in result_false:  # System appears to have crashed"结果为false
            print("本次稳定性测试种子值为:{}".format(number))
            exit("false")
        else:
            time.sleep(1)