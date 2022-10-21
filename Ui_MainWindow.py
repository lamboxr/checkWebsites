from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import applicationContext


class Ui_MainWindow(object):

    def setupUi_(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(577, 555)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 361, 491))
        self.textBrowser.setObjectName("textBrowser")
        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(430, 40, 93, 28))
        self.button_start.setObjectName("button_start")
        self.button_determine = QtWidgets.QPushButton(self.centralwidget)
        self.button_determine.setGeometry(QtCore.QRect(430, 140, 93, 28))
        self.button_determine.setObjectName("button_determine")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 577, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupUi(self, MainWindow):
        self.font_label = QFont()
        self.font_label.setPointSize(10)

        MainWindow.resize(800, 720)
        MainWindow.setFixedSize(800, 720)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        # MainWindow.move(300, 100)

        self.notice_Label = QtWidgets.QLabel(self.central_widget)
        self.notice_Label.setGeometry(QtCore.QRect(40, 25, 300, 40))
        self.notice_Label.setFont(self.font_label)
        self.notice_Label.setText('间隔%d秒检查一次网站' % applicationContext.cycle)

        self.central_widget.setObjectName("central_widget")
        self.log_Browser = QtWidgets.QTextBrowser(self.central_widget)
        self.log_Browser.setGeometry(QtCore.QRect(40, 80, 720, 460))
        self.log_Browser.setObjectName("log_Browser")

        self.warning_Label = QtWidgets.QLabel(self.central_widget)
        self.warning_Label.setGeometry(QtCore.QRect(40, 550, 200, 40))
        self.warning_Label.setStyleSheet('font-size:20;color:red;')
        # self.warning_Label.setFrameShape(QtWidgets.QFrame.Box)
        self.warning_Label.setFont(self.font_label)
        # self.warning_Label.setAlignment(Qt.AlignCenter)
        # self.warning_Label.setText('Warning')

        self.switch_ftqq_ComboBox = QtWidgets.QCheckBox(self.central_widget)
        self.switch_ftqq_ComboBox.setGeometry(QtCore.QRect(40, 600, 180, 40))
        self.switch_ftqq_ComboBox.stateChanged.connect(self.switch_ftqq_ComboBox_onchange)
        self.switch_ftqq_ComboBox.setText('开启微信推送')

        # self.switch_ftqq_Label = QtWidgets.QLabel(self.central_widget)
        # self.switch_ftqq_Label.setGeometry(QtCore.QRect(60, 600, 120, 40))
        # self.switch_ftqq_Label.setFont(self.font_label)
        # self.switch_ftqq_Label.setText('开启微信推送')

        self.ftqq_key_Label = QtWidgets.QLabel(self.central_widget)
        self.ftqq_key_Label.setGeometry(QtCore.QRect(180, 600, 120, 40))
        self.ftqq_key_Label.setFont(self.font_label)
        self.ftqq_key_Label.setText('Serer酱Key:')

        self.ftqq_key_Edit = QtWidgets.QLineEdit(self.central_widget)
        self.ftqq_key_Edit.setGeometry(QtCore.QRect(280, 605, 480, 28))
        self.ftqq_key_Edit.setPlaceholderText('请填入server酱服务的key')
        self.ftqq_key_Edit.setReadOnly(True)
        self.ftqq_key_Edit.setDisabled(True)

        self.button_start = QtWidgets.QPushButton(self.central_widget)
        self.button_start.setGeometry(QtCore.QRect(260, 660, 93, 28))
        self.button_start.setObjectName("button_start")

        self.button_determine = QtWidgets.QPushButton(self.central_widget)
        self.button_determine.setGeometry(QtCore.QRect(447, 660, 93, 28))
        self.button_determine.setObjectName("button_determine")
        # self.button_determine.setDisabled(True)

        MainWindow.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 577, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "网站首页检查器 v%s -- by %s" % (applicationContext.version, applicationContext.author)))
        self.button_start.setText(_translate("MainWindow", "启动"))
        self.button_determine.setText(_translate("MainWindow", "关闭"))

    def switch_ftqq_ComboBox_onchange(self, state):
        self.ftqq_key_Edit.setReadOnly(state == 0)
        self.ftqq_key_Edit.setDisabled(state == 0)
