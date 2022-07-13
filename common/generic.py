# -*- coding: utf-8 -*-

"""
Created on 2022年5月19日

@author: qguan
"""

__author__ = "joe-tester"

import os


def del_file(path):
    ls = os.listdir(path)
    for s in ls:
        d_path = os.path.join(path,s)
        if os.path.isdir(d_path):
            del_file(d_path)
        else:
            os.remove(d_path)