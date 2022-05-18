# -*- coding: utf-8 -*-
import os
import sys

__author__ = "joe-tester"

# root path
BASEDIR = os.path.dirname(os.path.dirname(__file__)) if "win" in sys.platform else os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

# other path
REPORTDIR = os.path.join(BASEDIR, "xlsxReports")
LOG_DIR = os.path.join(BASEDIR, 'logs')
ScreenShot_DIR = os.path.join(BASEDIR, "ScreenShot")

CPU_MEM_PATH = os.path.join(REPORTDIR, 'cpu_netflow_mem_report.xlsx')
TIME_PATH = os.path.join(REPORTDIR, 'app_start_time.xlsx')

TESTDATAPATH = os.path.join(BASEDIR,"TestData")

PNGREPORTSPATH = os.path.join(BASEDIR,"pngReports")

MEMINFOPATH = os.path.join(TESTDATAPATH,"meminfo")

CPUINFOPATH = os.path.join(TESTDATAPATH,"cpuinfo")

CONFIGPATH = os.path.join(BASEDIR,"config")

if not os.path.exists(ScreenShot_DIR):
    os.makedirs(ScreenShot_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(REPORTDIR):
    os.makedirs(REPORTDIR)

if not os.path.exists(TESTDATAPATH):
    os.makedirs(CPUINFOPATH)
    os.makedirs(MEMINFOPATH)

if not  os.path.exists(PNGREPORTSPATH):
    os.makedirs(PNGREPORTSPATH)
    
if __name__ == '__main__':
    print(BASEDIR)