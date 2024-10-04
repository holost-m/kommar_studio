from database.methods import Users
from datetime import datetime
import openpyxl

class Exel_writer:
    @classmethod
    def write_to_excel(cls, data, file_name='service/users.xlsx'):


        head = ('id', 'telegram id', 'Имя', 'Фамилия', 'username', 'Ссылка', 'Дата входа', 'Время входа')

        # Создаем новую книгу и активный лист
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # обавили заголовок таблицы
        sheet.append(head)

        # Записываем данные в Excel
        for row in data:
            datetime1 = datetime.fromisoformat(row[-1])
            date1 = datetime1.date().strftime("%d.%m.%Y")
            time1 = datetime1.time().strftime("%H:%M")

            row = row[:-1] + (date1, time1)

            sheet.append(row)

        # Настраиваем ширину колонок
        sheet.column_dimensions['A'].width = 8
        sheet.column_dimensions['B'].width = 15
        sheet.column_dimensions['C'].width = 20
        sheet.column_dimensions['D'].width = 20
        sheet.column_dimensions['E'].width = 30
        sheet.column_dimensions['F'].width = 35
        sheet.column_dimensions['G'].width = 14
        sheet.column_dimensions['H'].width = 14


        # Сохраняем файл, перезаписывая его
        workbook.save(file_name)

