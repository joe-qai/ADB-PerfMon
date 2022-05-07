# -*- coding: utf-8 -*-
import os
import sys

__author__ = "joe-tester"

if "win" in sys.platform:
    # 工程的根路径root
    BASEDIR = os.path.dirname(os.path.dirname(__file__))
elif "linux" in sys.platform:
    # py文件当前路径
    BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 工程根目录下的文件夹
# 结果路径
REPORTDIR = os.path.join(BASEDIR, "xlsxReports")
LOG_DIR = os.path.join(BASEDIR, 'logs')
ScreenShot_DIR = os.path.join(BASEDIR, "ScreenShot")


if not os.path.exists(ScreenShot_DIR):
    os.makedirs(ScreenShot_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(REPORTDIR):
    os.makedirs(REPORTDIR)
    
if __name__ == '__main__':
    print(os.path.join(REPORTDIR , 'cpu_netflow_men_report.xlsx'))