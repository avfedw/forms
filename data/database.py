import sqlite3
from models.databasestructure import DatabaseStructure
from data.sort import Sort

def isnullorempty(value):
    return value is None or value == ""


class SQLiteDB:
    def __init__(self, db_name: str, structure: dict):
        self.db_name = db_name
        self.structure = structure
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self._create_tables()

    def drop_error_tables(self, table: str):
        """Удаление таблицы (для отладки)"""
        sql = f"DROP TABLE IF EXISTS {table}"
        self.cur.execute(sql)
        self.conn.commit()

    def _create_tables(self):
        """Создание таблиц по структуре"""
        for table, fields in self.structure.items():
            columns = []
            for field in fields:
                for name, ftype in field.items():
                    columns.append(f"{name} {ftype.upper()}")
            sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})"
            self.cur.execute(sql)
        self.conn.commit()

    def delete(self, table: str, condition: str, params: tuple = ()):
        """Удаление данных"""
        sql = f"DELETE FROM {table} WHERE {condition}"
        self.cur.execute(sql, params)
        self.conn.commit()

    def maxNumForLit(self, lit: str):
        sql = f'select max(litnum) from form where lit="{lit}"'
        self.cur.execute(sql)
        max_litnum = self.cur.fetchone()[0]
        if max_litnum is None:
            max_litnum = 0
        return max_litnum
    
    def addorEditForm(self, data: dict):
        # Убираем пустые значения
        data = {k: v for k, v in data.items() if not isnullorempty(v)}

        # Проверяем, есть ли запись с таким lit/litnum
        self.cur.execute("SELECT n FROM form WHERE lit=? AND litnum=?", (data["lit"], data["litnum"]))
        row = self.cur.fetchone()

        if row:
            # Обновляем существующую запись
            updates = ", ".join([f"{k}=?" for k in data if k not in ("lit", "litnum")])
            values = tuple(data[k] for k in data if k not in ("lit", "litnum"))
            sqlM = f"UPDATE form SET {updates} WHERE lit=? AND litnum=?"
            values += (data["lit"], data["litnum"])
        else:
            # Вставляем новую запись
            self.cur.execute("SELECT max(n) FROM form")
            max_id = self.cur.fetchone()[0] or 0
            data["n"] = max_id + 1

            keys = ", ".join(data.keys())
            placeholders = ", ".join(["?"] * len(data))
            values = tuple(data.values())
            sqlM = f"INSERT INTO form ({keys}) VALUES ({placeholders})"

        print("SQL:", sqlM)
        print("VALUES:", values)

        self.cur.execute(sqlM, values)
        self.conn.commit()

        # Для проверки: вывести последнюю запись
        self.cur.execute("SELECT * FROM form ORDER BY n DESC LIMIT 1")
        row = self.cur.fetchone()
        if row:
            print("✅ Сохранено:", row)
        else:
            print("⚠️ Записи не найдены")

    def summary(self):
        self.cur.execute("""SELECT lit,litnum,lastname,firstname,secondname,form.note, 
        d.destroydate,d.destroynum, 
        s.ust, s.senddirection,s.regdate,s.regnum,
        m.askdate,m.asknum,m.ansdate,m.ansnum,m.formacsess,m.nakazdate,m.nakaznum,m.nakazstatus
        FROM form left join formdestroy as d on form.n=d.formnum  
        left join formsend as s on form.n=s.formnum
        left join mails as m on form.n=m.formnum
        order by lit,litnum""")
        return self.cur.fetchall()
    
    def close(self):
        self.conn.close()

    def addAktDestroy(self, lit: str, litnum: str, destroydate: str, destroynum: str):
        # Убираем пустые значения
       

        # Проверяем, есть ли запись с таким formnum
        self.cur.execute(f"SELECT n FROM formdestroy WHERE formnum=(SELECT n FROM form WHERE lit='{lit}' AND litnum='{litnum}')")
        row = self.cur.fetchone()

        if row:
            # Обновляем существующую запись

            sqlM = f"UPDATE formdestroy SET destroydate = '{destroydate}',destroynum = '{destroynum}' WHERE n='{row[0]}'"
        else:
            # Вставляем новую запись
            self.cur.execute("SELECT max(n) FROM formdestroy")
            max_id = self.cur.fetchone()[0] or 0
            formid=self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' AND litnum='{litnum}'").fetchone()[0]
            sqlM = f"INSERT INTO formdestroy (n, formnum, destroydate, destroynum) VALUES ({max_id + 1}, {formid}, '{destroydate}', '{destroynum}')"
       

        self.cur.execute(sqlM)
        self.conn.commit()

        # Для проверки: вывести последнюю запись
        self.cur.execute("SELECT * FROM formdestroy ORDER BY n DESC LIMIT 1")
        row = self.cur.fetchone()
        if row:
            print("✅ Сохранено:", row)
        else:
            print("⚠️ Записи не найдены")
    
    def getAktDestroy(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        formid = self.cur.fetchone()
        if formid is None:
            return None
        formid = formid[0]
        self.cur.execute(f"SELECT destroydate, destroynum FROM formdestroy WHERE formnum='{formid}'")
        return self.cur.fetchone()
    
    def deleteAktDestroy(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        formid = self.cur.fetchone()
        if formid is None:
            return None
        formid = formid[0]
        self.cur.execute(f"DELETE FROM formdestroy WHERE formnum='{formid}'")
        self.conn.commit()

    def getSendReg(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        formid = self.cur.fetchone()
        if formid is None:
            return None
        formid = formid[0]
        self.cur.execute(f"SELECT regdate, regnum, ust, senddirection FROM formsend WHERE formnum='{formid}'")
        return self.cur.fetchone()
    
    def getSendList(self):
        self.cur.execute("""SELECT form.lit, form.litnum, form.lastname, form.firstname, form.secondname,
        formsend.regdate, formsend.regnum, formsend.ust, formsend.senddirection
        FROM formsend
        LEFT JOIN form ON form.n = formsend.formnum
        ORDER BY form.lit, form.litnum""")
        return self.cur.fetchall()

    def addSendReg(self, lit: str, litnum: str, regdate: str, regnum: str, ust: str, senddirection: str):
        # Проверяем, есть ли запись с таким formnum
        self.cur.execute(f"SELECT n FROM formsend WHERE formnum=(SELECT n FROM form WHERE lit='{lit}' AND litnum='{litnum}')")
        row = self.cur.fetchone()

        if row:
            # Обновляем существующую запись

            sqlM = f"UPDATE formsend SET regdate = '{regdate}',regnum = '{regnum}', ust = '{ust}', senddirection = '{senddirection}' WHERE n='{row[0]}'"
        else:
            # Вставляем новую запись
            self.cur.execute("SELECT max(n) FROM formsend")
            max_id = self.cur.fetchone()[0] or 0
            formid=self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' AND litnum='{litnum}'").fetchone()[0]
            sqlM = f"INSERT INTO formsend (n, formnum, regdate, regnum, ust, senddirection) VALUES ({max_id + 1}, {formid}, '{regdate}', '{regnum}', '{ust}', '{senddirection}')"
       

        self.cur.execute(sqlM)
        self.conn.commit()

        # Для проверки: вывести последнюю запись
        self.cur.execute("SELECT * FROM formsend ORDER BY n DESC LIMIT 1")
        row = self.cur.fetchone()
        if row:
            print("✅ Сохранено:", row)
        else:
            print("⚠️ Записи не найдены")

    def deleteSendReg(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        formid = self.cur.fetchone()
        if formid is None:
            return None
        formid = formid[0]
        self.cur.execute(f"DELETE FROM formsend WHERE formnum='{formid}'")
        self.conn.commit()

    def getMails(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        formid = self.cur.fetchone()
        if formid is None:
            return None
        formid = formid[0]
        self.cur.execute(f"SELECT askdate, asknum, ansdate, ansnum, formacsess, nakazdate, nakaznum, nakazstatus, note FROM mails WHERE formnum='{formid}'")
        return self.cur.fetchone()
    
    def addMails(self, lit: str, litnum: str, askdate: str, asknum: str, ansdate: str, ansnum: str, formacsess: int, nakazdate: str, nakaznum: str, nakazstatus: str, note: str):
        # Проверяем, есть ли запись с таким formnum
        self.cur.execute(f"SELECT n FROM mails WHERE formnum=(SELECT n FROM form WHERE lit='{lit}' AND litnum='{litnum}')")
        row = self.cur.fetchone()

        if row:
            # Обновляем существующую запись

            sqlM = f"""UPDATE mails SET askdate = '{askdate}',asknum = '{asknum}', ansdate = '{ansdate}', ansnum = '{ansnum}', 
            formacsess = {formacsess}, nakazdate = '{nakazdate}', nakaznum = '{nakaznum}', nakazstatus = '{nakazstatus}', note = '{note}' 
            WHERE n='{row[0]}'"""
        else:
            # Вставляем новую запись
            self.cur.execute("SELECT max(n) FROM mails")
            max_id = self.cur.fetchone()[0] or 0
            formid=self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' AND litnum='{litnum}'").fetchone()[0]
            sqlM = f"""INSERT INTO mails (n, formnum, askdate, asknum, ansdate, ansnum, formacsess, nakazdate, nakaznum, nakazstatus, note) 
            VALUES ({max_id + 1}, {formid}, '{askdate}', '{asknum}', '{ansdate}', '{ansnum}', {formacsess}, '{nakazdate}', '{nakaznum}', '{nakazstatus}', '{note}')"""
       

        self.cur.execute(sqlM)
        self.conn.commit()

        # Для проверки: вывести последнюю запись
        self.cur.execute("SELECT * FROM mails ORDER BY n DESC LIMIT 1")
        row = self.cur.fetchone()
        if row:
            print("✅ Сохранено:", row)
        else:
            print("⚠️ Записи не найдены")

    def deleteMails(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        formid = self.cur.fetchone()
        if formid is None:
            return None
        formid = formid[0]
        self.cur.execute(f"DELETE FROM mails WHERE formnum='{formid}'")
        self.conn.commit()

    def literlist(self):
        self.cur.execute("SELECT DISTINCT lit FROM form ORDER BY lit")
        return Sort.SortLitera([row[0] for row in self.cur.fetchall()])

    def getForm(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT firstname, secondname, lastname FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        return self.cur.fetchone()

    def getFormID(self, lit: str, litnum: str):
        self.cur.execute(f"SELECT n FROM form WHERE lit='{lit}' and litnum='{litnum}'")
        formid = self.cur.fetchone()
        if formid is None:
            return None
        return formid[0]

    
   