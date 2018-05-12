import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import hashlib
from PyQt5.QtSql import *


class addAdminDia(QDialog):
    add_admin_success_signal = pyqtSignal()

    def __init__(self, parent = None):
        super(addAdminDia, self).__init__(parent)
        self.setWindowTitle("添加管理账号")
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        font_0 = QFont()
        font_0.setPixelSize(20)
        font_1 =QFont()
        font_1.setPixelSize(14)

        self.label_title = QLabel("添加Admin")
        self.label_title.setFont(font_0)
        self.label_title.setFixedWidth(150)
        self.label_Id = QLabel("帐号")
        self.label_Id.setFont(font_1)
        self.label_Name =QLabel("用户名")
        self.label_Name.setFont(font_1)

        self.label_Pswd = QLabel("密码")
        self.label_Pswd.setFont(font_1)
        self.label_rePswd = QLabel("再次输入密码")
        self.label_rePswd.setFont(font_1)

        self.LineEdit_Id = QLineEdit()
        self.LineEdit_Name = QLineEdit()
        self.LineEdit_Pswd = QLineEdit()
        self.LineEdit_rePswd = QLineEdit()

        self.LineEdit_Id.setMaxLength(10)
        self.LineEdit_Name.setMaxLength(20)
        self.LineEdit_Pswd.setMaxLength(30)
        self.LineEdit_Pswd.setEchoMode(QLineEdit.Password)
        self.LineEdit_rePswd.setEchoMode(QLineEdit.Password)
        self.LineEdit_rePswd.setMaxLength(30)

        self.Button_add = QPushButton("添加")

        self.layout.addRow("", self.label_title)
        self.layout.addRow(self.label_Id, self.LineEdit_Id)
        self.layout.addRow(self.label_Name, self.LineEdit_Name)
        self.layout.addRow(self.label_Pswd, self.LineEdit_Pswd)
        self.layout.addRow(self.label_rePswd, self.LineEdit_rePswd)
        self.layout.addRow("", self.Button_add)

        self.label_title.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.Button_add.pressed.connect(self.addBookSlot)

    def addBookSlot(self):
        Id = self.LineEdit_Id.text()
        Name =self.LineEdit_Name.text()
        Pswd = self.LineEdit_Pswd.text()
        rePswd = self.LineEdit_rePswd.text()
        if Id == '' or Name == '' or Pswd == '' or rePswd == '':
            QMessageBox.warning(self, "警告", "有字段为空，添加失败", QMessageBox.Yes, QMessageBox.Yes)
            return
        elif Pswd != rePswd:
            QMessageBox.warning(self, "警告", "两次密码不一致", QMessageBox.Yes, QMessageBox.Yes)
            return
        else:
            pswd_md5 = hashlib.md5()
            pswd_md5.update(Pswd.encode(encoding='utf-8'))
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('Library_db.db')
            db.open()
            query = QSqlQuery()
            sql = "INSERT INTO User VALUES ('%s','%s','%s', 1)" % (Id, Name, pswd_md5.hexdigest())
            query.exec_(sql)
            db.commit()
            QMessageBox.information(self, "提示", "添加成功!", QMessageBox.Yes, QMessageBox.Yes)
            self.add_admin_success_signal.emit()
            self.close()
        return



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMindow = addAdminDia()
    mainMindow.show()
    sys.exit(app.exec_())


