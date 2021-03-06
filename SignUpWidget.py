from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import sys
import hashlib

class SignUpWidget(QWidget):
    def __init__(self):
        super(SignUpWidget, self).__init__()

        self.resize(900, 600)

        # 欢迎
        font_0 = QFont()
        font_0.setPixelSize(30)
        font_1 = QFont()
        font_1.setPixelSize(16)
        font_2 = QFont()
        font_2.setPixelSize(18)
        self.label_welcome = QLabel("欢迎注册Library Manager！")
        self.label_welcome.setFixedWidth(390)
        self.label_welcome.setFont(font_0)
        self.label_id = QLabel("学号")
        self.label_id.setFont(font_1)
        self.label_name = QLabel("姓名")
        self.label_name.setFont(font_1)
        self.label_pswd = QLabel("密码")
        self.label_pswd.setFont(font_1)
        self.label_repswd = QLabel("再次输入密码")
        self.label_repswd.setFont(font_1)
        self.lineEdit_id = QLineEdit()
        self.lineEdit_id.setFont(font_2)
        self.lineEdit_id.setMaxLength(10)
        self.lineEdit_id.setFixedHeight(32)
        self.lineEdit_id.setFixedWidth(180)
        self.lineEdit_name = QLineEdit()
        self.lineEdit_name.setFont(font_2)
        self.lineEdit_name.setMaxLength(10)
        self.lineEdit_name.setFixedHeight(32)
        self.lineEdit_name.setFixedWidth(180)
        self.lineEdit_pswd = QLineEdit()
        self.lineEdit_pswd.setFont(font_2)
        self.lineEdit_pswd.setMaxLength(30)
        self.lineEdit_pswd.setFixedWidth(180)
        self.lineEdit_pswd.setFixedHeight(32)
        self.lineEdit_pswd.setEchoMode(QLineEdit.Password)
        self.lineEdit_repswd = QLineEdit()
        self.lineEdit_repswd.setFont(font_2)
        self.lineEdit_repswd.setMaxLength(30)
        self.lineEdit_repswd.setFixedWidth(180)
        self.lineEdit_repswd.setFixedHeight(32)
        self.lineEdit_repswd.setEchoMode(QLineEdit.Password)
        self.button_signUp = QPushButton("注 册")
        self.button_signUp.setFixedHeight(30)
        self.button_signUp.setFixedWidth(90)
        self.button_signUp.setFont(font_1)

        # Layout
        self.Vlayout_main = QVBoxLayout()
        self.Hlayout_0 = QHBoxLayout()
        self.Hlayout_1 = QHBoxLayout()
        self.Flayout = QFormLayout()

        self.Hlayout_0.addWidget(self.label_welcome, Qt.AlignCenter)
        self.subWidget_0 = QWidget()
        self.subWidget_0.setLayout(self.Hlayout_0)
        self.Flayout.addRow(self.label_id, self.lineEdit_id)
        self.Flayout.addRow(self.label_name, self.lineEdit_name)
        self.Flayout.addRow(self.label_pswd, self.lineEdit_pswd)
        self.Flayout.addRow(self.label_repswd, self.lineEdit_repswd)
        self.Flayout.addRow("", self.button_signUp)
        self.subWidget_1 = QWidget()
        self.subWidget_1.setLayout(self.Flayout)
        self.subWidget_1.setFixedWidth(300)
        self.subWidget_1.setFixedHeight(250)
        self.Hlayout_1.addWidget(self.subWidget_1, Qt.AlignCenter)
        self.subWidget_2 = QWidget()
        self.subWidget_2.setLayout(self.Hlayout_1)
        self.Vlayout_main.addWidget(self.subWidget_0)
        self.Vlayout_main.addWidget(self.subWidget_2, Qt.AlignCenter)
        self.setLayout(self.Vlayout_main)

        self.button_signUp.pressed.connect(self.SignUpSlot)

        # 设置验证
        reg = QRegExp("(PB,AD)[0~9]{8}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.lineEdit_id.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.lineEdit_pswd.setValidator(pValidator)
        self.lineEdit_repswd.setValidator(pValidator)

    stuSignup_signal = pyqtSignal(str)


    def SignUpSlot(self):
        id=self.lineEdit_id.text()
        name=self.lineEdit_name.text()
        pswd=self.lineEdit_pswd.text()
        repswd=self.lineEdit_repswd.text()

        if id=="" or name =="" or pswd =="" or repswd =="":
            print(QMessageBox.warning(self, "警告", "输入格式错误", QMessageBox.Yes))
            return
        elif pswd != repswd:
            print(QMessageBox.warning(self, "警告", "两次输入密码应一致", QMessageBox.Yes))
            return
        else:
            pswd_md5=hashlib.md5()
            pswd_md5.update(pswd.encode(encoding='utf-8'))

            Lib_db = QSqlDatabase.addDatabase("QSQLITE")
            Lib_db.setDatabaseName('Library_db.db')
            Lib_db.open()
            query = QSqlQuery()
            sql = "SELECT * FROM user WHERE Pswd='%s'" % (pswd_md5.hexdigest())
            query.exec_(sql)
            if query.next() is None:
                print(QMessageBox.warning(self, "提示", "账号已存在,请重新输入", QMessageBox.Yes))
                return
            else:
                sql="INSERT INTO User VALUES ('%s', '%s', '%s' ,0)" % (id, name, pswd_md5.hexdigest())
                if name == 'root':
                    sql = "INSERT INTO User VALUES ('%s', '%s', '%s' ,1)" % (id, name, pswd_md5.hexdigest())
                query.exec_(sql)
                print(Lib_db.lastError().text())
                Lib_db.commit()
                print(Lib_db.lastError().text())
                print(QMessageBox.information(self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
                self.stuSignup_signal.emit(id)
            Lib_db.close()
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMindow = SignUpWidget()
    mainMindow.show()
    sys.exit(app.exec_())
