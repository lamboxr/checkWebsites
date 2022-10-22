# -*- coding:utf-8 -*-

import os.path
import pathlib
import shutil
import sys
import time
# from concurrent.futures import wait, ALL_COMPLETED, FIRST_COMPLETED
from threading import Thread

import requests
from PyQt5.QtWidgets import QApplication
from apscheduler.schedulers.blocking import BlockingScheduler

import LoggerFactory
import applicationContext
import file_util

logger = LoggerFactory.getLogger(__name__)
_root, _name = os.path.split(os.path.abspath(sys.argv[0]))
templates_path = os.path.join(_root, applicationContext.template_dir)
templates_bak_path = os.path.join(_root, applicationContext.template_bak_dir)
ui = None


def templates_exist():
    pathlib.Path(templates_path).mkdir(parents=True, exist_ok=True)
    return len(os.listdir(templates_path))


def handle_generate_templates():
    def generate_templates_sub_thread(ui, _root):
        pathlib.Path(templates_path).mkdir(parents=True, exist_ok=True)
        if len(os.listdir(templates_path)):
            info('')
            info('""" 正在备份模版... """')
            info('')
            if os.path.exists(templates_bak_path):
                shutil.rmtree(templates_bak_path)
            shutil.move(templates_path, templates_bak_path)
            shutil.rmtree(templates_path, templates_bak_path)
            os.makedirs(templates_path)

        info('""" 正在生成模版... """')
        info('')

        for key, value in applicationContext.urls.items():
            resp = requests.get(value)
            if resp.status_code == 200:
                html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
                with open(os.path.join(templates_path, key), 'w',
                          encoding='utf-8') as file_object:
                    file_object.write(html)

        for key, value in applicationContext.login_pages.items():
            resp = requests.get(value)
            # if resp.status_code == 200:
            html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
            with open(os.path.join(templates_path, key), 'w',
                      encoding='utf-8') as file_object:
                file_object.write(html)

        info('""" 模版生成完毕 """')
        info('')
        applicationContext.is_checking = False
        ui.setWidgetStyle()

        # if job is None:
        #     job = schedule.every(applicationContext.cycle).seconds.do(check_job)
        # while True:
        #     run_pending()
        #     time.sleep(1)

    worker = Thread(target=generate_templates_sub_thread, kwargs={'ui': ui, '_root': _root})
    worker.start()


def check_once():
    start_time = time.time()
    msg = '\n检查结果：\n\n'

    check_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))
    info("开始新一轮，检查时间%s" % check_time_str)
    info('')
    info("检查首页")

    for key, value in applicationContext.urls.items():
        _txt = file_util.read_file(os.path.join(applicationContext.template_dir, key))
        resp = requests.get(value)
        if resp.status_code == 200:
            html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
            if not html == _txt:
                # print("error: " + key + " - " + value)
                line_msg = '%s : WARNING!' % value
                error(line_msg.replace('WARNING!', '<font style="color:red">WARNING!</font>'))
                msg += line_msg + '\n'
            else:
                line_msg = '%s : ok' % (value)
                info(line_msg.replace('ok', '<font style="color:blue">ok</font>'))
                msg += line_msg + '\n'

    msg += '\n\n'
    info('')
    info("检查登录页")
    for key, value in applicationContext.login_pages.items():
        _txt = file_util.read_file(os.path.join(applicationContext.template_dir, key))
        resp = requests.get(value)
        # if resp.status_code == 200:
        html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
        if not html == _txt:
            # print("error: " + key + " - " + value)
            line_msg = '%s : WARNING!' % value
            error(line_msg.replace('WARNING!', '<font style="color:red">WARNING!</font>'))
            msg += line_msg + '\n'
        else:
            line_msg = '%s : ok' % (value)
            info(line_msg.replace('ok', '<font style="color:blue">ok</font>'))
            msg += line_msg + '\n'

    if ui.comboBox_switch_ftqq.isChecked():
        ftqq_push(ui.lineEidt_ftqq_key.text(), check_time_str, msg)

    end_time = time.time()
    info('')
    info('本次检查结束，耗时：%f秒' % (end_time - start_time))
    info('')
    if applicationContext.is_checking:
        info('预计下次检查时间 %s, 请耐心等待...' % time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(start_time + ui.cycle)))
    else:
        info('侦测到检查被用户终止,再次启动将继续检查...')
        info('')


def check_job():
    check_once()


"""验证send_key是否为空"""


def validate():
    return not (ui.comboBox_switch_ftqq.isChecked() and len(ui.lineEdit_ftqq_key.text().strip()) == 0)


# @cli.command(name="check")
def handle_check():
    def check_sub_thread():
        """ 启动检查程序 """
        info('')
        info('""" 启动检查程序 """')
        info('')
        info('微信推送: 开启' if ui.comboBox_switch_ftqq.isChecked() else '微信推送: 未开启')
        info('')
        sched.remove_all_jobs()
        sched.add_job(check_job, 'interval', seconds=ui.cycle, id='check_job_id')

        if not sched.running:  # 未运行
            info('开启检查定时任务...')
            info('')
            check_job()
            sched.start()

        elif sched.state == 2:
            info('恢复检查定时任务...')
            info('')
            check_job()
            sched.resume()

        # if job is None:
        #     job = schedule.every(applicationContext.cycle).seconds.do(check_job)
        # while True:
        #     run_pending()
        #     time.sleep(1)

    worker = Thread(target=check_sub_thread)
    worker.start()


def determine():
    # schedule.cancel_job(self.job)

    # schedule.clear(self.job)

    if applicationContext.is_checking:
        if sched.state == 1:
            sched.pause()
        info('')
        info('""" 检查被用户手动终止 """')
        return True


def ftqq_push(send_key, check_time, msg):
    api = 'https://sctapi.ftqq.com/%s.send' % send_key

    title = '网站检查时间 %s' % check_time
    data = {'title': title, 'desp': msg}
    r = requests.post(api, data)
    info("推送结果：%s" % r.text.encode().decode("unicode_escape"))


def info(msg):
    if len(msg) > 0:
        logger.info(msg)
    appendToLogBrowser(msg)


def debug(msg):
    if len(msg) > 0:
        logger.debug(msg)
    appendToLogBrowser(msg)


def error(msg):
    if len(msg) > 0:
        logger.error(msg)
    appendToLogBrowser('<font style="color:red">%s</font>' % msg)


def warn(msg):
    if len(msg) > 0:
        logger.warn(msg)
    appendToLogBrowser(msg)


def appendToLogBrowser(msg):
    ui.log_idx += 1
    ui.ssLogBrowser.append_log.emit('%d: %s' % (ui.log_idx, msg))
    # self.ui.log_Browser.append()  # labelruning可以是文本部件或标签部件
    QApplication.processEvents()  # 实时刷新界面


# 处理进度的slot函数
def appendLog(log):
    ui.log_Browser.append(log)


sched = BlockingScheduler()
