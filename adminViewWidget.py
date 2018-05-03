from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import sys
from addBookInfoDialog import addBookDia

class adminViewWidget(QWidget):
    def __init__(self):
        super(adminViewWidget, self).__init__()

        self.resize(900, 600)
        self.setWindowIcon(QIcon("images/book--pencil.png"))

        # Search Line of widget
        font_0 = QFont()
        font_0.setPixelSize(16)
        self.lineEdit_search = QLineEdit()
        self.lineEdit_search.setFixedHeight(32)
        self.setFont(font_0)
        self.button_search = QPushButton("查询")
        self.button_search.setFont(font_0)
        self.button_search.setFixedHeight(32)
        # self.button_search.setIcon(QIcon(""))
        self.combobox_search = QComboBox()
        self.combobox_search.setFont(font_0)
        self.combobox_search.setFixedHeight(32)
        self.combobox_search.addItems(['书名查询', '书号查询', '作者查询', '分类查询', '出版社查询'])

        self.Hlayout_0 = QHBoxLayout()
        self.Hlayout_0.addWidget(self.lineEdit_search)
        self.Hlayout_0.addWidget(self.button_search)
        self.Hlayout_0.addWidget(self.combobox_search)

        self.button_addBook = QPushButton("添加图书")
        # self.button_addBook.setFixedWidth(150)
        self.button_addBook.setFixedHeight(42)
        self.button_addBook.setFont(font_0)
        self.button_delBook = QPushButton("删除图书")
        # self.button_delBook.setFixedWidth(150)
        self.button_delBook.setFixedHeight(42)
        self.button_delBook.setFont(font_0)
        self.button_submit = QPushButton("提交修改")
        # self.button_submit.setFixedWidth(150)
        self.button_submit.setFixedHeight(42)
        self.button_submit.setFont(font_0)
        self.button_revert = QPushButton("撤销未提交修改")
        # self.button_revert.setFixedWidth(150)
        self.button_revert.setFixedHeight(42)
        self.button_revert.setFont(font_0)

        self.Hlayout_1 = QHBoxLayout()
        self.Hlayout_1.addWidget(self.button_addBook)
        self.Hlayout_1.addWidget(self.button_delBook)
        self.Hlayout_1.addWidget(self.button_submit)
        self.Hlayout_1.addWidget(self.button_revert)

        # Table View
        self.Lib_db = QSqlDatabase.addDatabase('QSQLITE')
        self.Lib_db.setDatabaseName('Library_db.db')
        self.Lib_db.open()
        self.queryModel = QSqlTableModel(db=self.Lib_db)
        self.queryModel.setTable("BookInfo")
        self.queryModel.select()
        self.queryModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.tableView = QTableView()
        self.tableView.setModel(self.queryModel)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout_main = QVBoxLayout()
        self.layout_main.addLayout(self.Hlayout_0)
        self.layout_main.addWidget(self.tableView)
        self.layout_main.addLayout(self.Hlayout_1)

        # 布局完成
        self.setLayout(self.layout_main)

        self.SearchSlot()

        self.button_search.pressed.connect(self.SearchSlot)
        self.lineEdit_search.returnPressed.connect(self.SearchSlot)
        self.combobox_search.currentIndexChanged.connect(lambda x: self.SearchSlot())
        self.button_submit.pressed.connect(self.submitSlot)
        self.button_revert.pressed.connect(self.revertSlot)
        self.button_delBook.pressed.connect(self.deleteSlot)
        self.button_addBook.pressed.connect(self.addSlot)

    def SearchSlot(self):
        optionList = ['BookName', 'BookId', 'Auth', 'Category', 'Publisher']
        searchOption = optionList[self.combobox_search.currentIndex()]
        condition = self.lineEdit_search.text()

        if condition == '':
            self.queryModel.setFilter("")
        else:
            condition = '%' + condition + '%'
            sql = "%s LIKE '%s' ORDER BY '%s';" % (
                searchOption, condition, searchOption)
            self.queryModel.setFilter(sql)

        self.queryModel.setHeaderData(0, Qt.Horizontal, "书名")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.queryModel.setHeaderData(4, Qt.Horizontal, "地点")
        self.queryModel.setHeaderData(5, Qt.Horizontal, "出版社")
        self.queryModel.setHeaderData(6, Qt.Horizontal, "出版时间")
        self.queryModel.setHeaderData(7, Qt.Horizontal, "库存")
        self.queryModel.setHeaderData(8, Qt.Horizontal, "剩余可借")

    def submitSlot(self):
        msgBox = QMessageBox.question(self,"是否确认提交？","确认后更改将被提交到数据库", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if msgBox == QMessageBox.Yes:
            self.queryModel.submitAll()
            self.SearchSlot()


    def revertSlot(self):
        self.queryModel.revertAll()
        #self.SearchSlot()

    def addSlot(self):
        addDialog = addBookDia(self)
        addDialog.add_book_success_signal.connect(self.SearchSlot)
        addDialog.show()
        addDialog.exec_()
        self.SearchSlot()

    def deleteSlot(self):
        tempQuery = QSqlQuery(self.Lib_db)
        index = self.tableView.selectedIndexes()
        if len(index) == 0:
            return
        msgBox = QMessageBox.question(self, "是否确认？", "确认后将从数据库删除该条记录", QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
        if msgBox == QMessageBox.No:
            return
        if len(index) != 1 or index[0].column() != 1:
            QMessageBox.warning(self, "提示", "请仅选择一个书号~", QMessageBox.Yes, QMessageBox.No)
            return
        del_id = self.queryModel.data(index[0], Qt.DisplayRole)
        sql = "SELECT * FROM BookInfo WHERE BookId == '%s'" % del_id
        tempQuery.exec_(sql)
        tempQuery.first()
        if tempQuery.value(7) != tempQuery.value(8):
            msgBox = QMessageBox.question(self, "是否确认？", "该书仍有同学借阅！", QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No)
            if msgBox == QMessageBox.No:
                return
        sql = "DELETE FROM BookInfo WHERE BookId == '%s'" % del_id
        tempQuery.exec_(sql)
        # adminLog ????
        sql = "INSERT INTO adminLog VALUES ('%s', '%s', Date('now'), 0, %d )" % \
              (del_id, tempQuery.value(0), tempQuery.value(7))
        tempQuery.exec_(sql)
        QMessageBox.information(self,"完成", "删除图书完成", QMessageBox.Yes,QMessageBox.Yes)
        self.SearchSlot()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainMindow = adminViewWidget()
    mainMindow.show()
    sys.exit(app.exec_())