# -*- coding: utf-8 -*-
# Read the CSV file collecting app performance test data and generate two-dimensional pictures

import datetime
import os, time

from common.configpath import PERFPATH, PNGREPORTSPATH
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


def csv2images(src):
    
    target_dir = os.getcwd()
    
    package_name, iphone_info = tets_info(src)
    
    plt.figure(figsize=(19.20, 10.80))
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    data = pd.read_csv(src)
    
    data['time'] = data['time'].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"))

    timestr = time.strftime("%Y-%m-%d %H:%M")
    
    # network rcv
    rx_str = round(data['rxBytes'].sum(), 2)
    tx_str = round(data['txBytes'].sum(), 2)

    plt.subplot(7, 1, 1)
    plt.plot(data['time'], data['rxBytes'], label='all')
    plt.plot(data['time'], data['rxTcpBytes'], 'r--', label='tcp')
    plt.legend()

    plt.title(
        '\n'.join(
            ["Summary", iphone_info, src.split("/")[-1], package_name, timestr,
             'Recv %s KB, Send %s KB' % (rx_str, tx_str)]),
        loc='left')
    
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())

    plt.ylabel('Recv(KB)')
    
    plt.ylim(ymin=0)
    # network send
    plt.subplot(7, 1, 2)
    plt.plot(data['time'], data['txBytes'], label='all')
    plt.plot(data['time'], data['txTcpBytes'], 'r--', label='tcp')
    plt.legend()
    # plt.xlabel('Time')
    plt.ylabel('Send(KB)')
    plt.ylim(ymin=0)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
    # .clf()
    
    # meninfo
    plt.subplot(7, 1, 3)
    plt.plot(data['time'], data['mem'], '-')
    plt.ylabel('mem(MB)')
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
    
    # cpuinfo
    plt.subplot(7, 1, 4)
    plt.plot(data['time'], data['cpu'], 'r--', label='cpu')  # systemCpu
    plt.plot(data['time'], data['systemCpu'], label='systemCpu')  # systemCpu
    plt.legend()
    plt.ylim(0, max(100, data['cpu'].max()))
    plt.ylabel('CPU')
    plt.ylim(ymin=0)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
    
    # FPS
    plt.subplot(7, 1, 5)
    plt.plot(data['time'], data['fps'], '-')
    plt.ylabel('FPS')
    plt.ylim(-1, 60)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
    
    # battery level
    plt.subplot(7, 1, 6)
    plt.plot(data['time'], data['level'], '-')
    plt.ylabel('level')
    plt.ylim(0, 110)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())

    # SystemBattery
    plt.subplot(7, 1, 7)
    plt.plot(data['time'], data['batterytem'], '-')
    plt.ylim(0, 100)
    plt.ylabel('BatteryTem')
    plt.xlabel('Time')
    
    # Define the directory where pictures are saved
    plt.savefig(os.path.join(PNGREPORTSPATH, src.split("\\")[-1].split('.')[-2] +".png"))


def tets_info(src):
    data = pd.read_csv(src)
    print(data)
    pack = (data['package'][0]).replace(" ", '')
    iphone = (data['iphone_info'][0])
    return [pack, iphone]


if __name__ == '__main__':
    src = (os.path.join(PERFPATH , os.listdir(PERFPATH)[-1]))
    csv2images(src)