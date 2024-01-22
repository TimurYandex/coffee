import sqlite3
import sys
from itertools import product

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кофе")
        self.DATABASE = './coffee.sqlite'
        uic.loadUi('main.ui', self)
        conn = sqlite3.connect(self.DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM coffee')
        data = cursor.fetchall()
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for row_num, row_data in enumerate(data):
            for col_num, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_num, col_num, item)

        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())


def createbase():
    conn = sqlite3.connect('coffee.sqlite')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS coffee (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        variety_name TEXT,
                        degree_of_roasting TEXT,
                        ground_bean TEXT,
                        flavor_description TEXT,
                        price REAL,
                        package_volume INTEGER
                    )''')

    data1 = [['Arabica', 'Robusta', 'Colombian', 'Espresso', 'Decaf'],
             ['Medium', 'Dark', 'Light'],
             ['Ground', 'Whole bean'],
             ['Rich and smooth', 'Strong and bold', 'Nutty and fruity',
              'Intense and aromatic', 'Mild and balanced'],
             [5.99, 4.99, 6.99, 7.99, 6.49],
             [250, 500]]

    data = [line for line in product(*[data1[i] for i in range(6)])]

    cursor.executemany(
        '''INSERT INTO coffee (variety_name, degree_of_roasting, ground_bean, 
        flavor_description, price, 
        package_volume) VALUES (?, ?, ?, ?, ?, ?)''',
        data)

    conn.commit()
    conn.close()
