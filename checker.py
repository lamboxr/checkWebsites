# -*- coding:utf-8 -*-

import os.path
import pathlib
import sys
import time
# from concurrent.futures import wait, ALL_COMPLETED, FIRST_COMPLETED

import click
import requests
import schedule
from PyQt5.QtWidgets import QApplication
from schedule import every, repeat, run_pending
from timeloop import Timeloop

import checkWebsites_GUI
import LoggerFactory
import applicationContext
import file_util

# from t.BoundedThreadPoolExecutor import BoundedThreadPoolExecutor

logger = LoggerFactory.getLogger(__name__)


class Checker:
    def __init__(self, ui):
        self.ui = ui
        # self.isPush = ui.isPush
        # self.ftqq_key = ui.ftqq_key
        self.threads = ui.threads
        self.thread_no = ui.thread_no
        self._root, self._name = os.path.split(os.path.abspath(sys.argv[0]))
        self.job = None

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

    def _init(self):
        pathlib.Path(os.path.join(self._root, applicationContext.template_dir)).mkdir(parents=True, exist_ok=True)
        for key, value in applicationContext.urls.items():
            resp = requests.get(value)
            if resp.status_code == 200:
                html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
                with open(os.path.join(self._root, applicationContext.template_dir, key), 'w',
                          encoding='utf-8') as file_object:
                    file_object.write(html)
                self.info('保存网页完毕%s' % value)

        for key, value in applicationContext.login_pages.items():
            resp = requests.get(value)
            # if resp.status_code == 200:
            html = resp.text.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '')
            with open(os.path.join(self._root, applicationContext.template_dir, key), 'w',
                      encoding='utf-8') as file_object:
                file_object.write(html)
            self.info('保存网页完毕%s' % value)
        # else:
        #     print(value + " : " + str(resp.status_code))
        #     print(resp.text)

    def validate(self):
        if self.ui.switch_ftqq_ComboBox.isChecked():
            if len(self.ui.ftqq_key_Edit.text()) == 0:
                return False
        return True

    # @cli.command(name="check")
    def start_check(self):
        """ 启动检查程序 """
        self.info('')
        self.info('""" 启动检查程序 """')
        self.info('')
        if self.ui.switch_ftqq_ComboBox.isChecked():
            self.info('微信推送: 开启')
        else:
            self.info('微信推送: 未开启')

        # with BoundedThreadPoolExecutor(max_workers=1) as t:
        #     all_tasks = [t.submit(self._check_in_t)]
        #     wait(all_tasks, return_when=FIRST_COMPLETED)
        self._check()
        self.job = schedule.every(applicationContext.cycle).seconds.do(self._check)
        while True:
            run_pending()
            time.sleep(1)

    def determine(self):
        sys.exit(app.exec_())
        schedule.clear(self.job)
        self.job = None
        self.info('')
        self.info('""" 停止检查程序 """')
        applicationContext.is_running = False
        return True

    # @repeat(every(cycle).seconds)
    def _check(self):
        start_time = time.time()
        msg = '\n检查结果：\n\n'

        check_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.info("开始本次检查，检查时间%s" % check_time)
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
                    self.error(line_msg.replace('WARNING!', '<font style="color:blue">WARNING!</font>'))
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
                self.error(line_msg.replace('WARNING!', '<font style="color:blue">WARNING!</font>'))
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
        self.info('等待下一次检查... 预计下次检查时间 %s' % time.strftime('%Y-%m-%d %H:%M:%S',
                                                           time.localtime(time.time() + applicationContext.cycle)))

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
        self.ui.log_Browser.append('%d: %s' % (self.thread_no, msg))  # labelruning可以是文本部件或标签部件
        QApplication.processEvents()  # 实时刷新界面

# if __name__ == '__main__':
#     cli()
