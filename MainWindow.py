from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import sys,os
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
        self.signInAction = QAction("登录", self)
        #self.changePasswordAction = QAction("修改密码", self)
        self.quitSignInAction = QAction("退出登录", self)
        self.MenuInfo = bar.addMenu("关于")
        self.InfoAction = QAction("作者信息", self)
        self.ProjectInfo = QAction("项目信息", self)
        self.Menu.addAction(self.signUpAction)
        self.Menu.addAction(self.signInAction)
        #self.Menu.addAction(self.changePasswordAction)
        self.Menu.addAction(self.quitSignInAction)
        self.MenuInfo.addAction(self.InfoAction)
        self.MenuInfo.addAction(self.ProjectInfo)

        self.signUpAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)


        palette = QPalette()
        icon = QPixmap('images/background.jpg')
        palette.setBrush(self.backgroundRole(), QBrush(icon))  # 添加背景图片
        self.setPalette(palette)

        self.widget.is_admin_signal.connect(self.adminViewSlot)
        self.widget.is_student_signal.connect(self.stuViewSlot)

        self.signInAction.triggered.connect(self.signInAcSlot)
        self.signUpAction.triggered.connect(self.signUpAcSlot)
        self.quitSignInAction.triggered.connect(self.quitSignInAcSlot)
        self.InfoAction.triggered.connect(self.InfoAcSlot)
        self.ProjectInfo.triggered.connect(self.ProjectInfoSlot)


    def adminViewSlot(self,admin_id):
        sip.delete(self.widget)
        self.widget = adminViewWidget(admin_id)
        self.setCentralWidget(self.widget)
        self.signUpAction.setEnabled(False)
        self.signInAction.setEnabled(True)
        self.quitSignInAction.setEnabled(True)

    def stuViewSlot(self, stu_id):
        sip.delete(self.widget)
        self.widget = stuViewWidget(stu_id)
        self.setCentralWidget(self.widget)
        self.signUpAction.setEnabled(False)
        self.signInAction.setEnabled(True)
        self.quitSignInAction.setEnabled(True)

    def signInAcSlot(self):
        sip.delete(self.widget)
        self.widget = SignInWidget()
        self.setCentralWidget(self.widget)
        self.widget.is_admin_signal.connect(self.adminViewSlot)
        self.widget.is_student_signal.connect(self.stuViewSlot)

        self.signUpAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)

    def signUpAcSlot(self):
        sip.delete(self.widget)
        self.widget = SignUpWidget()
        self.setCentralWidget(self.widget)
        self.widget.stuSignup_signal.connect(self.stuViewSlot)

        self.signUpAction.setEnabled(False)
        self.signInAction.setEnabled(True)
        self.quitSignInAction.setEnabled(False)

    def quitSignInAcSlot(self):
        sip.delete(self.widget)
        self.widget = SignInWidget()
        self.setCentralWidget(self.widget)
        self.widget.is_admin_signal.connect(self.adminViewSlot)
        self.widget.is_student_signal.connect(self.stuViewSlot)
        self.signUpAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)

    def InfoAcSlot(self):
        msgBox = QMessageBox.information(self, "作者信息", "马睿淳 PB16001775", QMessageBox.Yes)

    def ProjectInfoSlot(self):
        Qweb = QWebEngineView()
        Qweb.setUrl(QUrl("https://github.com/Rui-Chun/Library_manager_Mrc"))

        self.win2 = QMainWindow()
        self.win2.setCentralWidget(Qweb)
        self.win2.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMindow = MainWindow()
    mainMindow.show()
    sys.exit(app.exec_())