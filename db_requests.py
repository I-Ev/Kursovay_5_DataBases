from DBManager import DBManager

dm = DBManager('headhunter')
# print(dm.get_all_vacancies())
print(dm.get_vacancies_with_keyword(['менеджер', 'продаж']))
