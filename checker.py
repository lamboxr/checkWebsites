# -*- coding:utf-8 -*-

import os.path
import pathlib
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


def generate_templates():
    _root, _name = os.path.split(os.path.abspath(sys.argv[0]))
    pathlib.Path(os.path.join(_root, applicationContext.template_dir)).mkdir(parents=True, exist_ok=True)
    for key, value in applicationContext.urls.items():
        resp = requests.get(value)
        if resp.status_code == 200:
            html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
            with open(os.path.join(_root, applicationContext.template_dir, key), 'w',
                      encoding='utf-8') as file_object:
                file_object.write(html)

    for key, value in applicationContext.login_pages.items():
        resp = requests.get(value)
        # if resp.status_code == 200:
        html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
        with open(os.path.join(_root, applicationContext.template_dir, key), 'w',
                  encoding='utf-8') as file_object:
            file_object.write(html)
    # else:
    #     print(value + " : " + str(resp.status_code))
    #     print(resp.text)


class Checker:
    def __init__(self, ui):
        self.ui = ui
        # self.isPush = ui.isPush
        # self.ftqq_key = ui.ftqq_key
        self.threads = ui.threads
        self.thread_no = ui.thread_no
        self._root, self._name = os.path.split(os.path.abspath(sys.argv[0]))
        # self.job = schedule.every(applicationContext.cycle).seconds.do(self.check_job)
        self.sched = BlockingScheduler()
        self.sched.add_job(self.check_job, 'interval', seconds=applicationContext.cycle, id='check_job_id')

    # CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

    # @click.group(context_settings=CONTEXT_SETTINGS)
    # def cli():
    #     """ProxyPool cli工具"""

    # @cli.command(name="init")
    # def init():
    #     """ 启动初始化程序 """
    #     logger.info('""" 启动初始化程序 """')
    #     _init()
    #     logger.info('""" 初始化完成 """')


    def validate(self):
        if self.ui.switch_ftqq_ComboBox.isChecked():
            if len(self.ui.ftqq_key_Edit.text()) == 0:
                return False
        return True

    # @cli.command(name="check")
    def handle_check(self):

        def start_check():
            """ 启动检查程序 """
            self.info('')
            self.info('""" 启动检查程序 """')
            self.info('')
            if self.ui.switch_ftqq_ComboBox.isChecked():
                self.info('微信推送: 开启')
            else:
                self.info('微信推送: 未开启')
            self.info('')

            # with BoundedThreadPoolExecutor(max_workers=1) as t:
            #     all_tasks = [t.submit(self._check_in_t)]
            #     wait(all_tasks, return_when=FIRST_COMPLETED)

            if not self.sched.running:  # 未运行
                self.info('开启检查定时任务...')
                self.info('')
                self.check_job()
                self.sched.start()
                self.sched.n

            elif self.sched.state == 2:
                self.info('恢复检查定时任务...')
                self.info('')
                self.check_job()
                self.sched.resume()

            # if self.job is None:
            #     self.job = schedule.every(applicationContext.cycle).seconds.do(self.check_job)
            # while True:
            #     run_pending()
            #     time.sleep(1)

        worker = Thread(target=start_check)
        worker.start()

    def determine(self):
        # schedule.cancel_job(self.job)

        # schedule.clear(self.job)
        if self.sched.state == 1:
            self.sched.pause()
        self.info('')
        self.info('""" 检查被用户手动终止 """')
        applicationContext.is_running = False
        return True

    # @repeat(every(cycle).seconds)
    def check_job(self):
        start_time = time.time()
        msg = '\n检查结果：\n\n'

        check_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.info("开始新一轮，检查时间%s" % check_time)
        self.info('')
        self.info("检查首页")

        for key, value in applicationContext.urls.items():
            _txt = file_util.read_file(os.path.join(applicationContext.template_dir, key))
            resp = requests.get(value)
            if resp.status_code == 200:
                html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
                if not html == _txt:
                    # print("error: " + key + " - " + value)
                    line_msg = '%s : WARNING!' % value
                    self.error(line_msg.replace('WARNING!', '<font style="color:red">WARNING!</font>'))
                    msg += line_msg + '\n'
                else:
                    line_msg = '%s : ok' % (value)
                    self.info(line_msg.replace('ok', '<font style="color:blue">ok</font>'))
                    msg += line_msg + '\n'

        msg += '\n\n'
        self.info('')
        self.info("检查登录页")
        for key, value in applicationContext.login_pages.items():
            _txt = file_util.read_file(os.path.join(applicationContext.template_dir, key))
            resp = requests.get(value)
            # if resp.status_code == 200:
            html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
            if not html == _txt:
                # print("error: " + key + " - " + value)
                line_msg = '%s : WARNING!' % value
                self.error(line_msg.replace('WARNING!', '<font style="color:red">WARNING!</font>'))
                msg += line_msg + '\n'
            else:
                line_msg = '%s : ok' % (value)
                self.info(line_msg.replace('ok', '<font style="color:blue">ok</font>'))
                msg += line_msg + '\n'

        # printLog(threads, msg)
        if self.ui.switch_ftqq_ComboBox.isChecked():
            self.ftqq_push(check_time, msg)
        # _root, filename = os.path.split(os.path.abspath(sys.argv[0]))
        # ftqq_key_file = os.path.join(_root, 'ftqq_key')
        # ftqq_key = file_util.read_file(ftqq_key_file)

        # printLog(threads, ftqq_key)
        end_time = time.time()
        self.info('')
        self.info('本次检查结束，耗时：%f秒' % (end_time - start_time))
        self.info('')
        if applicationContext.is_running:
            self.info('预计下次检查时间 %s, 请耐心等待...' % time.strftime('%Y-%m-%d %H:%M:%S',
                                                              time.localtime(time.time() + applicationContext.cycle)))
        else:
            self.info('侦测到检查被用户终止,再次启动将继续检查...')
            self.info('')

    def ftqq_push(self, check_time, msg):
        api = 'https://sctapi.ftqq.com/%s.send' % self.ui.ftqq_key_Edit.text()

        title = '网站检查时间 %s' % check_time
        data = {'title': title, 'desp': msg}
        r = requests.post(api, data)
        self.info("推送结果：%s" % r.text.encode().decode("unicode_escape"))

    def info(self, msg):
        if len(msg) > 0:
            logger.info(msg)
        self.appendToLogBrowser(msg)

    def debug(self, msg):
        if len(msg) > 0:
            logger.debug(msg)
        self.appendToLogBrowser(msg)

    def error(self, msg):
        if len(msg) > 0:
            logger.error(msg)
        self.appendToLogBrowser('<font style="color:red">%s</font>' % msg)

    def warn(self, msg):
        if len(msg) > 0:
            logger.warn(msg)
        self.appendToLogBrowser(msg)

    def appendToLogBrowser(self, msg):
        self.thread_no += 1
        self.ui.so.append_log.emit('%d: %s' % (self.thread_no, msg))
        # self.ui.log_Browser.append()  # labelruning可以是文本部件或标签部件
        QApplication.processEvents()  # 实时刷新界面

    # 处理进度的slot函数
    def appendLog(self, log):
        self.ui.log_Browser.append(log)

if __name__ == '__main__':
    generate_templates()
