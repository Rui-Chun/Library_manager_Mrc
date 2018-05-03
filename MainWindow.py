from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import sip

from SignInWidget import SignInWidget
from SignUpWidget import SignUpWidget
from stuViewWidget import stuViewWidget
from adminViewWidget import adminViewWidget


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(900, 600)
        self.setWindowTitle("Library Manager~~~")
        self.setWindowIcon(QIcon("images/books-brown.png"))
        self.widget=SignInWidget()
        self.setCentralWidget(self.widget)
        bar = self.menuBar()
        self.Menu = bar.addMenu("账号设置")
        self.signUpAction = QAction("注册", self)
        #self.changePasswordAction = QAction("修改密码", self)
        self.quitSignInAction = QAction("退出登录", self)
        self.MenuInfo = bar.addMenu("关于")
        self.InfoAction = QAction("作者信息", self)
        self.ProjectInfo = QAction("项目信息", self)
        self.Menu.addAction(self.signUpAction)
        #self.Menu.addAction(self.changePasswordAction)
        self.Menu.addAction(self.quitSignInAction)
        self.MenuInfo.addAction(self.InfoAction)
        self.MenuInfo.addAction(self.ProjectInfo)

        self.signUpAction.setEnabled(True)
        self.quitSignInAction.setEnabled(False)

        self.widget.is_admin_signal.connect(self.adminViewSlot)
        self.widget.is_student_signal.connect(self.stuViewSlot)
        self.Menu.triggered.connect(self.MenuSlot)
        self.MenuInfo.triggered.connect(self.MenuInfoSlot)


    def adminViewSlot(self):
        sip.delete(self.widget)
        self.widget = adminViewWidget()
        self.setCentralWidget(self.widget)

    def stuViewSlot(self, stu_id):
        sip.delete(self.widget)
        self.widget = stuViewWidget(stu_id)
        self.setCentralWidget(self.widget)

    def MenuSlot(self, Action):
        if Action.text() == "注册":
            sip.delete(self.widget)
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)
            self.widget.stuSignup_signal.connect(self.stuViewSlot)
            self.signUpAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        elif Action.text() == "退出登录":
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.signUpAction.setEnabled(True)
            self.quitSignInAction.setEnabled(False)

    def MenuInfoSlot(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMindow = MainWindow()
    mainMindow.show()
    sys.exit(app.exec_())