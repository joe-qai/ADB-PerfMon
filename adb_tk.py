# -*- coding: utf-8 -*-
import os
import threading
import time
from tkinter import messagebox, ttk
import tkinter
from tkinter.constants import END, LEFT

from adb.ab_python import starttime_app, adb_monkey, get_device_status, get_cpu_data, get_netflow, get_mem
from adb.configpath import ScreenShot_DIR, BASEDIR
from utils.handler_excel import start_app, get_cpu
from utils.logger import LOG, logger


@logger('启动app时间测试')
def StartAPP():
    start_tim = []
    times = []
    status_shebei = get_device_status()
    if status_shebei == 'device':
        try:
            packname = baoming_t.get('0.0', END).strip()
            acti = activ_t.get('0.0', END).strip()
            get_times = times_act.get()
        except:
            LOG.info('获取不到测试数据，请检查！')
            messagebox.showinfo('提醒', '获取不到测试数据，请检查！')
        if len(acti) <= 1 or len(packname) <= 1:
            messagebox.showinfo('提醒', '包命或者包名activity不能为空')
            LOG.info('包命或者包名activity不能为空')
        else:
            if len(get_times) <= 1:
                messagebox.showinfo('提醒', '次数不能为空')
                LOG.info('次数不能为空')
            else:
                i = 0
                e1['state'] = 'normal'
                e1.delete(1.0, tkinter.END)
                for i in range(int(get_times)):
                    start_time = starttime_app(
                        packagename=packname, packagenameactivicy=acti)
                    start_tim.append(int(start_time[1]))

                    times.append(i)
                    if start_time is None:
                        messagebox.showwarning('警告', '请检查您输入的包或者包的启动activity')
                        break
                    text = '第%s次启动时间：%s' % (i + 1, start_time[1])
                    LOG.info('第%s次启动时间：%s' % (i + 1, start_time[1]))
                    sum += int(start_time[1])
                    e1['state'] = 'normal'
                    e1.insert(tkinter.END, text)
                    e1.insert(tkinter.END, '\n')
                    e1.see(END)
                    btn_start['state'] = 'disabled'
                e1.insert(tkinter.END, ('平均用时:%s' % (sum / int(get_times))))
                LOG.info(('平均用时:%s' % (sum / int(get_times))))
                start_app(times=times, start=start_tim)
                messagebox.showinfo('提示', '测试报告已经生成，请到当前目录查看')
                LOG.info('测试报告已经生成，请到当前目录查看')
                e1['state'] = 'disabled'
                btn_start['state'] = 'normal'
                messagebox.showinfo('通知', '测试已经完成')
                LOG.info('测试已经完成')
    else:
        messagebox.showerror('警告', '设备连接异常')
        LOG.info('设备连接异常')


@logger('monkey测试')
def monkey_app():
    """adb shell monkey -p {0} -s {1} --throttle {2} --pct-touch {3} --pct-motion {4} --pct-trackball  {5}  --pct-nav {6}  
    --pct-majornav {7} --pct-syskeys {8} --pct-appswitch {9}  --pct-flip  {10}  --pct-anyevent {11} -v -v -v {12} >{13}"""
    device_status = get_device_status()
    if device_status == 'device':
        try:
            # 0包名
            packname = pkname.get('0.0', END).split()[0]
            # 1随机数产生的种子
            s = pseudorandom.get('0.0', END).split()[0]
            # 2每次事件发送间隔时间
            interval_times = time_t.get().split()[0]
            # 3点击/触发事件
            click = click_event.get('0.0', END).split()[0]
            # 4滑动事件
            sliding = sliding_event.get('0.0', END).split()[0]
            # 5轨迹球事件
            track = track_event.get('0.0', END).split()[0]
            # 6基本导航
            base_nav = base_navigation_event.get('0.0', END).split()[0]
            # 7主导航
            main_nav = main_navigation_event.get('0.0', END).split()[0]
            # 8系统事件
            syso = system_event.get('0.0', END).split()[0]
            # 9activiry切换事件
            acti = activity_switch_event.get('0.0', END).split()[0]
            # 10键盘唤出事件
            kboard = keyboard_event.get('0.0', END).split()[0]
            # 11其他事件
            others = other_event.get('0.0', END).split()[0]
            # 12 执行次数
            event_times = act_count.get('0.0', END).split()[0]
            # 13	日志路径
            log = log_path.get('0.0', END).split()[0]

            if len(packname) <= 5:
                LOG.info('请正确填写包名')
                messagebox.showwarning('提醒', '请正确填写包名')
            if int(click) + int(sliding) + int(track) + int(kboard) + int(main_nav) + int(base_nav) + int(syso) + int(acti) + int(others) > 100:
                messagebox.showerror('提醒', '您输入的所有的事件的比例和不能超过100%')
                LOG.info('您输入的所有的事件的比例和不能超过100')
            adb_monkey(pkname=packname, s_num=s, throttle=interval_times, pct_touch=click, pct_motion=sliding, pct_trackball=track, pct_nav=base_nav,
                       pct_majornav=main_nav, pct_syskeys=syso, pct_appswitch=acti, pct_flip=kboard, pct_anyevent=others, times=event_times, logfilepath=log)
        except:
            messagebox.showwarning('警告', '必须填写monkey相关数据')
            LOG.info('monkey 测试出错，原因:%s' % Exception)
    else:
        LOG.info('设备连接异常 请重新连接设备!')
        messagebox.showwarning('警告', '设备连接异常 请重新连接设备!')


def ScreenShot():
    '''截图'''
    name = 'ScreenShot_' + str(int(time.time()))
    os.system(r'adb shell screencap -p /sdcard/%s.png' % name)
    os.system(r'adb pull /sdcard/%s.png %s' % (name, ScreenShot_DIR))
    messagebox.showwarning('提示', "截图完成")


@logger('cpu占用率,上传下载流量，内存的测试')
def cpu_app():
    device_status = get_device_status()
    if device_status == 'device':
        perf_pkname = perform_pkname.get('0.0', END).split()[0]
        xing = xing_t.get()
        if len(perf_pkname) <= 5 or not perf_pkname.find("."):
            LOG.info('包名必须真实有效')
            messagebox.showwarning('警告', '请检查您的包名')
        times_list = []
        cpu_list = []
        rescv_list = []
        send_list = []
        total_list = []
        pass_list = []
        i = 0
        for i in range(int(xing)):
            nen_cun = get_mem(perf_pkname)
            rescv, send, netflow_sum = get_netflow(perf_pkname)
            cpu = get_cpu_data(perf_pkname)
            neicun_t['state'] = 'normal'
            pass_list.append(int(nen_cun)) # 保存数值
            neicun_t.insert(tkinter.END, ('Pass值：%s' % nen_cun))
            LOG.info('第%s次：Pass：%s' % (i, nen_cun))
            neicun_t.insert(tkinter.END, '\n')
            neicun_t.see(END)
            neicun_t['state'] = 'disabled'
            cpu_t['state'] = 'normal'
            cpu_list.append(float(cpu[:-1]))# 不带单位
            cpu_t.insert(tkinter.END, ('CPU占有率：%s' % cpu))
            LOG.info('第{}次：CPU占用率%：{}'.format(i, cpu))
            cpu_t.insert(tkinter.END, '\n')
            cpu_t.see(END)
            cpu_t['state'] = 'disabled'
            netflow_t['state'] = 'normal'
            total_list.append(int(netflow_sum))
            rescv_list.append(int(rescv))
            send_list.append(int(send))
            netflow_t.insert(
                tkinter.END, ('总流量：%sk,上传流量:%sk,下载流量：%sk' % (netflow_sum, rescv, send)))
            LOG.info('第%s次：总流量：%sk,上传流量:%sk,下载流量：%sk' %
                     (i, netflow_sum, rescv, send))
            netflow_t.insert(tkinter.END, '\n')
            netflow_t.see(END)
            netflow_t['state'] = 'disabled'
            perform_btn['state'] = 'disabled'
            i += 1
            times_list.append(int(i))
        get_cpu(times=times_list, start_cpu=cpu_list, recv_list=rescv_list,
                send_list=send_list, total_list=total_list, Pass_list=pass_list)
        perform_btn['state'] = 'normal'
        LOG.info('测试完成')
        messagebox.showinfo('提醒', '测试完毕，测试报告已经生成！')
    else:
        LOG.info('测试的设备必须正常连接，请注意')
        messagebox.showwarning('警告', '设备连接异常 请重新连接设备!')


@logger('采用线程来启动测试！采集cpu占用率,上传下载流量，内存')
def teread():  # 如果不是ui界面，可以不用线程
    for _ in range(1):
        t = threading.Thread(target=cpu_app, args=())
        t.start()


@logger('启动app时间线程测试')
def teread_start():  # 如果不用ui界面，可以不用线程
    for _ in range(1):
        t = threading.Thread(target=StartAPP, args=())
        t.start()


if __name__ == '__main__':
    LOG.info('测试小程序开始启动！测试开启！')
    try:
        status_shebei = get_device_status()
        if status_shebei == 'device':
            root = tkinter.Tk()
            root.title('安卓系统adb小工具')
            root.geometry("950x600")
            root.resizable(width=False, height=False)
            tkinter.Label(root, text='性能参数展示', fg='red', font=("黑体", 15, "bold"),).grid(
                row=1, column=3)
            cpu_t = tkinter.Text(root, height=5, width=30)
            cpu_t.grid(row=1, column=2)
            netflow_t = tkinter.Text(root, height=5, width=30)
            netflow_t.grid(row=1, column=4)
            netflow_t.see(END)
            neicun_t = tkinter.Text(root, height=5, width=30)
            neicun_t.grid(row=3, column=2)
            neicun_t.see(END)
            suji_ev = [50, 100, 150, 200, 300]  # 这里还原可以增加可以选择的次数
            xing_t = ttk.Combobox(root, values=suji_ev, width=5)
            xing_t.current(0)
            xing_t.grid(row=1, column=6)
            tkinter.Label(root, text='cpu:', justify=LEFT).grid(
                row=1, column=1)
            tkinter.Label(root, text='执行次数:', justify=LEFT).grid(
                row=1, column=5)
            tkinter.Label(root, text='流量:', justify=LEFT).grid(row=2, column=4)
            tkinter.Label(root, text='内存:', justify=LEFT).grid(row=3, column=1)
            tkinter.Label(root, text='性能测试包名:', justify=LEFT).grid(
                row=0, column=1)
            perform_pkname = tkinter.Text(root, height=1, width=30)
            perform_pkname.grid(row=0, column=2)
            perform_pkname.insert('0.0', "请输入被测APP应用的包名")
            perform_btn = tkinter.Button(
                root, text='执行性能测试', font=("黑体", 15, "bold"), command=teread)
            perform_btn.grid(row=0, column=3)
# 			tkinter.Label(root,text='启动时间测试',fg='red',height=2,font=("黑体", 15, "bold")).grid(row=8,column=3)
            tkinter.Label(root, text='启动测试包名:', justify=LEFT).grid(
                row=9, column=1)
            baoming_t = tkinter.Text(root, height=1, width=30)
            baoming_t.grid(row=9, column=2)
            baoming_t.insert('0.0', "请输入被测APP应用的包名")
            tkinter.Label(root, text='测试包Activity:', justify=LEFT).grid(
                row=9, column=3)
            activ_t = tkinter.Text(root, height=1, width=30)
            activ_t.grid(row=9, column=4)
            activ_t.insert('0.0', "请输入被测APP应用的主页面")
            tkinter.Label(root, text='执行次数:').grid(row=9, column=5)
            num = [10, 20, 30, 50, 100]
            # state='readonly',只读不可手输
            times_act = ttk.Combobox(root, values=num, width=5)
            times_act.current(0)
            times_act.grid(row=9, column=6)

            tkinter.Label(root, text='启动时间展示:', justify=LEFT).grid(
                row=10, column=1)
            e1 = tkinter.Text(root, width=30, height=5, state="disabled")
            e1.grid(row=10, column=2, padx=20, pady=30)

            screenshot_btn = tkinter.Button(root, text='截图', width=8, height=3, font=(
                "黑体", 16, "bold"), fg='red', command=ScreenShot)
            screenshot_btn.grid(row=10, column=4)

            btn_start = tkinter.Button(
                root, text='启动时间测试', font=("黑体", 15, "bold"), command=teread_start)
            btn_start.grid(row=8, column=3)
# 			tkinter.Label(root,text='Monkey测试',fg='red',font=("黑体", 15, "bold")).grid(row=11,column=4)
            tkinter.Label(root, text='Monkey测试包名:', justify=LEFT).grid(
                row=12, column=1)
            pkname = tkinter.Text(root, height=1, width=30)
            pkname.insert('0.0', '请输入被测APP应用的包名')
            pkname.grid(row=12, column=2)

            # 理解成次数
            tkinter.Label(root, text='执行次数:', justify=LEFT).grid(
                row=12, column=3)
            act_count = tkinter.Text(root, height=1, width=30)
            act_count.grid(row=12, column=4)
            act_count.insert('0.0', 5)

            tkinter.Label(root, text='时间间隔:', justify=LEFT).grid(
                row=12, column=5)
            random_event = [500, 1000, 1500, 2000, 3000]
            time_t = ttk.Combobox(root, values=random_event, width=5)
            time_t.current(0)
            time_t.grid(row=12, column=6)

            tkinter.Label(root, text='触发touch事件百分比:', justify=LEFT).grid(
                row=18, column=1)
            click_event = tkinter.Text(root, height=1, width=30)
            click_event.grid(row=18, column=2)
            click_event.insert('0.0', 15)

            tkinter.Label(root, text='手势motion事件百分比:', justify=LEFT).grid(
                row=15, column=1)
            sliding_event = tkinter.Text(root, height=1, width=30)
            sliding_event.grid(row=15, column=2)
            sliding_event.insert('0.0', 10)

            tkinter.Label(root, text='pinchzoom缩放事件百分比:', justify=LEFT).grid(
                row=16, column=3)
            zoom_event = tkinter.Text(root, height=1, width=30)
            zoom_event.grid(row=16, column=4)
            zoom_event.insert('0.0', 2)

            tkinter.Label(root, text='轨迹球事件百分比:', justify=LEFT).grid(
                row=14, column=3)
            track_event = tkinter.Text(root, height=1, width=30)
            track_event.grid(row=14, column=4)
            track_event.insert('0.0', 15)

            tkinter.Label(root, text='基本导航事件百分比:', justify=LEFT).grid(
                row=14, column=1)
            base_navigation_event = tkinter.Text(root, height=1, width=30)
            base_navigation_event.insert('0.0', 30)
            base_navigation_event.grid(row=14, column=2)

            tkinter.Label(root, text='主要导航事件百分比:', justify=LEFT).grid(
                row=13, column=1)
            main_navigation_event = tkinter.Text(root, height=1, width=30)
            main_navigation_event.insert('0.0', 15)
            main_navigation_event.grid(row=13, column=2)

            tkinter.Label(root, text='系统按键百分比:', justify=LEFT).grid(
                row=16, column=1)
            system_event = tkinter.Text(root, height=1, width=30)
            system_event.grid(row=16, column=2)
            system_event.insert('0.0', 2)

            tkinter.Label(root, text='Activity启动事件百分比:', justify=LEFT).grid(
                row=15, column=3)
            activity_switch_event = tkinter.Text(root, height=1, width=30)
            activity_switch_event.grid(row=15, column=4)
            activity_switch_event.insert('0.0', 2)

            tkinter.Label(root, text='键盘唤出隐藏事件百分比:', justify=LEFT).grid(
                row=13, column=3)
            keyboard_event = tkinter.Text(root, height=1, width=30)
            keyboard_event.grid(row=13, column=4)
            keyboard_event.insert('0.0', 1)

            tkinter.Label(root, text='其他事件百分比:', justify=LEFT).grid(
                row=17, column=3)
            other_event = tkinter.Text(root, height=1, width=30)
            other_event.grid(row=17, column=4)
            other_event.insert('0.0', 8)

            # 伪随机产生的种子数：默认5555
            tkinter.Label(root, text='伪随机数:').grid(row=17, column=1)
            pseudorandom = tkinter.Text(root, height=1, width=30)
            pseudorandom.insert('0.0', 5555)
            pseudorandom.grid(row=17, column=2)

            tkinter.Label(root, text='日志存放路径:', justify=LEFT).grid(
                row=18, column=3)
            log_path = tkinter.Text(root, height=1, width=30)
            log_path.grid(row=18, column=4)
            log_path.insert('0.0', os.path.join(BASEDIR[:3] ,'monekey.log'))
            btn_monkey = tkinter.Button(
                root, text='启动Monkey测试', font=("黑体", 15, "bold"), command=monkey_app)
            btn_monkey.grid(row=11, column=3)
            root.mainloop()
        else:
            LOG('设备未连接或者连接异常!目前连接状态:%s' % status_shebei)
    except Exception as e:
        LOG.error('测试异常，原因：%s' % e)
