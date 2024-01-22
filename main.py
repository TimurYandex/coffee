import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, \
    QDialog


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle("Добавить/редактировать кофе")
        self.add_button.clicked.connect(self.add_coffee)
        self.edit_button.clicked.connect(self.edit_coffee)
        selected_row = parent.tableWidget.currentRow()
        coffee_id = parent.tableWidget.item(selected_row, 0).text()
        self.variety_name_input.setText(
            parent.tableWidget.item(selected_row, 1).text())
        self.degree_of_roasting_input.setText(
            parent.tableWidget.item(selected_row, 2).text())
        self.ground_bean_input.setText(
            parent.tableWidget.item(selected_row, 3).text())
        self.flavor_description_input.setText(
            parent.tableWidget.item(selected_row, 4).text())
        self.price_input.setText(
            parent.tableWidget.item(selected_row, 5).text())
        self.package_volume_input.setText(
            parent.tableWidget.item(selected_row, 6).text())

    def add_coffee(self):
        variety_name = self.variety_name_input.text()
        degree_of_roasting = self.degree_of_roasting_input.text()
        ground_bean = self.ground_bean_input.text()
        flavor_description = self.flavor_description_input.text()
        price = float(self.price_input.text())
        package_volume = int(self.package_volume_input.text())

        conn = sqlite3.connect(self.parent.DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            '''INSERT INTO coffee (variety_name, degree_of_roasting, 
            ground_bean, flavor_description, price, package_volume) 
            VALUES (?, ?, ?, ?, ?, ?)''',
            (variety_name, degree_of_roasting, ground_bean, flavor_description,
             price, package_volume))

        conn.commit()
        conn.close()

        self.accept()
        self.parent.data_update()

    def edit_coffee(self):
        variety_name = self.variety_name_input.text()
        degree_of_roasting = self.degree_of_roasting_input.text()
        ground_bean = self.ground_bean_input.text()
        flavor_description = self.flavor_description_input.text()
        price = float(self.price_input.text())
        package_volume = int(self.package_volume_input.text())

        conn = sqlite3.connect(self.parent.DATABASE)
        cursor = conn.cursor()

        selected_row = self.parent.tableWidget.currentRow()

        coffee_id = self.parent.tableWidget.item(selected_row, 0).text()

        cursor.execute(
            '''UPDATE coffee SET variety_name=?, degree_of_roasting=?, 
            ground_bean=?, flavor_description=?, price=?, package_volume=? 
            WHERE ID=?''', (variety_name, degree_of_roasting,
                            ground_bean, flavor_description,
                            price, package_volume, coffee_id))

        conn.commit()
        conn.close()

        self.accept()
        self.parent.data_update()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кофе")
        self.DATABASE = './coffee.sqlite'
        uic.loadUi('main.ui', self)
        self.data_update()
        self.add_button.clicked.connect(self.open_addEditCoffeeForm)

    def data_update(self):
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

    def open_addEditCoffeeForm(self):
        form = AddEditCoffeeForm(self)
        form.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())


def createbase():
    conn = sqlite3.connect('coffee.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE
        TABLE
        IF
        NOT
        EXISTS
        coffee(
            ID
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        variety_name
        TEXT,
        degree_of_roasting
        TEXT,
        ground_bean
        TEXT,
        flavor_description
        TEXT,
        price
        REAL,
        package_volume
        INTEGER
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
        '''
        INSERT
        INTO
        coffee(variety_name, degree_of_roasting, ground_bean,
               flavor_description, price,
               package_volume)
        VALUES(?, ?, ?, ?, ?, ?)''',
        data)

    conn.commit()
    conn.close()
