from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import sip

from SignInWidget import SignInWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(900, 600)
        self.setWindowTitle("Library Manager~~~")
        self.setWindowIcon(QIcon("images/books-brown.png"))
        self.widget=SignInWidget()
        self.setCentralWidget(self.widget)
        self.widget.is_admin_signal.connect(self.adminViewSlot)

        #self.widget.is_student_signal.connect(self.stuViewSlot)

    def adminViewSlot(self):
        sip.delete(self.widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMindow = MainWindow()
    mainMindow.show()
    sys.exit(app.exec_())