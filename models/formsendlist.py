from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QComboBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from PyQt5.QtGui import QIntValidator
from data.database import SQLiteDB
from models.databasestructure import DatabaseStructure
from models.formsend import FormSendWindow
from data.sort import Sort

class FormSendListWindow(QDialog):   # ❗ QDialog
    data: SQLiteDB
    def __init__(self, record=None):
        super().__init__()
        self.data = SQLiteDB("mydb.sqlite", DatabaseStructure)
        self.record = record
        self.initUI()

    def closeEvent(self, a0):
        self.data.close()
        return super().closeEvent(a0)

    def initUI(self):
        self.setWindowTitle("Список надісланих форм")
        self.setGeometry(150, 150, 900, 400)
        self.showMaximized()
        
        main_layout = QVBoxLayout()

        self.tabble = QTableWidget()
        self.tabble.setColumnCount(9)
        self.tabble.setHorizontalHeaderLabels(["Літера", "Номер форми", "Прізвище", "Ім'я", 
                                               "По батькові", "Номер реєстру", "Дата підпису", 
                                               "Отримано/Надіслано", "Установа"])
        #self.tabble.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Заборон
        header = self.tabble.horizontalHeader()
        header.setDefaultAlignment(Qt.Alignment(Qt.AlignCenter | Qt.AlignVCenter))  
        header.setFixedHeight(80)  # Встановлюємо висоту заголовка
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)  # Останній стовпець розтя
        self.tabble.setEditTriggers(QTableWidget.NoEditTriggers)  # Забороняємо редагування
        main_layout.addWidget(self.tabble)
        self.filltable()

        button_layout = QHBoxLayout()
        self.openButton = QPushButton("Відкрити форму")
        self.openButton.clicked.connect(self.open_form)
        button_layout.addWidget(self.openButton)

        self.addButton = QPushButton("Додати запис")
        self.addButton.clicked.connect(self.addBottonClicked)
        button_layout.addWidget(self.addButton)

        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def filltable(self):
        records = Sort.SortTable(self.data.getSendList())
        self.tabble.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data) if col_data is not None else "")
                item.setTextAlignment(Qt.Alignment(Qt.AlignCenter | Qt.AlignVCenter))
                self.tabble.setItem(row_idx, col_idx, item)
        self.tabble.resizeColumnsToContents()

    def open_form(self):
        selected_items = self.tabble.selectedItems()
        if not selected_items:
            return  # Нічого не вибрано

        selected_row = selected_items[0].row()
        lit = self.tabble.item(selected_row, 0).text()
        litnum = self.tabble.item(selected_row, 1).text()

        form_id = self.data.getFormID(lit, litnum)
        if form_id is None:
            return  # Форма не знайдена

        form_window = FormSendWindow()
        form_window.SetID(int(form_id))  # Передаємо ID форми
        form_window.mode = 1  # Режим редагування
        form_window.exec_()  # Відкриваємо вікно як модальне

    def addBottonClicked(self):
        form_window = FormSendWindow()
        form_window.mode = 0  # Режим додавання нового запису
        if form_window.exec_() == QDialog.Accepted:
            self.filltable()  # Оновлюємо таблицю після додавання нового запису
        