ukr_alphabet = [
    "А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З", "И", "І", "Ї", "Й",
    "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч",
    "Ш", "Щ", "Ь", "Ю", "Я"
]
ukr_order = {ch: i for i, ch in enumerate(ukr_alphabet)}

class Sort:
    
    @staticmethod
    def SortTable(table):
        sorted_table = sorted(
            table,
            key=lambda row: (ukr_order.get(row[0], 999), int(row[1]))  # 999 если буквы нет в алфавите
            )
        return sorted_table
    @staticmethod
    def SortLitera(list):
        list.sort(key=lambda x: ukr_order.get(x, 999))
        return list
       
