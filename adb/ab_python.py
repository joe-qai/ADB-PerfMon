# -*- coding: utf-8 -*-
import os,subprocess
from adb.checkpath import get_sys_env
from tools.HandleLogging import logger

find=get_sys_env()

"""
python调用adb系统命令测试Android应用
"""
@logger('获取启动耗时')
def starttime_app(packagename,packagenameactivicy):#启动耗时
	# 强制退出
	cmd2='adb shell am force-stop %s'%packagename
	os.system(cmd2)
	# 启动app
	cmd='adb shell am start -W -n %s/%s'%(packagename,packagenameactivicy) 	
	me=os.popen(cmd).read().split('\n')[-4].split(':')#获取启动时间
	# 强制退出
	cmd2='adb shell am force-stop %s'%packagename
	os.system(cmd2)
	return me


@logger('获取流量')
def get_netflow(packagename):
	cmd = 'adb shell dumpsys package  "%s" | find "userId"'%(packagename)
	cm=os.popen(cmd).read().split('=')[1].strip()
	cmd1='adb shell cat /proc/net/xt_qtaguid/stats | %s %s'%(find,cm)
	me1_shou=os.popen(cmd1).read().split()[5]#接收
	me2_shou=os.popen(cmd1).read().split()[7]#上传
	cmd2='adb shell cat /proc/net/xt_qtaguid/stats | %s %s'%(find,cm)
	me1_xia=os.popen(cmd2).read().split()[5]#接收
	me2_xia=os.popen(cmd2).read().split()[7]#上传
	netflow_sum_1=(int(me1_shou)+int(me2_shou))#过程产生流量计算为执行后的流量-执行前的流量，
	netflow_sum_xia=(int(me1_xia)+int(me2_xia))
	netflow_sum=int(netflow_sum_xia)-int(netflow_sum_1)
	me1=int(me1_xia)-int(me1_shou)
	me2=int(me2_xia)-int(me2_shou)
	return me1 ,me2,netflow_sum


@logger('获取cpu信息')
def get_cpu_data(packagename):#这里采集的cpu时候可以是执行操作采集 就是-n  -d  刷新间隔
	cpu='adb shell top -n 1 | %s "%s"'%(find,packagename[:15])
	# print(os.popen(cpu).read())
	re_cpu=os.popen(cpu).read().split()[4]
	return re_cpu


@logger('获取内存')
def get_mem(packagename):#Total 的实际使用过物理内存
	cpu = 'adb shell top -n 1| %s "%s"' % (find, packagename[:15])
	re_cpu=os.popen(cpu).read().split()[8]
	return re_cpu


@logger('执行monkey测试')
def adb_monkey(pkname,s_num,throttle,pct_touch ,pct_motion,pct_trackball,pct_nav,pct_majornav,pct_syskeys,pct_appswitch,pct_flip,pct_anyevent,times,logfilepath):
	"""adb shell monkey -p {0} -s {1} --throttle {2} --pct-touch {3} --pct-motion {4} --pct-trackball  {5}  --pct-nav {6}  
	--pct-majornav {7} --pct-syskeys {8} --pct-appswitch {9}  --pct-flip  {10}  --pct-anyevent {11} -v -v -v {12} >{13}"""
	cmden='adb shell monkey -p {0} -s {1} --throttle {2} --pct-touch {3} --pct-motion {4} --pct-trackball  {5}  --pct-nav {6} --pct-majornav {7} --pct-syskeys {8} --pct-appswitch {9}  --pct-flip  {10}  --pct-anyevent {11} -v -v -v {12} >{13}'.format(pkname,s_num,throttle,pct_touch ,pct_motion,pct_trackball,pct_nav,pct_majornav,pct_syskeys,pct_appswitch,pct_flip,pct_anyevent,times,logfilepath)
	os.popen(cmden)


@logger('获取设备状态')
def get_device_status():#获取设备状态
	cmd1='adb get-state'
	devices_status=os.popen(cmd1).read().split()[0]
	return devices_status


def app_force_stop(package_name):
	cmd = 'adb shell dumpsys package  "{}" | findstr "userId"'.format(package_name)
	cm=os.popen(cmd).read().split('=')[1].strip()
	try:
		subprocess.call('adb -s %s shell am force-stop %s' % (cm, package_name), shell=True)
	except:
		pass


def get_netflow1(package):
	'''获取的是总数'''
	cmd = 'adb shell dumpsys package  "%s" | findstr "userId"'%(package)
	uid=os.popen(cmd).read().split('=')[1].strip()
	#下载流量
	c ='adb shell cat proc/uid_stat/%s/tcp_rcv'%uid
	p1 = subprocess.Popen(c,stdout=subprocess.PIPE,stderr=subprocess.PIPE)#用adb获取信息uid
	flo_rec =int(p1.stdout.read())
	#获取上传流量
	p1 = subprocess.Popen('adb shell cat proc/uid_stat/%s/tcp_snd'%uid,
	stdout=subprocess.PIPE,stderr=subprocess.PIPE)#用adb获取信息
	flo_snd =int(p1.stdout.read())
	return flo_snd,flo_rec