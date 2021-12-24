from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
import sys
import youtube_dl
import os


class Downloader(QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.link = None

    def init_link(self, link):
        self.link = link

    def run(self):
        self.mysignal.emit('Видеоролик загружается..')

        with youtube_dl.YoutubeDL({}) as ydl:
            ydl.download([self.link])

        self.mysignal.emit('Видеоролик загружен!')
        self.mysignal.emit('finish')



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 230)
        Form.setMinimumSize(QtCore.QSize(400, 230))
        Form.setMaximumSize(QtCore.QSize(400, 230))
        Form.setStyleSheet("background-color: rgb(255, 60, 60);")
        self.btn_download = QtWidgets.QPushButton(Form)
        self.btn_download.setGeometry(QtCore.QRect(75, 180, 250, 40))
        self.btn_download.setMinimumSize(QtCore.QSize(250, 40))
        self.btn_download.setMaximumSize(QtCore.QSize(250, 40))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(18)
        self.btn_download.setFont(font)
        self.btn_download.setStyleSheet("QPushButton {\n"
        "border: 2px solid #ffffff;\n"
        "color: #ffffff;\n"
        "}\n"
        "QPushButton:hover {\n"
        "border: 2px solid #ffffff;\n"
        "color: #ffffff;\n"
        "background-color: rgb(255, 100, 100);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "border: 2px solid red;\n"
        "color: #ffffff;\n"
        "background-color: red;\n"
        "}\n"
        "")
        self.btn_download.setObjectName("btn_download")
        self.btn_path = QtWidgets.QPushButton(Form)
        self.btn_path.setGeometry(QtCore.QRect(290, 140, 100, 30))
        self.btn_path.setMinimumSize(QtCore.QSize(100, 30))
        self.btn_path.setMaximumSize(QtCore.QSize(100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(9)
        self.btn_path.setFont(font)
        self.btn_path.setStyleSheet("QPushButton {\n"
        "border: 2px solid #ffffff;\n"
        "color: #ffffff;\n"
        "}\n"
        "QPushButton:hover {\n"
        "border: 2px solid #ffffff;\n"
        "color: #ffffff;\n"
        "background-color: rgb(255, 100, 100);\n"
        "}\n"
        "QPushButton:pressed {\n"
        "border: 2px solid red;\n"
        "color: #ffffff;\n"
        "background-color: red;\n"
        "}\n"
        "")
        self.btn_path.setObjectName("btn_path")
        self.line_link = QtWidgets.QLineEdit(Form)
        self.line_link.setGeometry(QtCore.QRect(10, 140, 270, 30))
        self.line_link.setMinimumSize(QtCore.QSize(270, 30))
        self.line_link.setMaximumSize(QtCore.QSize(270, 30))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        self.line_link.setFont(font)
        self.line_link.setStyleSheet("border: 2px solid #ffffff;\n"
        "color: #ffffff;")
        self.line_link.setObjectName("line_link")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 380, 80))
        self.plainTextEdit.setMinimumSize(QtCore.QSize(380, 120))
        self.plainTextEdit.setMaximumSize(QtCore.QSize(380, 120))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet("border: 2px solid #ffffff;\n"
        "color: #ffffff;")
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.download_path = None

        self.mythread = Downloader()

        self.mythread.mysignal.connect(self.handler)

        self.btn_path.clicked.connect(self.choose_path)
        self.btn_download.clicked.connect(self.download)


    def choose_path(self):
        self.download_path = QtWidgets.QFileDialog.getExistingDirectory()
        os.chdir(self.download_path)
        print(self.download_path)

    def download(self):
        link = self.line_link.text()
        self.mythread.init_link(link)
        self.mythread.start()
        self.locker_btns(True)

    def handler(self, value):
        if value == 'finish':
            self.locker_btns(False)
        else:
            self.plainTextEdit.appendPlainText(value)

    def locker_btns(self, lock_value):
        btns = [self.btn_path, self.btn_download]
        for btn in btns:
            btn.setDisabled(lock_value)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Скачать видео с Youtube"))
        self.btn_download.setText(_translate("Form", "Скачать"))
        self.btn_path.setText(_translate("Form", "Укажите путь"))
        self.line_link.setText(_translate("Form", "https://www.youtube.com/"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
