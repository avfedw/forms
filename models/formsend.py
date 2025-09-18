from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QComboBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator
from data.database import SQLiteDB
from models.databasestructure import DatabaseStructure

class FormSendWindow(QDialog):   # ❗ QDialog
    n: int
    mode: int = 0 # 0 новий запис, 1 редагування
    # Переписати під декілька отримань та надіслань
    data: SQLiteDB
    def __init__(self, record=None):
        super().__init__()
        self.data = SQLiteDB("mydb.sqlite", DatabaseStructure)
        self.record = record
        self.initUI()
        

    def SetID(self, n: int):
        self.n = n

    def closeEvent(self, a0):
        self.data.close()
        return super().closeEvent(a0)

    def initUI(self):
        self.setWindowTitle("Отримані та надіслані форми")
        self.setGeometry(150, 150, 600, 400)
        
        main_layout = QVBoxLayout()
        
        # блок Літера і номер форми
        line_layout = QHBoxLayout()

        self.letterFilter = QComboBox()
        self.letterFilter.addItems(self.data.literlist())
        line_layout.addWidget(QLabel("Літера:"))
        line_layout.addWidget(self.letterFilter)

        # self.litnInput= QLineEdit()
        # line_layout.addWidget(QLabel("Номер форми:"))
        # line_layout.addWidget(self.litnInput)
        self.litnInput = QComboBox()
        self.litnInput.setEditable(True)
        self.litnInput.addItems([str(i) for i in range(1, int(self.data.maxNumForLit(self.letterFilter.currentText()))+1)])
        self.litnInput.setCurrentText(str(int(self.data.maxNumForLit(self.letterFilter.currentText()))))
        line_layout.addWidget(QLabel("Номер форми:"))
        line_layout.addWidget(self.litnInput)


        self.letterFilter.currentIndexChanged.connect(self.leterFilter_changed)
        self.litnInput.currentIndexChanged.connect(self.leternum_changed)
        main_layout.addLayout(line_layout)
        
        # блок ПІБ
        line_pib_layout = QHBoxLayout()
        self.lastnameInput = QLineEdit() 
        self.lastnameInput.setReadOnly(True)
        self.lastnameInput.minimumWidth = 200
        self.lastnameInput.maximumWidth = 200
        self.lastnameInput.setReadOnly(True)
        #self.lastnameInput.setDisabled(True)
        line_pib_layout.addWidget(QLabel("Прізвище:"))
        line_pib_layout.addWidget(self.lastnameInput)
        main_layout.addLayout(line_pib_layout)

        self.firstnameInput = QLineEdit()
        self.firstnameInput.setReadOnly(True)
        self.firstnameInput.minimumWidth = 200
        self.firstnameInput.maximumWidth = 200
        self.firstnameInput.setReadOnly(True)
        line_pib_layout.addWidget(QLabel("Ім'я:"))
        line_pib_layout.addWidget(self.firstnameInput)

        self.secondnameInput = QLineEdit()
        line_pib_layout.addWidget(QLabel("По батькові:"))
        self.secondnameInput.setReadOnly(True)
        self.secondnameInput.minimumWidth = 200
        self.secondnameInput.maximumWidth = 200
        self.secondnameInput.setReadOnly(True)
        line_pib_layout.addWidget(self.secondnameInput)
          
        line_date_layout = QHBoxLayout()
        self.ust=QLineEdit()
        line_date_layout.addWidget(QLabel("Установа:"))
        line_date_layout.addWidget(self.ust)
        self.send=QComboBox()
        self.send.addItems(["Отримано", "Надіслано"])
        line_date_layout.addWidget(QLabel("Отримано/надіслано:"))
        line_date_layout.addWidget(self.send)
        self.sendRegNumInput = QLineEdit()
        line_date_layout.addWidget(QLabel("Номер реєстру:"))
        line_date_layout.addWidget(self.sendRegNumInput)    
        self.sendRegDateInput = QDateEdit()
        self.sendRegDateInput.setCalendarPopup(True)
        self.sendRegDateInput.setDisplayFormat("dd.MM.yyyy")

        ddata=self.data.getSendReg(self.letterFilter.currentText(), self.litnInput.currentText())
        if ddata:
            self.sendRegDateInput.setDate(QDate.fromString(ddata[0], "yyyy-MM-dd"))
            self.sendRegNumInput.setText(ddata[1])
            self.ust.setText(ddata[2])
            if ddata[3] == "Отримано":
                self.send.setCurrentIndex(0)
            elif ddata[3] == "Надіслано":
                self.send.setCurrentIndex(1)
        else:
            self.sendRegDateInput.setDate(QDate.currentDate())

        self.sendRegDateInput.setMaximumWidth(200)
        self.sendRegDateInput.setMinimumWidth(200)
        line_date_layout.addWidget(QLabel("Дата підпису:"))
        line_date_layout.addWidget(self.sendRegDateInput)
        main_layout.addLayout(line_date_layout)
        # кнопки ОК і Відміна
        line_button_layout = QHBoxLayout()
        self.deleteButton = QPushButton("Видалити надсилання форми")
        self.deleteButton.clicked.connect(self.deleteButton_clicked)
        line_button_layout.addWidget(self.deleteButton)
        self.saveButton = QPushButton("Зберегти дані про надсилання")
        self.saveButton.clicked.connect(self.accept)
        line_button_layout.addWidget(self.saveButton)
        self.closeButton = QPushButton("Закрити")
        self.closeButton.clicked.connect(self.reject)
        line_button_layout.addWidget(self.closeButton)

        main_layout.addLayout(line_button_layout)

        self.leterFilter_changed()
        self.InitMode()
        self.setLayout(main_layout)

    def deleteButton_clicked(self):
        self.data.deleteSendReg(self.letterFilter.currentText(), self.litnInput.currentText())
        self.fillForm()
    
    def accept(self):
        if self.sendRegNumInput.text().strip()!="":
                self.data.addSendReg(
                self.letterFilter.currentText(),
                self.litnInput.currentText(),
                self.sendRegDateInput.date().toString("yyyy-MM-dd"),
                self.sendRegNumInput.text(),
                self.ust.text(),
                self.send.currentText()
            )
    
    def reject(self):
        return super().reject()
    
    def leterFilter_changed(self):
        self.litnInput.clear()
        self.litnInput.addItems([str(i) for i in range(1, int(self.data.maxNumForLit(self.letterFilter.currentText()))+1)])
        #self.litnInput.setCurrentText(str(int(self.data.maxNumForLit(self.letterFilter.currentText()))))
        self.litnInput.setCurrentIndex(0)
        self.fillForm()

    def leternum_changed(self):
        self.fillForm()

   
        
    def fillForm(self):
        littera = self.letterFilter.currentText()
        # Заповнюємо ПІБ, якщо є така форма
        pib = self.data.getForm(littera, self.litnInput.currentText())
        if pib:
            self.lastnameInput.setText(pib[0])
            self.firstnameInput.setText(pib[1])
            self.secondnameInput.setText(pib[2])
        else:
            self.lastnameInput.setText("")
            self.firstnameInput.setText("")
            self.secondnameInput.setText("")
        akt=self.data.getSendReg(littera, self.litnInput.currentText())
        if akt:
            self.sendRegNumInput.setText(akt[1])
            if akt[0]:
                self.sendRegDateInput.setDate(QDate.fromString(akt[0], "yyyy-MM-dd"))
            else:
                self.sendRegDateInput.setDate(QDate.currentDate())
            self.ust.setText(akt[2])
            if akt[3] == "Отримано":
                self.send.setCurrentIndex(0)
            elif akt[3] == "Надіслано":
                self.send.setCurrentIndex(1)
            
        else:
            self.sendRegNumInput.setText("")
            self.sendRegDateInput.setDate(QDate.currentDate())
            self.ust.setText("")
            self.send.setCurrentText("")

    def InitMode(self):
        if self.mode == 1: # режим редагування
            self.letterFilter.setEnabled(False)
            self.litnInput.setEnabled(False)
            self.letterFilter.setCurrentText(self.data.getFormLit(self.n))
            self.litnInput.setCurrentText(self.data.getFormLitNum(self.n))
            self.fillForm()
        elif self.mode == 0: # режим додавання нового запису
            self.letterFilter.setEnabled(True)
            self.litnInput.setEnabled(True)    
        
        