import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from PyQt5.QtSql import *


class addBookDia(QDialog):
    add_book_success_signal = pyqtSignal()

    def __init__(self, parent = None):
        super(addBookDia, self).__init__(parent)
        self.setWindowTitle("添加书籍")
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        font_0 = QFont()
        font_0.setPixelSize(20)
        font_1 =QFont()
        font_1.setPixelSize(14)

        self.label_title = QLabel("添加书籍")
        self.label_title.setFont(font_0)
        self.label_title.setFixedWidth(150)
        self.label_bookName =QLabel("书名")
        self.label_bookName.setFont(font_1)
        self.label_bookId = QLabel("书号")
        self.label_bookId.setFont(font_1)
        self.label_Auth =QLabel("作者")
        self.label_Auth.setFont(font_1)
        self.label_Category = QLabel("分类")
        self.label_Category.setFont(font_1)
        self.label_location =QLabel("地点")
        self.label_location.setFont(font_1)
        self.label_Publisher = QLabel("出版社")
        self.label_Publisher.setFont(font_1)
        self.label_PublishTime = QLabel("出版时间")
        self.label_PublishTime.setFont(font_1)
        self.label_Storage = QLabel("库存")
        self.label_Storage.setFont(font_1)

        Category = ["数学", "化学", "物理", "计算机", "信息技术", "文学", "社科"]

        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(Category)
        self.publisherEdit = QLineEdit()
        self.locationEdit = QLineEdit()
        self.publishTime = QDateTimeEdit()
        self.publishTime.setDisplayFormat("yyyy-MM-dd")
        # self.publishDateEdit = QLineEdit()
        self.addNumEdit = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(6)
        self.authNameEdit.setMaxLength(10)
        self.locationEdit.setMaxLength(30)
        self.publisherEdit.setMaxLength(20)
        self.addNumEdit.setMaxLength(12)
        self.addNumEdit.setValidator(QIntValidator())

        self.addBookButton = QPushButton("添加")

        self.layout.addRow("", self.label_title)
        self.layout.addRow(self.label_bookName, self.bookNameEdit)
        self.layout.addRow(self.label_bookId, self.bookIdEdit)
        self.layout.addRow(self.label_Auth, self.authNameEdit)
        self.layout.addRow(self.label_Category, self.categoryComboBox)
        self.layout.addRow(self.label_location, self.locationEdit)
        self.layout.addRow(self.label_Publisher, self.publisherEdit)
        self.layout.addRow(self.label_PublishTime, self.publishTime)
        self.layout.addRow(self.label_Storage, self.addNumEdit)
        self.layout.addRow("", self.addBookButton)

        self.label_title.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.addBookButton.pressed.connect(self.addBookSlot)

    def addBookSlot(self):
        bookName = self.bookNameEdit.text()
        bookId = self.bookIdEdit.text()
        authName = self.authNameEdit.text()
        bookCategory = self.categoryComboBox.currentText()
        location = self.locationEdit.text()
        publisher = self.publisherEdit.text()
        publishTime = self.publishTime.text()
        addBookNum = self.addNumEdit.text()
        if bookName == "" or bookId == "" or authName == "" or bookCategory == "" or publisher == "" or publishTime == "" or addBookNum == "":
            QMessageBox.warning(self, "警告", "有字段为空，添加失败", QMessageBox.Yes, QMessageBox.Yes)
            return
        else:
            addBookNum = int(addBookNum)
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('Library_db.db')
            db.open()
            query = QSqlQuery()
            sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
            query.exec_(sql)
            if (query.next()):
                sql = "UPDATE BookInfo SET Storage=Storage+%d,NumCanBorrow=NumCanBorrow+%d WHERE BookId='%s'" % (
                    addBookNum, addBookNum, bookId)
            else:
                sql = "INSERT INTO BookInfo VALUES ('%s','%s','%s','%s','%s','%s','%s',%d,%d)" % (
                    bookName, bookId, authName, bookCategory, location, publisher, publishTime, addBookNum, addBookNum)
            query.exec_(sql)
            db.commit()
            sql = "INSERT INTO adminLog VALUES ('%s','%s', DATE('now'), 1, %d)" % (bookId, bookName, addBookNum)
            query.exec_(sql)
            db.commit()
            QMessageBox.information(self, "提示", "添加书籍成功!", QMessageBox.Yes, QMessageBox.Yes)
            self.add_book_success_signal.emit()
            self.close()
            self.bookNameEdit.clear()
            self.bookIdEdit.clear()
            self.authNameEdit.clear()
            self.addNumEdit.clear()
            self.publisherEdit.clear()
        return



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainMindow = addBookDia()
    mainMindow.show()
    sys.exit(app.exec_())


