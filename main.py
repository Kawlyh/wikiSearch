import sys
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import pandas as pd


# 窗口操作类
class MyPicture(QWidget):

    # 布局初始化
    def __init__(self):
        self.my_name = ""
        self.my_entity = ""
        self.w = QWidget()
        self.out1 = ""
        self.out2 = ""
        self.out3 = ""
        self.out4 = ""
        self.conn = pymysql.connect(
            user='root',  # 用户名
            password='970925',  # 密码：注意字符串形式
            host='localhost',  # 指定访问的服务器，本地服务器指定“localhost”，远程服务器指定服务器的ip地址
            database='wikilast',  # 数据库的名字
            port=3306,  # 指定端口号
            charset='utf8mb4',  # 数据库的编码方式
        )
        self.sql1 = ""
        self.sql2 = ""
        self.sql3 = ""
        self.sql4 = ""


        # window
        super(MyPicture, self).__init__()
        self.w.resize(900, 900)
        self.w.setWindowTitle("WikiSearch")
        # 输入名字
        self.edit1 = QLineEdit(self.w)
        self.edit1.setPlaceholderText("请输入name")
        self.edit1.setFixedSize(800, 40)
        self.edit1.move(50, 50)
        # 输入1的确认
        self.btn1 = QPushButton(self.w)
        self.btn1.setText("确定")
        self.btn1.move(750, 100)
        self.btn1.setFixedSize(90, 40)
        self.btn1.clicked.connect(self.getTextInput1)
        # 输入实体
        self.edit2 = QLineEdit(self.w)
        self.edit2.setPlaceholderText("请输入entity")
        self.edit2.setFixedSize(800, 40)
        self.edit2.move(50, 150)
        # 输入2的确认
        self.btn2 = QPushButton(self.w)
        self.btn2.setText("确定")
        self.btn2.move(750, 200)
        self.btn2.setFixedSize(90, 40)
        self.btn2.clicked.connect(self.getTextInput2)
        # 输出name匹配的所有实体
        self.label1 = QLabel(self.w)
        self.label1.setFixedSize(800, 100)
        self.label1.move(50, 300)
        self.label1.setStyleSheet("QLabel{background:white;}")
        # 输出entity所属所有先前类别
        self.label2 = QLabel(self.w)
        self.label2.setFixedSize(800, 100)
        self.label2.move(50, 450)
        self.label2.setStyleSheet("QLabel{background:white;}")
        # 输出entity共存的所有实体
        self.label3 = QLabel(self.w)
        self.label3.setFixedSize(800, 100)
        self.label3.move(50, 600)
        self.label3.setStyleSheet("QLabel{background:white;}")
        # 输出entity所有属性和语句
        self.label4 = QLabel(self.w)
        self.label4.setFixedSize(800, 100)
        self.label4.move(50, 750)
        self.label4.setStyleSheet("QLabel{background:white;}")

    # 获取文本输入框1的内容
    def getTextInput1(self):
        self.my_name = self.edit1.text()

        # 获得name的实体
        self.sql1 = "SELECT DISTINCT labels.eid,labels.`value` AS 'NAME',aliases.`value` AS 'ALIASES' FROM labels,aliases WHERE labels.`value` = '"+self.my_name+"' LIMIT 3"
        self.out1 = str(pd.read_sql(self.sql1, con=self.conn))
        self.label1.setText(self.out1)

    # 获取文本输入框2的内容
    def getTextInput2(self):
        self.my_entity = self.edit2.text()

        # 获得id的所属类别
        now_sql ="SELECT labels.`value`  FROM labels WHERE labels.eid = '" + self.my_entity + "' LIMIT 1"
        now_name = str(pd.read_sql(now_sql, con=self.conn)).split()[2]
        self.sql2 = "SELECT DISTINCT labels.`value`,labels.eid FROM labels WHERE labels.`value` LIKE '%"+now_name+"%' LIMIT 3"
        self.out2 = str(pd.read_sql(self.sql2, con=self.conn))
        self.label2.setText(self.out2)

        # 获得实体共存的实体
        self.sql3 = "SELECT DISTINCT refer.eid FROM statements,refer WHERE statements.eid = '" + self.my_entity + "'LIMIT 3"
        self.out3 = str(pd.read_sql(self.sql3, con=self.conn))
        self.label3.setText(self.out3)

        # 获得实体所有text
        self.sql4 = "SELECT DISTINCT text FROM statements,snak,monotext WHERE statements.eid = '" + self.my_entity + "' LIMIT 3"
        self.out4 = str(pd.read_sql(self.sql4, con=self.conn))
        self.label4.setText(self.out4)

    # 翻译输入的name


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my = MyPicture()
    my.w.show()
    sys.exit(app.exec_())
