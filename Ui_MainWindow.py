from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QFont

import applicationContext


class Ui_MainWindow(object):

    def setupUi(self, mainWindow):
        self.font_label = QFont()
        self.font_label.setPointSize(10)

        mainWindow.resize(800, 720)
        mainWindow.setFixedSize(800, 720)
        self.central_widget = QtWidgets.QWidget(mainWindow)
        self.central_widget.setObjectName("central_widget")
        # mainWindow.move(300, 100)

        # self.notice_Label = QtWidgets.QLabel(self.central_widget)
        # self.notice_Label.setGeometry(QtCore.QRect(40, 25, 300, 40))
        # self.notice_Label.setFont(self.font_label)
        # self.notice_Label.setText('间隔%d秒检查一次网站' % applicationContext.cycle)
        self.label_cycle = QtWidgets.QLabel(self.central_widget)
        self.label_cycle.setGeometry(QtCore.QRect(40, 25, 100, 40))
        self.radio_cycle_quarter = QtWidgets.QRadioButton(self.central_widget)
        self.radio_cycle_quarter.setGeometry(QtCore.QRect(140, 25, 100, 40))
        self.radio_cycle_half_an_hour = QtWidgets.QRadioButton(self.central_widget)
        self.radio_cycle_half_an_hour.setGeometry(QtCore.QRect(240, 25, 100, 40))
        self.radio_cycle_one_hour = QtWidgets.QRadioButton(self.central_widget)
        self.radio_cycle_one_hour.setGeometry(QtCore.QRect(340, 25, 100, 40))
        self.radio_cycle_two_hour = QtWidgets.QRadioButton(self.central_widget)
        self.radio_cycle_two_hour.setGeometry(QtCore.QRect(440, 25, 100, 40))
        self.radio_cycle_two_hour.setChecked(True)

        self.label_timeout = QtWidgets.QLabel(self.central_widget)
        self.label_timeout.setGeometry((QtCore.QRect(40, 60, 100, 40)))
        self.spinBox_timeout = QtWidgets.QSpinBox(self.central_widget)
        self.spinBox_timeout.setGeometry((QtCore.QRect(140, 69, 75, 22)))
        self.spinBox_timeout.setAlignment(Qt.AlignRight)
        self.spinBox_timeout.setValue(30)
        self.spinBox_timeout.setMinimum(10)
        self.spinBox_timeout.setMaximum(60)
        self.label_timeout_range = QtWidgets.QLabel(self.central_widget)
        self.label_timeout_range.setGeometry((QtCore.QRect(225, 60, 100, 40)))

        self.log_Browser = QtWidgets.QTextBrowser(self.central_widget)
        self.log_Browser.setGeometry(QtCore.QRect(40, 115, 720, 425))
        self.log_Browser.setObjectName("log_Browser")

        self.label_warning = QtWidgets.QLabel(self.central_widget)
        self.label_warning.setGeometry(QtCore.QRect(40, 550, 200, 40))
        self.label_warning.setStyleSheet('font-size:20;color:red;')
        # self.label_warning.setFrameShape(QtWidgets.QFrame.Box)
        self.label_warning.setFont(self.font_label)
        # self.label_warning.setAlignment(Qt.AlignCenter)
        # self.label_warning.setText('Warning')

        self.comboBox_switch_ftqq = QtWidgets.QCheckBox(self.central_widget)
        self.comboBox_switch_ftqq.setGeometry(QtCore.QRect(40, 600, 180, 40))
        self.comboBox_switch_ftqq.setText('开启微信推送')

        # self.switch_ftqq_Label = QtWidgets.QLabel(self.central_widget)
        # self.switch_ftqq_Label.setGeometry(QtCore.QRect(60, 600, 120, 40))
        # self.switch_ftqq_Label.setFont(self.font_label)
        # self.switch_ftqq_Label.setText('开启微信推送')

        self.label_ftqq_key = QtWidgets.QLabel(self.central_widget)
        self.label_ftqq_key.setGeometry(QtCore.QRect(180, 600, 120, 40))
        self.label_ftqq_key.setFont(self.font_label)
        self.label_ftqq_key.setText('Server酱Key:')

        self.lineEdit_ftqq_key = QtWidgets.QLineEdit(self.central_widget)
        self.lineEdit_ftqq_key.setGeometry(QtCore.QRect(280, 605, 480, 28))
        self.lineEdit_ftqq_key.setPlaceholderText('请填入server酱服务的key')
        self.lineEdit_ftqq_key.setReadOnly(True)
        self.lineEdit_ftqq_key.setDisabled(True)

        self.button_init = QtWidgets.QPushButton(self.central_widget)
        self.button_init.setGeometry(QtCore.QRect(185, 660, 90, 28))
        self.button_init.setObjectName("button_init")

        self.button_start = QtWidgets.QPushButton(self.central_widget)
        self.button_start.setGeometry(QtCore.QRect(355, 660, 90, 28))
        self.button_start.setObjectName("button_start")

        self.button_determine = QtWidgets.QPushButton(self.central_widget)
        self.button_determine.setGeometry(QtCore.QRect(525, 660, 90, 28))
        self.button_determine.setObjectName("button_determine")
        self.button_determine.setDisabled(True)

        mainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 577, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("mainWindow", "网站首页检查器 v%s -- by %s" % (applicationContext.version, applicationContext.author)))
        self.button_init.setText(_translate("mainWindow", "生成模版"))
        self.button_start.setText(_translate("mainWindow", "启  动"))
        self.button_determine.setText(_translate("mainWindow", "停  止"))
        self.label_cycle.setText(_translate("mainWindow", "时间间隔:"))
        self.label_timeout.setText(_translate("mainWindow", "超时(秒):"))
        self.label_timeout_range.setText(_translate("mainWindow", "(10-60)"))

        self.radio_cycle_quarter.setText(_translate("mainWindow", "15分钟"))
        self.radio_cycle_half_an_hour.setText(_translate("mainWindow", "30分钟"))
        self.radio_cycle_one_hour.setText(_translate("mainWindow", "1小时"))
        self.radio_cycle_two_hour.setText(_translate("mainWindow", "2小时"))
