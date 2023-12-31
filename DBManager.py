import psycopg2
from config import config


class DBManager:
    """Класс для работы и подключения к БД"""

    def __init__(self, db_name: str = 'headhunter', params: dict = config()):
        self.__database_name = db_name
        self.__params = params
        self.__query_file = "queries.sql"

    def get_connection(self):
        params_with_db = self.__params.copy()
        params_with_db['dbname'] = self.__database_name
        return psycopg2.connect(**params_with_db)
        # return psycopg2.connect(self.__params)

    def execute_query(self, query_name, *args):
        connection = self.get_connection()
        cursor = connection.cursor()

        with open(self.__query_file, 'r', encoding='UTF-8') as file:
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
        query_name = "get_all_vacancies"
        return self.execute_query(query_name)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        query_name = "get_avg_salary"
        return self.execute_query(query_name)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query_name = "get_vacancies_with_higher_salary"
        return self.execute_query(query_name)

    def get_vacancies_with_keyword(self, *words: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        query_name = "get_vacancies_with_keyword"
        placeholders = tuple(['%' + word + '%' for word in words])
        return self.execute_query(query_name, placeholders)