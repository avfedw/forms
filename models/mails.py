from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QComboBox, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIntValidator
from data.database import SQLiteDB
from models.databasestructure import DatabaseStructure


class MailWindow(QDialog):   # ❗ QDialog
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
        self.letterFilter.addItems(self.data.literlist())
        line_layout.addWidget(QLabel("Літера:"))
        line_layout.addWidget(self.letterFilter)

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
        line_p_layout = QHBoxLayout()
        self.lastnameInput = QLineEdit() 
        self.lastnameInput.minimumWidth = 400
        self.lastnameInput.maximumWidth = 400
        self.lastnameInput.setReadOnly(True)
        line_p_layout.addWidget(QLabel("Прізвище:"))
        line_p_layout.addWidget(self.lastnameInput)
        main_layout.addLayout(line_p_layout)

        line_i_layout = QHBoxLayout()
        self.firstnameInput = QLineEdit()
        self.firstnameInput.minimumWidth = 400
        self.firstnameInput.maximumWidth = 400
        line_i_layout.addWidget(QLabel("Ім'я:"))
        self.firstnameInput.setReadOnly(True)
        line_i_layout.addWidget(self.firstnameInput)
        main_layout.addLayout(line_i_layout)

        line_b_layout = QHBoxLayout()
        self.secondnameInput = QLineEdit()
        self.secondnameInput.setReadOnly(True)
        line_b_layout.addWidget(QLabel("По батькові:"))
        self.secondnameInput.minimumWidth = 400
        self.secondnameInput.maximumWidth = 400
        line_b_layout.addWidget(self.secondnameInput)
        main_layout.addLayout(line_b_layout)

        line_acsess_layout = QHBoxLayout()
        self.accessInput = QComboBox()
        self.accessInput.addItems(['Ф1 ("ОВ", "ЦТ", "Т")', 'Ф2 ("ЦТ", "Т")', 'Ф3 ("Т")'])
        line_acsess_layout.addWidget(QLabel("Форма допуску:"))
        line_acsess_layout.addWidget(self.accessInput)
        self.accessInput.setCurrentIndex(2)  # За замовчуванням "Ф3 ("Т")"
        self.accessStatus=QComboBox()
        self.accessStatus.addItems(['Надано', 'Скасовано'])
        line_acsess_layout.addWidget(self.accessStatus)
        self.accessStatus.setCurrentIndex(0)  # За замовчуванням "Надано"
        main_layout.addLayout(line_acsess_layout)

        line_mail_layout = QHBoxLayout()
        self.mailInput = QLineEdit()
        self.mailInput.minimumWidth = 400
        self.mailInput.maximumWidth = 400
        line_mail_layout.addWidget(QLabel("Номер листа до СБУ"))
        line_mail_layout.addWidget(self.mailInput)
        self.mailDateInput = QDateEdit()
        self.mailDateInput.setCalendarPopup(True)
        self.mailDateInput.setDisplayFormat("dd.MM.yyyy")
        self.mailDateInput.setDate(QDate.currentDate())
        line_mail_layout.addWidget(QLabel("Дата листа до СБУ"))
        line_mail_layout.addWidget(self.mailDateInput)
        main_layout.addLayout(line_mail_layout)

        line_ansver_layout = QHBoxLayout()
        self.ansverInput = QLineEdit()
        self.ansverInput.minimumWidth = 400
        self.ansverInput.maximumWidth = 400
        line_ansver_layout.addWidget(QLabel("Номер відповіді від СБУ"))
        line_ansver_layout.addWidget(self.ansverInput)
        self.ansverDateInput = QDateEdit()
        self.ansverDateInput.setCalendarPopup(True)
        self.ansverDateInput.setDisplayFormat("dd.MM.yyyy")
        self.ansverDateInput.setDate(QDate.currentDate())
        line_ansver_layout.addWidget(QLabel("Дата відповіді від СБУ"))
        line_ansver_layout.addWidget(self.ansverDateInput)
        main_layout.addLayout(line_ansver_layout)

        line_order_layout = QHBoxLayout()
        self.orderInput = QLineEdit()
        self.orderInput.minimumWidth = 400
        self.orderInput.maximumWidth = 400
        line_order_layout.addWidget(QLabel("Номер наказу на допуск"))
        line_order_layout.addWidget(self.orderInput)
        self.orderDateInput = QDateEdit()
        self.orderDateInput.setCalendarPopup(True)
        self.orderDateInput.setDisplayFormat("dd.MM.yyyy")
        self.orderDateInput.setDate(QDate.currentDate())
        line_order_layout.addWidget(QLabel("Дата наказу на допуск"))
        line_order_layout.addWidget(self.orderDateInput)
        main_layout.addLayout(line_order_layout)

        self.noteInput = QLineEdit()
        note_layout = QHBoxLayout()
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
        self.fillForm()
    
    def leterFilter_changed(self):
        self.litnInput.clear()
        self.litnInput.addItems([str(i) for i in range(1, int(self.data.maxNumForLit(self.letterFilter.currentText()))+1)])
        #self.litnInput.setCurrentText(str(int(self.data.maxNumForLit(self.letterFilter.currentText()))))
        self.litnInput.setCurrentIndex(0)
        self.fillForm()

    def leternum_changed(self):
        self.fillForm()

    def accept(self):
        if self.mailInput.text().strip()!="":
                self.data.addMails(
                self.letterFilter.currentText(),
                self.litnInput.currentText(),
                self.mailInput.text(),
                self.mailDateInput.date().toString("yyyy-MM-dd"),
                self.ansverInput.text(),
                self.ansverDateInput.date().toString("yyyy-MM-dd"),
                self.accessInput.currentIndex()+1,
                self.orderInput.text(),
                self.orderDateInput.date().toString("yyyy-MM-dd"),
                self.accessStatus.currentText(),
                self.noteInput.text()
            )
        return super().accept()
    
    def reject(self):
        return super().reject()
        
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

        mail = self.data.getMails(littera, self.litnInput.currentText())
        if mail:
            self.mailInput.setText(mail[0])
            if mail[1]:
                self.mailDateInput.setDate(QDate.fromString(mail[1], "yyyy-MM-dd"))
            else:
                self.mailDateInput.setDate(QDate.currentDate())
            self.ansverInput.setText(mail[2])
            if mail[3]:
                self.ansverDateInput.setDate(QDate.fromString(mail[3], "yyyy-MM-dd"))
            else:
                self.ansverDateInput.setDate(QDate.currentDate())
            self.acceptInput.setCurentIndex(mail[4]-1)
            self.orderInput.setText(mail[5])
            if mail[6]:
                self.orderDateInput.setDate(QDate.fromString(mail[6], "yyyy-MM-dd"))
            else:
                self.orderDateInput.setDate(QDate.currentDate())
            if mail[7] == "Надано":
                self.accessStatus.setCurrentIndex(0)
            elif mail[7] == "Скасовано":
                self.accessStatus.setCurrentIndex(1)
            self.noteInput.setText(mail[8])
        # akt=self.data.getAktDestroy(littera, self.litnInput.currentText())
        # if akt:
        #     self.destroynumInput.setText(akt[1])
        #     if akt[0]:
        #         self.destrotdateInput.setDate(QDate.fromString(akt[0], "yyyy-MM-dd"))
        #     else:
        #         self.destrotdateInput.setDate(QDate.currentDate())
        # else:
        #     self.destroynumInput.setText("")
        #     self.destrotdateInput.setDate(QDate.currentDate())