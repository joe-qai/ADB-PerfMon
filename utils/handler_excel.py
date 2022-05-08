# -*- coding: utf-8 -*-

import os

import xlsxwriter

from adb.configpath import REPORTDIR
from utils.logger import logger, LOG


__author__ = "joe-tester"

        
@logger('save time of start app')
def start_app(times, start):
    try:
        workbook = xlsxwriter.Workbook(os.path.join(REPORTDIR , '/app_start_time.xlsx'))
        worksheet = workbook.add_worksheet('time')
        bold = workbook.add_format({'bold': 1})
        headings = ['启动次数', '启动时间']
        data = [times, start]
        worksheet.write_row('A1', headings, bold)
        worksheet.write_column('A2', data[0])
        worksheet.write_column('B2', data[1])
        chart1 = workbook.add_chart({'type': 'scatter',
                                     'subtype': 'straight_with_markers'})
        chart1.add_series({
            'name': '=time!$B$1',
            'categories': '=time!$A$2:$A$%s' % (len(start) + 1),
            'values': '=time!$B$2:$B$%s' % (len(start) + 1),
        })
        chart1.set_title({'name': '启动监测'})
        chart1.set_x_axis({'name': "启动次数"})
        chart1.set_y_axis({'name': '花费时间:ms'})
        chart1.set_style(11)
        worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
        workbook.close()
        LOG.info('save success!!!')
    except:
        LOG.info('save failed，because is: %s' % Exception)


@logger('save cpuinfo meminfo netflow_info')
def get_cpu(times, start_cpu, recv_list, send_list, total_list, Pass_list):
    try:
        workbook = xlsxwriter.Workbook(os.path.join(REPORTDIR , 'cpu_netflow_men_report.xlsx'))
        worksheet = workbook.add_worksheet('cpu')
        worksheet_netflow = workbook.add_worksheet('netflow')
        worksheet_men = workbook.add_worksheet('men')
        bold = workbook.add_format({'bold': 1})
        headings = ['监控次数', 'cpu占用率(单位:G)']
        headings_netflow = ['监控次数', '上行流量', '下行流量', '流量总计']
        headings_men = ['监控次数', 'Pass占百分比']
        data_cpu = [times, start_cpu]
        data_netflow = [times, recv_list, send_list, total_list]
        data_men = [times, Pass_list]
        # write netflow to excel
        worksheet_netflow.write_row('A1', headings_netflow, bold)
        worksheet_netflow.write_column('A2', data_netflow[0])
        worksheet_netflow.write_column('B2', data_netflow[2])
        worksheet_netflow.write_column('C2', data_netflow[1])
        worksheet_netflow.write_column('D2', data_netflow[3])
        # write meminfo to excel
        worksheet_men.write_row('A1', headings_men, bold)
        worksheet_men.write_column('A2', data_men[0])
        worksheet_men.write_column('B2', data_men[1])
        # write cpuinfo to excel
        worksheet.write_row('A1', headings, bold)
        worksheet.write_column('A2', data_cpu[0])
        worksheet.write_column('B2', data_cpu[1])
        # Generate 2D map
        chart1 = workbook.add_chart({'type': 'scatter',
                                     'subtype': 'straight_with_markers'})
        chart2 = workbook.add_chart({'type': 'scatter',
                                     'subtype': 'straight_with_markers'})
        chart3 = workbook.add_chart({'type': 'scatter',
                                     'subtype': 'straight_with_markers'})
        chart3.add_series({
            'name': '=men!$B$1',
            'categories': '=men!$A$2:$A$%s' % (len(times) + 1),
            'values': '=men!$B$2:$B$%s' % (len(times) + 1),
        })
        chart2.add_series({
            'name': '=netflow!$B$1',
            'categories': '=netflow!$A$2:$A$%s' % (len(times) + 1),
            'values': '=netflow!$B$2:$B$%s' % (len(times) + 1),

        })
        chart1.add_series({
            'name': '=cpu!$B$1',
            'categories': '=cpu!$A$2:$A$%s' % (len(times) + 1),
            'values': '=cpu!$B$2:$B$%s' % (len(times) + 1),
        })
        chart2.add_series({
            'name': '=netflow!$C$1',    # netflow
            'categories': '=netflow!$A$2:$A$%s' % (len(times)),
            'values': '=netflow!$C$2:$C$%s' % (len(times)),
        })
        chart2.add_series({
            'name': '=netflow!$D$1',
            'categories': '=netflow!$A$2:$A$%s' % (len(times)),
            'values': '=netflow!$D$2:$D$%s' % (len(times)),
        })
        chart2.set_title({'name': '流量统计图'})
        chart2.set_x_axis({'name': '次数'})
        chart2.set_y_axis({'name': '流量：k'})
        chart2.set_style(11)
        chart3.set_title({'name': '内存占有率统计图'})
        chart3.set_x_axis({'name': '次数'})
        chart3.set_y_axis({'name': 'pass值：k'})
        chart3.set_style(11)
        worksheet_men.insert_chart(
            'F2', chart3, {'x_offset': 60, 'y_offset': 60})
        worksheet_netflow.insert_chart(
            'F2', chart2, {'x_offset': 60, 'y_offset': 60})
        chart1.set_title({'name': 'cpu占用率'})
        chart1.set_x_axis({'name': "次数"})
        chart1.set_y_axis({'name': '占用:%'})
        chart1.set_style(11)
        worksheet.insert_chart('D2', chart1, {'x_offset': 60, 'y_offset': 60})
        workbook.close()
        LOG.info('Successfully saved collected data')
    except:
        LOG.info('Failed to save collected data: %s' % Exception)