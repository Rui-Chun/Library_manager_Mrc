from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import sys

class stuViewWidget(QWidget):
    def __init__(self,stu_id):
        super(stuViewWidget,self).__init__()

        self.resize(900,600)

