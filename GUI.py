import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QComboBox, QCheckBox

from Ui_MainWindow import Ui_MainWindow


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
        self.is_push = False
        self.ftqq_key = ''
        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.resize(800, 700)
        self.window.move(300, 100)
        self.window.setWindowTitle('PT Searcher')

        self.ft = QFont();
        self.ft.setPointSize(12);

        self.warningLabel = QLabel(self.window)
        self.warningLabel.move(50, 10)
        self.warningLabel.resize(800, 40)
        self.warningLabel.setStyleSheet('font-size:20;color:red;')
        # self.warning_Label.setFrameShape(QtWidgets.QFrame.Box)
        self.warningLabel.setFont(self.ft)
        self.warningLabel.setAlignment(Qt.AlignCenter)
        # self.warning_Label.setText('warning')

        ftqqComboBox_h = 50
        ftqqComboBox_v = 700 - 100
        ftqq_label_width = 120
        ftqq_label_height = 25
        self.ftqqComboBox = QCheckBox(self.window)
        self.ftqqComboBox.move(ftqqComboBox_h, ftqqComboBox_v)
        # self.is_ftqq_ComboBox.resize(ftqqComboBox_width, ftqqComboBox_height)

        self.ftqqLabel = QLabel(self.window)
        self.ftqqLabel.move(ftqqComboBox_h + 25, ftqqComboBox_v)
        self.ftqqLabel.resize(ftqq_label_width, ftqq_label_height)
        self.ftqqLabel.setFont(self.ft)
        self.ftqqLabel.setText('开启微信推送')

        self.ftqq_key_Edit = QLineEdit(self.window)
        self.ftqq_key_Edit.setPlaceholderText('请填入server酱服务的key')
        self.ftqq_key_Edit.move(ftqqComboBox_h + ftqq_label_width + 30, ftqqComboBox_v)
        self.ftqq_key_Edit.resize(500, 28)
        self.ftqq_key_Edit.setFont(self.ft)
        self.ftqq_key_Edit.returnPressed.connect(self.handleSearch)
        self.ftqq_key_Edit.textChanged.connect(lambda: self.handleKeywordEditChanged(self.ftqq_key_Edit.text()))
        self.ftqq_key_Edit.setReadOnly(True)
        self.ftqq_key_Edit.setDisabled(True)

        # self.is_ftqq_ComboBox.setFont(self.ft)
        # self.is_ftqq_ComboBox.addItem('Palemoon')
        # self.is_ftqq_ComboBox.addItem('Chrome')

        self.button_start = QPushButton('启动', self.window)
        self.button_start.move(ftqqComboBox_h, ftqqComboBox_v + 50)
        self.button_start.resize(100, 30)
        self.button_start.setFont(self.ft)
        self.button_start.setDisabled(False)
        self.button_start.clicked.connect(self.handleSearch)

        self.button_determine = QPushButton('停止', self.window)
        self.button_determine.move(ftqqComboBox_h + 200, ftqqComboBox_v + 50)
        self.button_determine.resize(100, 30)
        self.button_determine.setFont(self.ft)
        self.button_determine.setDisabled(True)
        self.button_determine.clicked.connect(self.handleSearch)

        self.window.show()
        self.app.exec_()

    # Signal_NoParameters = PQC.pyqtSignal()

    # button_start.setDisabled(True)

    def handleKeywordEditChanged(self, text):
        self.button_start.setDisabled(len(text.strip()) <= 0)

    def handleSearch(self):
        self.ftqq_key_Edit.setText(self.ftqq_key_Edit.text().strip())
        if self.ftqq_key_Edit.text() == '':
            self.warning('请输入搜索关键字')
        elif self.last_keywords[self.ftqqComboBox.currentText()] != self.ftqq_key_Edit.text():
            self.warningLabel.setText('')
            searcher.search(self.ftqqComboBox.currentText(), self.ftqq_key_Edit.text())
            self.last_keywords[self.ftqqComboBox.currentText()] = self.ftqq_key_Edit.text()
        else:
            self.warning('请勿连续重复搜索')

    def warning(self, context):
        self.warningLabel.setText(context)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = Main()
    mainWindow.show()

    sys.exit(app.exec_())
