# 备注说明：
# APP性能数据，内存，CPU，流量等，自动生成数据图


import os, time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime


def csv2images(src):
    target_dir = os.getcwd()
    package_name, iphone_info = tets_info(src)


    plt.figure(figsize=(19.20, 10.80))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    data = pd.read_csv(src)
    
    data['time'] = data['time'].apply( lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"))

    timestr = time.strftime("%Y-%m-%d %H:%M")

    # network
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

    plt.subplot(7, 1, 2)
    plt.plot(data['time'], data['txBytes'], label='all')
    plt.plot(data['time'], data['txTcpBytes'], 'r--', label='tcp')
    plt.legend()
    # plt.xlabel('Time')
    plt.ylabel('Send(KB)')
    plt.ylim(ymin=0)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())
    # .clf()

    plt.subplot(7, 1, 3)

    plt.plot(data['time'], data['mem'], '-')
    plt.ylabel('mem(MB)')
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())

    plt.subplot(7, 1, 4)
    plt.plot(data['time'], data['cpu'], 'r--', label='cpu')  # systemCpu
    plt.plot(data['time'], data['systemCpu'], label='systemCpu')  # systemCpu
    plt.legend()
    plt.ylim(0, max(100, data['cpu'].max()))
    plt.ylabel('CPU')
    plt.ylim(ymin=0)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())

    plt.subplot(7, 1, 5)
    plt.plot(data['time'], data['fps'], '-')
    plt.ylabel('FPS')
    plt.ylim(-1, 60)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())

    plt.subplot(7, 1, 6)
    plt.plot(data['time'], data['level'], '-')
    plt.ylabel('level')
    plt.ylim(0, 110)
    plt.gca().xaxis.set_major_formatter(ticker.NullFormatter())

    plt.subplot(7, 1, 7)
    plt.plot(data['time'], data['batterytem'], '-')
    plt.ylim(0, 100)
    plt.ylabel('BatteryTem')
    plt.xlabel('Time')

    # 定义图片保存的目录
    image_file = os.path.dirname(os.path.dirname(__file__)) + '/TestData/'

    plt.savefig(os.path.join(target_dir, image_file,src.split("/")[-1].split('.')[0] +".png"))


def tets_info(src):

    data = pd.read_csv(src)

    pack = (data['package'][0]).replace(" ", '')

    iphone = (data['iphone_info'][0])

    return [pack, iphone]


if __name__ == '__main__':

    # 定义保存性能数据的目录
    performance_file = os.path.dirname(os.path.dirname(__file__)) + '/TestData/'
    # 读取性能数据列表中【-1】代表最后1个数据列表
    src = (performance_file + "performance_data/" + os.listdir((performance_file + "performance_data"))[-1])
    
    csv2images(src)