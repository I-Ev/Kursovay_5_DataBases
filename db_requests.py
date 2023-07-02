from DBManager import DBManager

dm = DBManager('headhunter')

print(dm.get_all_vacancies())
print(dm.get_companies_and_vacancies_count())
print(dm.get_avg_salary())
print(dm.get_vacancies_with_higher_salary())
print(dm.get_vacancies_with_keyword('Менеджер', 'помощник'))
