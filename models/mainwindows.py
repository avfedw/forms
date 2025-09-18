from PyQt5.QtWidgets import QApplication, QDialog, QDateEdit, QComboBox, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QStyle, QHeaderView
from PyQt5.QtCore import QDate, Qt, QRect
from models.databasestructure import DatabaseStructure
from data.database import SQLiteDB
from models.formwindow import FormWindow
from models.destroy import DestroyAktWindow
from models.formsendlist import FormSendListWindow
from models.mails import MailWindow
from data.sort import Sort


class MainWindow(QWidget):

    DatabaseStructure = DatabaseStructure

    def __init__(self):
        super().__init__()
        self.data = SQLiteDB("mydb.sqlite", self.DatabaseStructure)
        #self.data.drop_error_tables("formdestroy")  
        self.setWindowTitle("Форми")
        self.init_ui()

    def closeEvent(self, a0):
        self.data.close()
        return super().closeEvent(a0)

    def __refresh__(self):
        self.fillTabble()  

    def init_ui(self):
        line_layout = QHBoxLayout()
        layout = QVBoxLayout()
        self.setGeometry(100, 100, 1700, 800)
        self.showMaximized()
        # Letter filter
        self.letterFilterLabel = QLabel("Фільтр по літері:")
        line_layout.addWidget(self.letterFilterLabel)
        self.letterFilter = QComboBox()
        self.letterFilter.setMaximumWidth(100)
        self.letterFilter.setMinimumWidth(100)
        self.letterFilter.addItems(["Всі", "А", "Б", "В", "Г", "Д", "Е", "Є", "Ж", "З", "И", "І", "Ї", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"   ])
        line_layout.addWidget(self.letterFilter)
        # Date filters
        self.minDateFilterLabel = QLabel("Фільтр по даті від:")
        line_layout.addWidget(self.minDateFilterLabel)

        self.minDateFilter = QDateEdit()
        self.minDateFilter.setCalendarPopup(True)
        self.minDateFilter.setDisplayFormat("dd.MM.yyyy")
        self.minDateFilter.setDate(QDate(2000, 1, 1))
        self.minDateFilter.setMaximumWidth(200)
        self.minDateFilter.setMinimumWidth(200)
        line_layout.addWidget(self.minDateFilter)

        self.maxDateFilterLabel = QLabel("до:")
        line_layout.addWidget(self.maxDateFilterLabel)

        self.maxDateFilter = QDateEdit()
        self.maxDateFilter.setCalendarPopup(True)
        self.maxDateFilter.setDisplayFormat("dd.MM.yyyy")
        self.maxDateFilter.setDate(QDate.currentDate())
        self.maxDateFilter.setMaximumWidth(200)
        self.maxDateFilter.setMinimumWidth(200)
        line_layout.addWidget(self.maxDateFilter)

        line_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(line_layout)


        self.tabble=QTableWidget(40,20)
        self.tabble.setHorizontalHeaderLabels([
            "Літера", "Номер\nформи", "Прізвище", "Ім'я", "По батькові", 
            "Дата\nзапиту", "Номер\nзапиту", "Дата\nвідповіді", "Номер\nвідповіді", 
            "Форма\nдопуску", "Дата\nнаказу", "Номер\nнаказу", "Надано/скасовано",
            "Установа",  "Отримано/надіслано", "Дата\nреєстрації", "Номер\nреєстрації",
            "Дата\nзнищення", "Номер\nнаказу","Примітка"
            ])
        
        header = self.tabble.horizontalHeader()
        header.setDefaultAlignment(Qt.Alignment(Qt.AlignCenter | Qt.AlignVCenter))  
        header.setFixedHeight(80)  # Встановлюємо висоту заголовка
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        self.tabble.setColumnWidth(0,10)   # Літера
        self.tabble.setColumnWidth(1,20)   # Номер форми
        self.fillTabble()
        self.tabble.setEditTriggers(QTableWidget.NoEditTriggers)  # Забороняємо редагування
        layout.addWidget(self.tabble)        

        buttonLayout = QHBoxLayout()

        self.buttonForm = QPushButton("Додати форму")
        self.buttonForm.clicked.connect(self.on_buttonForm_click)
        buttonLayout.addWidget(self.buttonForm)

        self.buttonMails = QPushButton("Додати лист про відправленн")
        self.buttonMails.clicked.connect(self.on_buttonSend_click)
        buttonLayout.addWidget(self.buttonMails)

        self.buttonSBU = QPushButton("Отримання допуску")
        self.buttonSBU.clicked.connect(self.on_buttonMail_click)
        buttonLayout.addWidget(self.buttonSBU)

        self.buttonAkts = QPushButton("Акти зніщення")
        self.buttonAkts.clicked.connect(self.on_buttonAkts_click)
        buttonLayout.addWidget(self.buttonAkts)

        self.buttonRefresh = QPushButton("Оновити") 
        self.buttonRefresh.clicked.connect(self.__refresh__)
        buttonLayout.addWidget(self.buttonRefresh)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        
    
    def fillTabble(self):
        row=0
        self.tabble.setRowCount(0)  # Очищаем таблицу перед заполнением
        table = Sort.SortTable(self.data.summary())
        #print("Table:", table)
        for row_data in table:
            self.tabble.insertRow(row)
            print(f'Row {row} data: {row_data}')
            self.tabble.setItem(row, 0, QTableWidgetItem(str(row_data[0])))  # Літера
            self.tabble.setItem(row, 1, QTableWidgetItem(str(row_data[1])))  # Номер форми
            self.tabble.setItem(row, 2, QTableWidgetItem(str(row_data[2])))  # Прізвище
            self.tabble.setItem(row, 3, QTableWidgetItem(str(row_data[3])))  # Ім'я
            self.tabble.setItem(row, 4, QTableWidgetItem(str(row_data[4])))  # По батькові
            self.tabble.setItem(row, 19, QTableWidgetItem(str(row_data[5])))  # Примітка
            self.tabble.setItem(row, 17, QTableWidgetItem(str(row_data[6]) if str(row_data[6])!='None' else ''))  # Дата знищення
            self.tabble.setItem(row, 18, QTableWidgetItem(str(row_data[7]) if str(row_data[7])!='None' else ''))  # Номер акту знищення
            self.tabble.setItem(row, 13, QTableWidgetItem(str(row_data[8]) if str(row_data[8])!='None' else ''))  # Установа
            self.tabble.setItem(row, 14, QTableWidgetItem(str(row_data[9]) if str(row_data[9])!='None' else ''))  # Отримано/надіслано
            self.tabble.setItem(row, 15, QTableWidgetItem(str(row_data[10]) if str(row_data[10])!='None' else ''))  # Дата реєстрації
            self.tabble.setItem(row, 16, QTableWidgetItem(str(row_data[11]) if str(row_data[11])!='None' else ''))  # Номер реєстрації
            self.tabble.setItem(row, 5, QTableWidgetItem(str(row_data[12]) if str(row_data[12])!='None' else ''))  # Дата запиту
            self.tabble.setItem(row, 6, QTableWidgetItem(str(row_data[13]) if str(row_data[13])!='None' else ''))  # Номер запиту
            self.tabble.setItem(row, 7, QTableWidgetItem(str(row_data[14]) if str(row_data[14])!='None' else ''))  # Дата відповіді
            self.tabble.setItem(row, 8, QTableWidgetItem(str(row_data[15]) if str(row_data[15])!='None' else ''))  # Номер відповіді
            self.tabble.setItem(row, 9, QTableWidgetItem(str(row_data[16]) if str(row_data[16])!='None' else ''))  # Форма допуску
            self.tabble.setItem(row, 10, QTableWidgetItem(str(row_data[17]) if str(row_data[17])!='None' else ''))  # Дата наказу
            self.tabble.setItem(row, 11, QTableWidgetItem(str(row_data[18]) if str(row_data[18])!='None' else ''))  # Номер наказу
            self.tabble.setItem(row, 12, QTableWidgetItem(str(row_data[19]) if str(row_data[19])!='None' else ''))  # Надано/скасовано

            for i in range(self.tabble.columnCount()):
                item = self.tabble.item(row, i)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)  # Центрируем текст в ячейке
            row += 1
        self.tabble.setRowCount(row)  # Устанавливаем количество строк в таблице

    def on_buttonForm_click(self):
        #self.label.setText("Button clicked!")
        formWindow = FormWindow()
        if formWindow.exec_() == QDialog.Accepted:
            pass

    def on_buttonAkts_click(self):
        destroyWindow = DestroyAktWindow()
        destroyWindow.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                destroyWindow.size(),
                self.frameGeometry()
            )
            )
        if destroyWindow.exec_() == QDialog.Accepted:
            pass

    def on_buttonSend_click(self):
        formSendWindow = FormSendListWindow()
        formSendWindow.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                formSendWindow.size(),
                self.frameGeometry()
            )
            )
        if formSendWindow.exec_() == QDialog.Accepted:
            pass
        
    def on_buttonMail_click(self):
        formMail = MailWindow()
        formMail.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                formMail.size(),
                self.frameGeometry()
            )
            )
        if formMail.exec_() == QDialog.Accepted:
            pass
        