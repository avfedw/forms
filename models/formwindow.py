from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QComboBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator
from data.database import SQLiteDB
from models.databasestructure import DatabaseStructure

class FormWindow(QDialog):   # ❗ QDialog
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
        self.setWindowTitle("Форма запису")
        self.setGeometry(150, 150, 900, 600)
        main_layout = QVBoxLayout()
        line_layout = QHBoxLayout()

        self.letterFilter = QComboBox()
        self.letterFilter.addItems(['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 
                                    'Ї', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 
                                    'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я'])
        line_layout.addWidget(QLabel("Літера:"))
        line_layout.addWidget(self.letterFilter)

        self.litnInput = QComboBox()
        self.litnInput.setEditable(True)
        self.litnInput.addItems([str(i) for i in range(1, int(self.data.maxNumForLit(self.letterFilter.currentText()))+2)])
        self.litnInput.setCurrentText(str(int(self.data.maxNumForLit(self.letterFilter.currentText()))+1))
        line_layout.addWidget(QLabel("Номер форми:"))
        line_layout.addWidget(self.litnInput)

        self.letterFilter.currentIndexChanged.connect(self.leterFilter_changed)
        self.litnInput.currentIndexChanged.connect(self.leternum_changed)
        main_layout.addLayout(line_layout)
        
        # блок ПІБ
        line_p_layout = QHBoxLayout()
        self.lastNameInput = QLineEdit() 
        self.lastNameInput.minimumWidth = 400
        self.lastNameInput.maximumWidth = 400
        line_p_layout.addWidget(QLabel("Прізвище:"))
        line_p_layout.addWidget(self.lastNameInput)
        main_layout.addLayout(line_p_layout)

        
        line_i_layout = QHBoxLayout()
        self.firstNameInput = QLineEdit()
        self.firstNameInput.minimumWidth = 400
        self.firstNameInput.maximumWidth = 400
        line_i_layout.addWidget(QLabel("Ім'я:"))
        line_i_layout.addWidget(self.firstNameInput)
        main_layout.addLayout(line_i_layout)

        line_b_layout = QHBoxLayout()
        self.secondNameInput = QLineEdit()
        line_b_layout.addWidget(QLabel("По батькові:"))
        self.secondNameInput.minimumWidth = 400
        self.secondNameInput.maximumWidth = 400
        line_b_layout.addWidget(self.secondNameInput)
        main_layout.addLayout(line_b_layout)

        note_layout = QHBoxLayout()
        self.noteInput = QLineEdit()
        note_layout.addWidget(QLabel("Примітка:"))
        note_layout.addWidget(self.noteInput)
        main_layout.addLayout(note_layout)
        
        # … остальные поля …
        line_layout = QHBoxLayout()
        buttonSave = QPushButton("Зберегти")
        buttonSave.clicked.connect(self.accept)  # Закрити діалог з результатом Accepted
        buttonCancel = QPushButton("Відміна")
        buttonCancel.clicked.connect(self.reject)  # Закрити діалог з результатом Rejected
        line_layout.addWidget(buttonSave)
        line_layout.addWidget(buttonCancel)
        main_layout.addLayout(line_layout)

        self.setLayout(main_layout)
    
    def leterFilter_changed(self):
        self.litnInput.clear()
        self.litnInput.addItems([str(i) for i in range(1, int(self.data.maxNumForLit(self.letterFilter.currentText()))+2)])
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
            self.lastNameInput.setText(pib[0])
            self.firstNameInput.setText(pib[1])
            self.secondNameInput.setText(pib[2])
        else:
            self.lastNameInput.setText("")
            self.firstNameInput.setText("")
            self.secondNameInput.setText("")
       
        self.litnInput.setValidator(QIntValidator(0, int(self.data.maxNumForLit(self.letterFilter.currentText()))+2))
        #self.litnInput.setText(str(int(self.data.maxNumForLit(self.letterFilter.currentText()))+1))
    
    def accept(self):
        self.data.addorEditForm({
            "lit": self.letterFilter.currentText(),
            "litnum": int(self.litnInput.currentText()),
            "firstname": self.firstNameInput.text(),
            "secondname": self.secondNameInput.text(),
            "lastname": self.secondNameInput.text(),
            "note": self.noteInput.text()
        })
        return super().accept()
    
    def reject(self):
        return super().reject()
