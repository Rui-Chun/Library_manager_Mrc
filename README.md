# Library_manager_Mrc
A Library Manager app using PyQt5 and Sqlite.

# 数据库实验报告

[TOC]


## 机房上机实验

具体SQL语句见 上机实验文件夹 *数据库实验.sql*文件，或者[在线查看](https://github.com/Rui-Chun/Library_manager_Mrc)

## 大作业应用程序

### 代码环境

本程序使用PyQt5+Sqlite实现

尝试将程序编译成exe时，数据库文件连接出现问题。希望助教直接运行代码，造成不便希望谅解。

测试环境：python 3.6

需要安装的包：PyQt5 , sip![5.7](C:\Users\马睿淳\Desktop\大二下\数据库\实验报告\5.7.PNG)

### 说明

1.测试用账号 

学生：PB16001775 密码：123321 

管理员：root 密码：123456

2.单独测试

每个文件可以单独测试运行，但部分图标无法显示。MainWindow.py是正常入口。

3.界面

窗口可拉伸，在高分辨率电脑上字体偏小

###具体功能

#### 登录

<img src="C:\Users\马睿淳\Desktop\大二下\数据库\实验报告\login.PNG" width="70%" height="70%">

输入账号密码登陆

密码转化成 MD5码 与数据库中存储信息比较，对输入格式作了限制，防止sql注入

#### 注册

点击菜单栏 账号设置->注册，进入账号注册页面，输入学号，姓名，密码，再次输入密码，完成学生账号注册。

#### 学生视图

<img src="C:\Users\马睿淳\Desktop\大二下\数据库\实验报告\stuView.PNG" width="70%" height="70%">

下拉菜单可选择搜索类别（图书借阅，未归还，已归还），查询方式。

文本框输入查询条件，回车或者点击查询查询书籍。

借书，还书操作，通过**点击书号**选中，然后点击下方按钮实现。

界面操作后自动查询刷新

#### 管理员视图

细化了对于权限的管理

<u>管理权限</u>分为三级：

student用户——借阅图书，归还图书，查看借阅记录

admin用户——增减图书，管理学生账号，查看管理日志

root用户——增减图书，管理学生账号，查看管理日志，增加或取消admin账号

<img src="C:\Users\马睿淳\Desktop\大二下\数据库\实验报告\adminView.PNG" width="70%" height="70%">

右上角的两个复选框分别选定搜索选项，管理模式。

管理模式——图书管理，学生账号管理，管理记录，admin账号管理(仅root)

不同的管理模式有不同的搜索选项

下端按钮给出了不同模式下的基本操作

#####图书管理

点击  *添加书籍*  会弹出对话框，填入书籍信息即完成书籍添加

单击选定单个书号，点击  *删除书记*  会删除指定书籍，如有学生正在借阅该书，需要二次确认，对应的借阅记录也会删除

管理员视图的表单支持**双击修改**，直接输入修改，点击  *提交修改*  按钮，修改将更新到数据库

点击  *撤销未提交修改*  ，放弃未提交修改

##### 学生账号管理

<img src="C:\Users\马睿淳\Desktop\大二下\数据库\实验报告\adminViewstu.PNG" width="70%" height="70%">

显示所有学生账号，提供按 学号或账号名查询

<u>选择账号</u>，可以删除学生账号，同时删除所有借阅记录

##### 管理日志

<img src="C:\Users\马睿淳\Desktop\大二下\数据库\实验报告\adminViewlog.PNG" width="70%" height="70%">

显示管理员操作日志，提供 书名，书号搜索选项，默认按操作序号排列。

出于保护记录的目的，不支持删除增加日志

##### admin账号管理（仅root用户）

<img src="C:\Users\马睿淳\Desktop\大二下\数据库\实验报告\adminViewadminManage.PNG" width="70%" height="70%">

显示所有管理员帐户，可以按账号或账号名查询

可以增加或删除管理员账号，实现了对于权限的管理

###数据库结构

有 BookInfo, User, User_Book, adminLog 四个表单，分别存储 图书信息，用户信息，借阅信息，管理日志

DDL如下

```sql lite
CREATE TABLE BookInfo
(
  BookName     VARCHAR(30) NOT NULL,
  BookId       CHAR(8)     NOT NULL
    PRIMARY KEY,
  Auth         VARCHAR(20) NOT NULL,
  Category     VARCHAR(10) DEFAULT NULL,
  Location     VARCHAR(10) DEFAULT NULL,
  Publisher    VARCHAR(30) DEFAULT NULL,
  PublishTime  DATE,
  Storage      INT         DEFAULT 0,
  NumCanBorrow INT         DEFAULT 0,
  CHECK (NumCanBorrow > 0),
  CHECK (Storage > 0),
  CHECK (Storage >= BookInfo.NumCanBorrow)
);

CREATE TABLE User
(
  Id      CHAR(10) NOT NULL
    UNIQUE,
  Name    VARCHAR(20),
  Pswd    CHAR(32) NOT NULL,
  IsAdmin BIT DEFAULT 0
);

CREATE TABLE User_Book
(
  StudentId   CHAR(10) NOT NULL
    REFERENCES User_Book (StudentId)
      ON UPDATE CASCADE
      ON DELETE CASCADE,
  BookId      CHAR(8)  NOT NULL
    REFERENCES BookInfo （BookId）
      ON UPDATE CASCADE
      ON DELETE CASCADE,
  BorrowTime  DATE,
  ReturnTime  DATE,
  BorrowState BIT DEFAULT 0,
  PRIMARY KEY (StudentId, BookId)
);

CREATE TABLE adminLog
(
  OP_Id     INT PRIMARY KEY ,
  BookId    CHAR(6)     NOT NULL,
  BookName  VARCHAR(20) NOT NULL,
  Time      DATE,
  BuyOrDrop BIT DEFAULT 0,
  Number    INT DEFAULT 0
);
```

BookInfo存储 （书号，书名，作者，分类，地点，出版社，出版时间，库存，剩余可借 ）信息

User存储 （账号，用户姓名，密码MD5，是否管理员）

User_book存储（账号，书号，借出时间，归还时间，是否归还）

adminLog存储（日志号，书号，书名，时间，购入OR淘汰，数量）

定义了User_Book的外键是User中的StudentId,BookInfo中的BookId,保证了参照完整性



### 具体实现

#### 数据库连接

使用PyQt自带的模块实现数据库连接

```python
 # 打开数据库连接
        Lib_db = QSqlDatabase.addDatabase("QSQLITE")#设置数据库类型
        Lib_db.setDatabaseName('Library_db.db')     #设置数据库名
        Lib_db.open()                                #打开数据库
        #操作
        #......
        Lib_db.close()                               #关闭数据库
```

####查询

PyQt提供了两种方式进行查询等操作，

1.直接执行sql语句，获取数据，

2.设置 数据库model，从model获取数据库数据，model直接与QtableView连接显示

方式二更加便于表单展示

```python
#方式一
        Lib_db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM user WHERE Id='%s'" % (id) #sql语句
        query.exec_(sql) #执行sql语句
        if (query.value(3) == 1):  # 获取数据
            self.is_admin_signal.emit(id)
        else:
            self.is_student_signal.emit(id)
            
#方式二      
        self.Lib_db = QSqlDatabase.addDatabase('QSQLITE') #设置数据库类型
        self.Lib_db.setDatabaseName('Library_db.db')      #设置数据库名
        self.Lib_db.open()                                #打开数据库
      
        self.queryModel = QSqlTableModel(db=self.Lib_db)  #设置表单Model
        self.queryModel.setTable("BookInfo")              #设置要查询的表
        self.queryModel.select()                          #执行查询
        self.queryModel.setEditStrategy(QSqlTableModel.OnManualSubmit)  #设置修改策略
        
        optionList = ['BookName', 'BookId', 'Auth', 'Category', 'Publisher']
        searchOption = optionList[self.combobox_search.currentIndex()]
        condition = self.lineEdit_search.text()

        self.tableView.setModel(self.queryModel) #将界面与Model连接
        
        if condition == '':
            self.queryModel.setFilter("") 
        else:
            condition = '%' + condition + '%'
            sql = "%s LIKE '%s' ORDER BY '%s';" % (
                searchOption, condition, searchOption) # 设置sql语句
            self.queryModel.setFilter(sql) #设置Filter，相当于WHERE后的内容
                                           #设置完成表单显示相应内容
```

####更改

以学生借阅图书为例

```python
tempQuery = QSqlQuery(self.Lib_db)
sql = "UPDATE User_Book SET BorrowState = 1, BorrowTime = DATE('now') , ReturnTime = NULL             WHERE StudentId = '%s' AND BookId = '%s';" % (self.stu_id, borrow_id)
tempQuery.exec_(sql)
sql = "UPDATE BookInfo SET NumCanBorrow = NumCanBorrow-1 WHERE BookId = '%s';" % borrow_id
tempQuery.exec_(sql)
QMessageBox.information(self, "消息", "借阅成功", QMessageBox.Yes)
```

#### 删除

以管理员淘汰书为例

```python
  if curIndex == 0:
      del_id = self.queryModel.data(index[0], Qt.DisplayRole)
      if len(index) != 1 or index[0].column() != 1:
          QMessageBox.information(self, "提示", "请仅选择一个书号或账号~",                                                        QMessageBox.Yes,QMessageBox.Yes)
          return
      sql = "SELECT * FROM BookInfo WHERE BookId == '%s'" % del_id
      tempQuery.exec_(sql)
      tempQuery.first()
      if tempQuery.value(7) != tempQuery.value(8):
          msgBox = QMessageBox.question(self, "是否确认？", "该书仍有同学借阅！",                                            QMessageBox.Yes| QMessageBox.No,QMessageBox.No)
          if msgBox == QMessageBox.No:
              return
      BookName = tempQuery.value(0)
      Num = tempQuery.value(7)
      sql = "SELECT OP_Id FROM adminLog ORDER BY OP_Id DESC "
      tempQuery.exec_(sql)
      if tempQuery.first():
          Opid = tempQuery.value(0)+1
      else:
          Opid=1
      sql = "INSERT INTO adminLog VALUES (%d,'%s', '%s', Date('now'), 0, %d )" % 
                                                     /(Opid, del_id, BookName, Num)
      tempQuery.exec_(sql)
      sql = "DELETE FROM BookInfo WHERE BookId == '%s'" % del_id
      tempQuery.exec_(sql)
      # adminLog ????
  elif curIndex ==1:
      del_id = self.queryModel_User.data(index[0], Qt.DisplayRole)
      if len(index) != 1 or index[0].column() != 0:
          QMessageBox.information(self, "提示", "请仅选择一个用户Id~",                                                               QMessageBox.Yes,QMessageBox.Yes)
          return
      sql = "DELETE FROM User WHERE Id == '%s'" % del_id
      tempQuery.exec_(sql)
  elif curIndex ==2:
      pass
  elif curIndex ==3:
      del_id = self.queryModel_User.data(index[0], Qt.DisplayRole)
      if len(index) != 1 or index[0].column() != 0:
          QMessageBox.information(self, "提示", "请仅选择一个账号~",                                                               QMessageBox.Yes,QMessageBox.Yes)
          return
      sql = "DELETE FROM User WHERE Id == '%s'" % del_id
      tempQuery.exec_(sql)

  QMessageBox.information(self,"完成", "删除完成", QMessageBox.Yes,QMessageBox.Yes)
```







