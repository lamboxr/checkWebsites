import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import applicationContext
import checker
from Ui_MainWindow import Ui_MainWindow


# from test_ui import Ui_MainWindow


class SignalStore(QObject):
    append_log = pyqtSignal(str)


class MyThread(QThread):
    # 设置线程变量
    trigger = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def run_(self, message):
        '''
        向信号trigger发送消息
        '''
        self.trigger.emit(message)


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.thread_no = 0  # 序号
        self.setupUi(self)
        self.threads = MyThread(self)  # 自定义线程类
        self.threads.trigger.connect(self.update_text)  # 当信号接收到消息时，更新数据

        self.c = checker.Checker(self)

        self.button_start.clicked.connect(lambda checked: self.button_start_onClick())
        self.button_determine.clicked.connect(lambda checked: self.button_determine_onClick())
        self.so = SignalStore()
        self.so.append_log.connect(self.c.appendLog)  # TODO

    def button_start_onClick(self):
        '''
        当点击start按键时日志栏中应显示start:序号
        '''
        # self.thread_no += 1
        # message = "start:{0}".format(self.thread_no)
        applicationContext.is_running = True
        self.button_start.setDisabled(applicationContext.is_running)
        self.button_determine.setDisabled(not applicationContext.is_running)

        if not self.c.validate():
            self.warning_Label.setText("Server酱 KEY不能为空")
            applicationContext.is_running = False
            self.button_start.setDisabled(applicationContext.is_running)
            self.button_determine.setDisabled(not applicationContext.is_running)
            return
        else:
            self.warning_Label.setText("运行中...")
            self.switch_ftqq_ComboBox.setDisabled(True)
            if self.switch_ftqq_ComboBox.isChecked():
                self.ftqq_key_Edit.setReadOnly(applicationContext.is_running)
                self.ftqq_key_Edit.setDisabled(applicationContext.is_running)

        self.c.handle_check()
        # self.threads.run_(message)  # start the thread

    def button_determine_onClick(self):
        '''
        当点击stop按键时日志栏中应显示stop:序号
        '''
        if self.c.determine():
            self.button_start.setDisabled(applicationContext.is_running)
            self.button_determine.setDisabled(not applicationContext.is_running)
            self.switch_ftqq_ComboBox.setDisabled(applicationContext.is_running)
            self.warning_Label.setText('已停止')
            if self.switch_ftqq_ComboBox.isChecked():
                self.ftqq_key_Edit.setReadOnly(applicationContext.is_running)
                self.ftqq_key_Edit.setDisabled(applicationContext.is_running)

    def update_text(self, message):
        '''
        添加信息到日志栏中(即控件QTextBrowser中)
        '''
        self.log_Browser.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = Main()
    mainWindow.show()

    sys.exit(app.exec_())
