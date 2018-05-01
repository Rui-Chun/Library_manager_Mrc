from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import sys

class stuViewWidget(QWidget):
    def __init__(self, stu_id):
        super(stuViewWidget,self).__init__()
        self.stu_id = stu_id
        self.resize(900,600)
        self.setWindowIcon(QIcon("images/book--pencil.png"))

        # Search Line of widget
        font_0=QFont()
        font_0.setPixelSize(16)
        self.lineEdit_search=QLineEdit()
        self.lineEdit_search.setFixedHeight(32)
        self.setFont(font_0)
        self.button_search=QPushButton("查询")
        self.button_search.setFont(font_0)
        self.button_search.setFixedHeight(32)
        # self.button_search.setIcon(QIcon(""))
        self.combobox_mode=QComboBox()
        self.combobox_mode.setFont(font_0)
        self.combobox_mode.setFixedHeight(32)
        self.combobox_mode.addItems(['图书借阅', '未归还', '已归还'])
        self.combobox_search=QComboBox()
        self.combobox_search.setFont(font_0)
        self.combobox_search.setFixedHeight(32)
        self.combobox_search.addItems(['书名查询', '书号查询', '作者查询', '分类查询', '出版社查询'])

        self.Hlayout_0=QHBoxLayout()
        self.Hlayout_0.addWidget(self.lineEdit_search)
        self.Hlayout_0.addWidget(self.button_search)
        self.Hlayout_0.addWidget(self.combobox_mode)
        self.Hlayout_0.addWidget(self.combobox_search)

        self.button_submit=QPushButton("借书")
        self.button_submit.setFixedWidth(100)
        self.button_submit.setFixedHeight(42)
        self.button_submit.setFont(font_0)

        self.Hlayout_1=QHBoxLayout()
        self.Hlayout_1.addWidget(self.button_submit, Qt.AlignCenter)

        # Table View
        self.Lib_db=QSqlDatabase.addDatabase('QSQLITE')
        self.Lib_db.setDatabaseName('Library_db.db')
        self.Lib_db.open()
        self.queryModel=QSqlQueryModel()
        self.tableView=QTableView()
        self.tableView.setModel(self.queryModel)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.SearchSlot()  # 显示

        self.layout_main=QVBoxLayout()
        self.layout_main.addLayout(self.Hlayout_0)
        self.layout_main.addWidget(self.tableView)
        self.layout_main.addLayout(self.Hlayout_1)

        # 布局完成
        self.setLayout(self.layout_main)

        self.button_search.pressed.connect(self.SearchSlot)
        self.lineEdit_search.returnPressed.connect(self.SearchSlot)
        self.combobox_mode.currentIndexChanged.connect(lambda x: self.SearchSlot())
        self.combobox_search.currentIndexChanged.connect(lambda x: self.SearchSlot())
        self.button_submit.pressed.connect(self.SubmitSlot)

    def SearchSlot(self):
        modeList=['BookInfo', 'Borrowed', 'Given_back']
        searchMode=modeList[self.combobox_mode.currentIndex()]
        optionList=['BookName', 'BookId', 'Auth', 'Category', 'Publisher']
        searchOption=optionList[self.combobox_search.currentIndex()]
        condition = self.lineEdit_search.text()

        if searchMode == 'BookInfo':
            self.button_submit.setEnabled(True)
            self.button_submit.setText("借书")
            if condition == '':
                sql = "SELECT * FROM BookInfo"
                self.queryModel.setQuery(sql)
            else:
                condition = '%' + condition + '%'
                sql = "SELECT * FROM BookInfo WHERE %s LIKE '%s' ORDER BY '%s';" % (
                    searchOption, condition, searchOption)
                self.queryModel.setQuery(sql)

            self.queryModel.setHeaderData(0, Qt.Horizontal, "书名")
            self.queryModel.setHeaderData(1, Qt.Horizontal, "书号")
            self.queryModel.setHeaderData(2, Qt.Horizontal, "作者")
            self.queryModel.setHeaderData(3, Qt.Horizontal, "分类")
            self.queryModel.setHeaderData(4, Qt.Horizontal, "地点")
            self.queryModel.setHeaderData(5, Qt.Horizontal, "出版社")
            self.queryModel.setHeaderData(6, Qt.Horizontal, "出版时间")
            self.queryModel.setHeaderData(7, Qt.Horizontal, "库存")
            self.queryModel.setHeaderData(8, Qt.Horizontal, "剩余可借")

        elif searchMode == 'Borrowed':
            self.button_submit.setEnabled(True)
            self.button_submit.setText("还书")
            if condition == '':
                sql = "SELECT BookName,BookInfo.BookId, Auth, Location, BorrowTime  " \
                      "FROM BookInfo,User_Book " \
                      "WHERE BookInfo.BookId == User_Book.BookId " \
                      "AND StudentId == '%s' AND User_Book.BorrowState ==1;" % self.stu_id
                self.queryModel.setQuery(sql)
            else:
                condition = '%' + condition + '%'
                sql = "SELECT BookName,BookInfo.BookId, Auth, Location, BorrowTime  " \
                      "FROM BookInfo,User_Book " \
                      "WHERE BookInfo.BookId == User_Book.BookId " \
                      "AND StudentId == '%s' AND User_Book.BorrowState ==1 " \
                      "AND %s LIKE '%s' ORDER BY '%s';" % (self.stu_id, searchOption, condition, searchOption)
                print(self.queryModel.lastError().text())
                self.queryModel.setQuery(sql)
            self.queryModel.setHeaderData(0, Qt.Horizontal, "书名")
            self.queryModel.setHeaderData(1, Qt.Horizontal, "书号")
            self.queryModel.setHeaderData(2, Qt.Horizontal, "作者")
            self.queryModel.setHeaderData(3, Qt.Horizontal, "地点")
            self.queryModel.setHeaderData(4, Qt.Horizontal, "借出时间")

        else:
            self.button_submit.setEnabled(False)
            self.button_submit.setText("")
            if condition == '':
                sql = "SELECT BookName,BookInfo.BookId, Auth, Location,ReturnTime  " \
                      "FROM BookInfo,User_Book " \
                      "WHERE BookInfo.BookId == User_Book.BookId " \
                      "AND StudentId == '%s' AND User_Book.BorrowState ==0;" % self.stu_id
                self.queryModel.setQuery(sql)
            else:
                condition = '%' + condition + '%'
                sql = "SELECT BookName,BookInfo.BookId, Auth, Location,ReturnTime  " \
                      "FROM BookInfo,User_Book " \
                      "WHERE BookInfo.BookId == User_Book.BookId " \
                      "AND StudentId == '%s' AND User_Book.BorrowState ==1 " \
                      "AND %s LIKE '%s' ORDER BY '%s';" % (self.stu_id, searchOption, condition, searchOption)
                print(self.queryModel.lastError().text())
                self.queryModel.setQuery(sql)
            self.queryModel.setHeaderData(0, Qt.Horizontal, "书名")
            self.queryModel.setHeaderData(1, Qt.Horizontal, "书号")
            self.queryModel.setHeaderData(2, Qt.Horizontal, "作者")
            self.queryModel.setHeaderData(3, Qt.Horizontal, "地点")
            self.queryModel.setHeaderData(4, Qt.Horizontal, "归还时间")


    def SubmitSlot(self):
        tempQuery = QSqlQuery(self.Lib_db)
        if self.button_submit.text() == '借书':
            index = self.tableView.selectedIndexes()
            if len(index) != 1 or index[0].column() != 1:
                QMessageBox.warning(self, "提示", "请仅选择一个书号~", QMessageBox.Yes, QMessageBox.Yes)
                return
            borrow_id = self.queryModel.data(index[0], Qt.DisplayRole)
            sql = "SELECT NumCanBorrow FROM BookInfo WHERE BookId ='%s';" % borrow_id
            tempQuery.exec_(sql)
            tempQuery.first()
            if tempQuery.value(0) == 0:
                QMessageBox.warning(self, "提示", "请选择还有库存的书~", QMessageBox.Yes, QMessageBox.Yes)
                return
            sql = "SELECT BorrowState FROM User_Book WHERE BookId ='%s' AND StudentId = '%s' ;" % (borrow_id, self.stu_id)
            tempQuery.exec_(sql)
            if tempQuery.next():
                if tempQuery.value(0) == 1:
                    QMessageBox.warning(self, "提示", "您已经借过该书~", QMessageBox.Yes, QMessageBox.Yes)
                    return
                else:
                    sql = "UPDATE User_Book SET BorrowState = 1, BorrowTime = DATE('now') , ReturnTime = NULL WHERE StudentId = '%s' AND BookId = '%s';" % (self.stu_id, borrow_id)
                    tempQuery.exec_(sql)
                    sql = "UPDATE BookInfo SET NumCanBorrow = NumCanBorrow-1 WHERE BookId = '%s';" % borrow_id
                    tempQuery.exec_(sql)
                    QMessageBox.information(self, "消息", "借阅成功", QMessageBox.Yes)
                    self.SearchSlot()
                    return
            else:
                sql = "UPDATE BookInfo SET NumCanBorrow = NumCanBorrow-1 WHERE BookId = '%s';" % borrow_id
                tempQuery.exec_(sql)
                sql = "INSERT INTO User_Book VALUES ('%s', '%s', DATE('now'), NULL , 1);" % (self.stu_id, borrow_id)
                tempQuery.exec_(sql)
                QMessageBox.information(self, "消息", "借阅成功", QMessageBox.Yes)
                self.SearchSlot()
                return

        elif self.button_submit.text() == '还书':
            index = self.tableView.selectedIndexes()
            if len(index) != 1 or index[0].column() != 1:
                QMessageBox.warning(self, "提示", "请仅选择一个书号~", QMessageBox.Yes, QMessageBox.Yes)
                return
            borrow_id = self.queryModel.data(index[0], Qt.DisplayRole)
            sql = "UPDATE BookInfo SET NumCanBorrow = NumCanBorrow+1 WHERE BookId = '%s';" % borrow_id
            tempQuery.exec_(sql)
            sql = "UPDATE User_Book SET ReturnTime = DATE('now'), BorrowState = 0 WHERE StudentId = '%s' AND BookId = '%s';" % (self.stu_id, borrow_id)
            tempQuery.exec_(sql)
            QMessageBox.information(self, "消息", "还书成功")
            self.SearchSlot()
            return




if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainMindow = stuViewWidget('PB16001775')
    mainMindow.show()
    sys.exit(app.exec_())

