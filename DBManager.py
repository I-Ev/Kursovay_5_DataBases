import psycopg2
from config import config


class DBManager:
    """Класс для работы и подключения к БД"""

    def __init__(self, db_name: str = 'headhunter', params: dict = config()):
        self.database_name = db_name
        self.params = params
        self.query_file = "queries.sql"

    def get_connection(self):
        # return psycopg2.connect(self.database_name, **self.params)
        return psycopg2.connect(**self.params)

    def execute_query(self, query_name, *args):
        connection = self.get_connection()
        cursor = connection.cursor()

        with open(self.query_file, 'r', encoding='UTF-8') as file:
            queries = file.read().split(';')

        query = None
        for q in queries:
            if query_name in q:
                query = q.strip()

        if query:
            cursor.execute(query, args)
            result = cursor.fetchall()
        else:
            raise ValueError(f"Запрос '{query_name}' не найден в файле с запросами.")

        cursor.close()
        connection.close()

        return result

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        query_name = "get_companies_and_vacancies_count"
        return self.execute_query(query_name)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию"""
        pass

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        pass
