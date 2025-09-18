from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QComboBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator
from data.database import SQLiteDB
from models.databasestructure import DatabaseStructure

class DestroyAktWindow(QDialog):   
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
        self.setWindowTitle("Форма акту знищення")
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
        self.litnInput.setCurrentText(str(int(self.data.maxNumForLit(self.letterFilter.currentText()))+1))
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
        line_pib_layout.addWidget(QLabel("Прізвище:"))
        line_pib_layout.addWidget(self.lastnameInput)
        main_layout.addLayout(line_pib_layout)

        self.firstnameInput = QLineEdit()
        self.firstnameInput.setReadOnly(True)
        self.firstnameInput.minimumWidth = 200
        self.firstnameInput.maximumWidth = 200
        line_pib_layout.addWidget(QLabel("Ім'я:"))
        line_pib_layout.addWidget(self.firstnameInput)

        self.secondnameInput = QLineEdit()
        line_pib_layout.addWidget(QLabel("По батькові:"))
        self.secondnameInput.setReadOnly(True)
        self.secondnameInput.minimumWidth = 200
        self.secondnameInput.maximumWidth = 200
        line_pib_layout.addWidget(self.secondnameInput)
        
        # блок дати і номера акту знищення
        line_date_layout = QHBoxLayout()
        self.destroynumInput = QLineEdit()
        line_date_layout.addWidget(QLabel("Номер акту знищення:"))
        line_date_layout.addWidget(self.destroynumInput)    
        self.destrotdateInput = QDateEdit()
        self.destrotdateInput.setCalendarPopup(True)
        self.destrotdateInput.setDisplayFormat("dd.MM.yyyy")

        ddata=self.data.getAktDestroy(self.letterFilter.currentText(), self.litnInput.currentText())
        if ddata:
            self.destrotdateInput.setDate(QDate.fromString(ddata[1], "yyyy-MM-dd"))
            self.destroynumInput.setText(ddata[0])
        else:
            self.destrotdateInput.setDate(QDate.currentDate())

        self.destrotdateInput.setMaximumWidth(200)
        self.destrotdateInput.setMinimumWidth(200)
        line_date_layout.addWidget(QLabel("Дата акту знищення:"))
        line_date_layout.addWidget(self.destrotdateInput)
        main_layout.addLayout(line_date_layout)
        # кнопки ОК і Відміна
        line_button_layout = QHBoxLayout()
        self.deleteButton = QPushButton("Видалити акт знищення")
        self.deleteButton.clicked.connect(self.deleteButton_clicked)
        line_button_layout.addWidget(self.deleteButton)
        self.saveButton = QPushButton("Зберегти акт знищення")
        self.saveButton.clicked.connect(self.accept)
        line_button_layout.addWidget(self.saveButton)
        self.closeButton = QPushButton("Закрити")
        self.closeButton.clicked.connect(self.reject)
        line_button_layout.addWidget(self.closeButton)

        main_layout.addLayout(line_button_layout)

        self.leterFilter_changed()
        self.setLayout(main_layout)
    
    def deleteButton_clicked(self):
        self.data.deleteAktDestroy(self.letterFilter.currentText(), self.litnInput.currentText())
        self.fillForm()
    
    def accept(self):
        if self.destroynumInput.text().strip()!="":
                self.data.addAktDestroy(
                self.letterFilter.currentText(),
                self.litnInput.currentText(),
                self.destrotdateInput.date().toString("yyyy-MM-dd"),
                self.destroynumInput.text()
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
        akt=self.data.getAktDestroy(littera, self.litnInput.currentText())
        if akt:
            self.destroynumInput.setText(akt[1])
            if akt[0]:
                self.destrotdateInput.setDate(QDate.fromString(akt[0], "yyyy-MM-dd"))
            else:
                self.destrotdateInput.setDate(QDate.currentDate())
        else:
            self.destroynumInput.setText("")
            self.destrotdateInput.setDate(QDate.currentDate())
        
