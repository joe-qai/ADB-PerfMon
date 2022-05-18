# 备注说明：

# APP启动时间的统计脚本，自动生成数据表格
# 如果需要换APP程序，请更新以下内容：
# 更新包名和Activity：
# 请查找内容：

# （1）通过cmd启动app程序
    # cmd = 'adb shell am start -W -n com.fundrive.truck.mobile/com.mapbar.android.MainActivity '

    # 然后替换“com.fundrive.truck.mobile/com.mapbar.android.MainActivity ”

# （2） package='com.fundrive.truck.mobile/com.mapbar.android.MainActivity'

        # 然后替换“com.fundrive.truck.mobile/com.mapbar.android.MainActivity ”

# （3）  # adb关闭APP
    # os.popen('adb shell am force-stop com.fundrive.truck.mobile')

    # 然后替换包名 “com.fundrive.truck.mobile ”


import time
import xlwt
import os
import logging.config
import xlrd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

CON_LOG = '../config/log.conf'
#logging.config.fileConfig(CON_LOG)
logging = logging.getLogger()


# 指定默认字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
# 解决保存图像是负号'-'显示为方块的问题
mpl.rcParams['axes.unicode_minus'] = False

# 定义保存app启动时间数据的目录
startTime_file = os.path.dirname(os.path.dirname(__file__)) + '/TestData/'

# 判断有没有这个数据目录，没有的话创建，有的话pass
if os.path.exists(startTime_file + "/startTime"):

    pass

else:

    os.makedirs(startTime_file + "/startTime")


# 启动app，获取启动时间
def launch_app():
    cmd = 'adb shell am start -W -n com.tencent.mm/com.tencent.mm.ui.LauncherUI'
    # 运行cmd命令
    count = os.popen(cmd)

    for line in count.readlines():

        if "WaitTime" in line:

            startTime = line.split(':')[1]

            break

    return startTime.strip()

# 创建表格
file = xlwt.Workbook()

# 创建sheet
table = file.add_sheet("app启动时间", cell_overwrite_ok=True)

# 写入时间
table.write(0, 0, '时间')

# 写入启动用时
table.write(0, 1, '启动用时')

# 写入单位
table.write(0, 2, '单位/s')


time_li = []

row = 1

while row < 31:

    # 调用app启动的方法
    now = launch_app()
    
    # 在第一列写入当前系统时间
    table.write(row, 0, time.strftime('%H:%M:%S', time.localtime()))
    
    # 在第二列写入启动用时
    table.write(row, 1, int(now) / 1000)
    
    if row > 1:
    
        time_li.append(int(now))
    
    time.sleep(6)
    
    
    cmd = 'adb shell am force-stop com.tencent.mm'
    
    os.popen(cmd)
    
    row += 1
    
    try:
    
        # 自定义数据名称
        file.save(startTime_file + "/startTime/" + 'APP启动时间' + '.xls')
        # 通过时间定义数据的名称
        # file.save(performance_file + "/startTime/" + time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())) + '.xls')
    
    except PermissionError:
        print("被测应用权限不足，无法使用adb测试启动时间!!!")
        pass
    
    time.sleep(3)

# # 定义保存性能数据的目录
performance_file = os.path.dirname(os.path.dirname(__file__)) + '/TestData/'
# 读取性能数据列表中【-1】代表最后1个数据列表
startTime_file = (performance_file + "/startTime/" + os.listdir((performance_file + "/startTime"))[-1])

# 去读取文件
reade_filename = xlrd.open_workbook(startTime_file)

# 通过索引获取 sheet 名称
sheet1_name = reade_filename.sheets()[0]

# 定义展示数据，应于画图
show_filename = pd.read_excel(startTime_file)

# 删除第0行，因为第一行的数据不准
del_data = show_filename.drop([0])

# 打印出删除后的数据
logging.info(del_data)

# 输出日志文件
logging.info("平均值：" + str(sum(time_li) / len(time_li) / 100))
logging.info("最小值：" + str(min(time_li) / 100))
logging.info("最大值：" + str(max(time_li) / 100))

# 根据删除后的数据进行画图
plt.plot(del_data["时间"], del_data["启动用时"], label='启动用时', linewidth=1, color='r', marker='.',
markerfacecolor='blue', markersize=16)
# 定义X坐标
plt.xlabel("时间")
# 定义Y坐标
plt.ylabel('启动用时')
# 定义标题
plt.title("APP启动耗时分析图")

plt.legend()

# Abscissa display interval
if len(time_li) > 15:
    t = int(len(time_li) / 15)
    plt.xticks(range(0, len(time_li), t))
    
plt.gcf().autofmt_xdate()

plt.grid()

# 定义图片保存的目录
image_file = os.path.dirname(os.path.dirname(__file__)) + '/TestData/'

plt.savefig(os.path.join(image_file,time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))))

plt.show()