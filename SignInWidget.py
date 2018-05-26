from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import sys
import hashlib


class SignInWidget(QWidget):
    def __init__(self):
        super(SignInWidget, self).__init__()
        self.resize(900, 600)
        #欢迎
        font_0=QFont()
        font_0.setPixelSize(30)
        font_1=QFont()
        font_1.setPixelSize(16)
        font_2=QFont()
        font_2.setPixelSize(18)
        self.label_welcome=QLabel("欢迎登陆Library Manager！")
        self.label_welcome.setFixedWidth(390)
        self.label_welcome.setFont(font_0)
        self.label_id=QLabel("账号")
        self.label_id.setFont(font_1)
        self.label_pswd = QLabel("密码")
        self.label_pswd.setFont(font_1)
        self.lineEdit_id=QLineEdit()
        self.lineEdit_id.setFont(font_2)
        self.lineEdit_id.setMaxLength(10)
        self.lineEdit_id.setFixedHeight(32)
        self.lineEdit_id.setFixedWidth(180)
        self.lineEdit_pswd = QLineEdit()
        self.lineEdit_pswd.setFont(font_2)
        self.lineEdit_pswd.setMaxLength(30)
        self.lineEdit_pswd.setFixedWidth(180)
        self.lineEdit_pswd.setFixedHeight(36)
        self.lineEdit_pswd.setEchoMode(QLineEdit.Password)
        self.button_signIn=QPushButton("登 录")
        self.button_signIn.setFixedHeight(30)
        self.button_signIn.setFixedWidth(90)
        self.button_signIn.setFont(font_1)

        #Layout
        self.Vlayout_main=QVBoxLayout(self)
        self.Hlayout_0=QHBoxLayout()
        self.Hlayout_1=QHBoxLayout()
        self.Flayout=QFormLayout()

        self.Hlayout_0.addWidget(self.label_welcome, Qt.AlignCenter)
        self.subWidget_0=QWidget()
        self.subWidget_0.setLayout(self.Hlayout_0)
        self.Flayout.addRow(self.label_id, self.lineEdit_id)
        self.Flayout.addRow(self.label_pswd, self.lineEdit_pswd)
        self.Flayout.addRow("", self.button_signIn)
        self.subWidget_1=QWidget()
        self.subWidget_1.setLayout(self.Flayout)
        self.subWidget_1.setFixedWidth(300)
        self.subWidget_1.setFixedHeight(150)
        self.Hlayout_1.addWidget(self.subWidget_1, Qt.AlignCenter)
        self.subWidget_2=QWidget()
        self.subWidget_2.setLayout(self.Hlayout_1)
        self.Vlayout_main.addWidget(self.subWidget_0)
        self.Vlayout_main.addWidget(self.subWidget_2, Qt.AlignCenter)

        # 设置验证
        pValidator = QRegExpValidator(self)
        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.lineEdit_pswd.setValidator(pValidator)

        self.button_signIn.pressed.connect(self.SignIn_Slot)
        self.lineEdit_pswd.returnPressed.connect(self.SignIn_Slot)

    is_admin_signal = pyqtSignal(str)
    is_student_signal = pyqtSignal(str)

    def SignIn_Slot(self):
        id = self.lineEdit_id.text()
        pswd = self.lineEdit_pswd.text()
        if (id == "" or pswd == ""):
            print(QMessageBox.warning(self, "警告", "输入正确格式!", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库连接
        Lib_db = QSqlDatabase.addDatabase("QSQLITE")
        Lib_db.setDatabaseName('Library_db.db')
        Lib_db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM user WHERE Id='%s'" % (id)
        query.exec_(sql)
        Lib_db.close()

        pswd_md5 = hashlib.md5()
        pswd_md5.update(pswd.encode(encoding='utf-8'))
        if not query.next():
            print(QMessageBox.information(self, "提示", "账号不存在!", QMessageBox.Yes, QMessageBox.Yes))
        else:
            if id == query.value(0) and pswd_md5.hexdigest() == query.value(2):
                # 如果是管理员
                if (query.value(3) == 1):
                    self.is_admin_signal.emit(id)
                else:
                    self.is_student_signal.emit(id)
            else:
                print(QMessageBox.information(self, "提示", "密码错误!", QMessageBox.Yes, QMessageBox.Yes))
        return




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainMindow = SignInWidget()
    mainMindow.show()
    sys.exit(app.exec_())
