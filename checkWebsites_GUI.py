import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import applicationContext
import checker
from Ui_MainWindow import Ui_MainWindow


# from test_ui import Ui_MainWindow


class SignalStoreLogBrowser(QObject):
    append_log = pyqtSignal(str)


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        self.log_idx = 0
        self.cycle = 2 * 60 * 60
        self.setupUi(self)
        self.radio_cycle_quarter.toggled.connect(lambda checked: self.radio_button_toggled(15))
        self.radio_cycle_half_an_hour.toggled.connect(lambda checked: self.radio_button_toggled(30))
        self.radio_cycle_one_hour.toggled.connect(lambda checked: self.radio_button_toggled(60))
        self.radio_cycle_two_hour.toggled.connect(lambda checked: self.radio_button_toggled(60 * 2))

        self.button_start.clicked.connect(self.button_start_onClick)
        self.button_determine.clicked.connect(self.button_determine_onClick)
        self.ssLogBrowser = SignalStoreLogBrowser()
        self.ssLogBrowser.append_log.connect(checker.appendLog)
        self.comboBox_switch_ftqq.stateChanged.connect(self.switch_ftqq_ComboBox_onchange)
        checker.ui = self

    def button_start_onClick(self):
        '''
        当点击start按键时日志栏中应显示start:序号
        '''
        # self.thread_no += 1
        # message = "start:{0}".format(self.thread_no)
        applicationContext.is_running = True
        self.setWidgetStyle()

        if not checker.validate():
            self.label_warning.setText("Server酱 KEY不能为空")
            applicationContext.is_running = False
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
            self.setWidgetStyle()

    def update_text(self, message):
        '''
        添加信息到日志栏中(即控件QTextBrowser中)
        '''
        self.log_Browser.append(message)

    def radio_button_toggled(self, cycle):
        self.cycle = cycle * 60

    def setWidgetStyle(self):
        self.radio_cycle_quarter.setEnabled(not applicationContext.is_running)
        self.radio_cycle_half_an_hour.setEnabled(not applicationContext.is_running)
        self.radio_cycle_one_hour.setEnabled(not applicationContext.is_running)
        self.radio_cycle_two_hour.setEnabled(not applicationContext.is_running)
        self.comboBox_switch_ftqq.setEnabled(not applicationContext.is_running)
        self.lineEdit_ftqq_key.setEnabled(not applicationContext.is_running and self.comboBox_switch_ftqq.isChecked())
        self.button_start.setEnabled(not applicationContext.is_running)
        self.button_determine.setEnabled(applicationContext.is_running)


    def switch_ftqq_ComboBox_onchange(self, state):
        self.lineEdit_ftqq_key.setDisabled(state == 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = Main()
    mainWindow.show()

    sys.exit(app.exec_())
