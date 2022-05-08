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

if not os.path.exists(ScreenShot_DIR):
    os.makedirs(ScreenShot_DIR)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(REPORTDIR):
    os.makedirs(REPORTDIR)

if __name__ == '__main__':
    print(BASEDIR)