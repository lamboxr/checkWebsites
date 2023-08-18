import sys

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import applicationContext
import checker
from Ui_MainWindow import Ui_MainWindow


# from test_ui import Ui_MainWindow


class SignalStoreLogBrowser(QObject):
    append_log = pyqtSignal(str)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.log_idx = 0
        self.cycle = 2 * 60 * 60
        self.setupUi(self)
        self.radio_cycle_quarter.toggled.connect(lambda checked: self.radio_button_toggled(15))
        self.radio_cycle_half_an_hour.toggled.connect(lambda checked: self.radio_button_toggled(30))
        self.radio_cycle_one_hour.toggled.connect(lambda checked: self.radio_button_toggled(60))
        self.radio_cycle_two_hour.toggled.connect(lambda checked: self.radio_button_toggled(60 * 2))

        self.button_init.clicked.connect(self.button_init_onClick)
        self.button_start.clicked.connect(self.button_start_onClick)
        self.button_determine.clicked.connect(self.button_determine_onClick)
        self.ssLogBrowser = SignalStoreLogBrowser()
        self.ssLogBrowser.append_log.connect(checker.appendLog)
        self.comboBox_switch_ftqq.stateChanged.connect(self.switch_ftqq_ComboBox_onchange)
        checker.ui = self

    def button_init_onClick(self):
        checker.is_checking = True
        self.setWidgetStyle()
        self.button_determine.setDisabled(True)
        reply = QMessageBox.question(self, 'Message', '请确认网站均可访问后再生成模版，是否继续?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if checker.templates_exist():
                reply2 = QMessageBox.question(self, 'Message', '模版已存在，是否重新生成?', QMessageBox.Yes | QMessageBox.No)

                if reply2 == QMessageBox.Yes:
                    checker.handle_generate_templates()
            else:
                checker.handle_generate_templates()

    def button_start_onClick(self):
        '''
        当点击start按键时日志栏中应显示start:序号
        '''
        # self.thread_no += 1
        # message = "start:{0}".format(self.thread_no)
        applicationContext.is_checking = True
        self.setWidgetStyle()

        if not checker.validate():
            self.label_warning.setText("Server酱 KEY不能为空")
            applicationContext.is_checking = False
            self.setWidgetStyle()
            return
        else:
            self.label_warning.setText("运行中...")
            self.setWidgetStyle()

        checker.handle_check()
        # self.threads.run_(message)  # start the thread

    def button_determine_onClick(self):
        '''
        当点击stop按键时日志栏中应显示stop:序号
        '''
        if checker.determine():
            self.label_warning.setText('已停止')
            applicationContext.is_checking = False
            self.setWidgetStyle()

    def update_text(self, message):
        '''
        添加信息到日志栏中(即控件QTextBrowser中)
        '''
        self.log_Browser.append(message)

    def radio_button_toggled(self, cycle):
        self.cycle = cycle * 60

    def setWidgetStyle(self):
        self.radio_cycle_quarter.setEnabled(not applicationContext.is_checking)
        self.radio_cycle_half_an_hour.setEnabled(not applicationContext.is_checking)
        self.radio_cycle_one_hour.setEnabled(not applicationContext.is_checking)
        self.radio_cycle_two_hour.setEnabled(not applicationContext.is_checking)
        self.spinBox_timeout.setEnabled(not applicationContext.is_checking)
        self.comboBox_switch_ftqq.setEnabled(not applicationContext.is_checking)
        self.lineEdit_ftqq_key.setEnabled(not applicationContext.is_checking and self.comboBox_switch_ftqq.isChecked())
        self.button_init.setEnabled(not applicationContext.is_checking)
        self.button_start.setEnabled(not applicationContext.is_checking)
        self.button_determine.setEnabled(applicationContext.is_checking)

    def switch_ftqq_ComboBox_onchange(self, state):
        self.lineEdit_ftqq_key.setDisabled(state == 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
