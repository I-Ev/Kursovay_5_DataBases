import random
from typing import Any
import psycopg2
import requests


def get_companies_from_hh(area_id: str) -> list[dict[str, Any]]:
    """ Возвращает список с данными по компаниям"""
    # описание API https://api.hh.ru/openapi/redoc#tag/Rabotodatel/operation/get-employer-info

    url = 'https://api.hh.ru/employers'
    area = area_id  # 1 - Москва, 63- Саранск
    company_with_vacancies = True  # только те, у кого есть вакансии
    per_page = 100
    page = 0
    result = []

    while True:
        params = {
            'area': area,
            'only_with_vacancies': company_with_vacancies,
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, params=params)
        data = response.json()
        if 'items' in data:
            result.extend(data['items'])
            print(f'Успешно получены и сохранены данные со страницы {page}')

        if 'pages' not in data:
            print(f'Успешно получены и сохранены данные со страницы {page}\n'
                  f'Достигнут предел глубины возвращаемых результатов по API')
            break

        if data['pages'] - 1 == page:
            print('Все страницы получены')
            break
        page += 1
    return result


def create_db(db_name: str, params: dict) -> None:
    """ Создает БД и таблицы для хранения информации с сайта HH.ru"""

    # создаем саму БД
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True  # установка autocommit в True
    cur = conn.cursor()
    try:
        cur.execute(f'CREATE DATABASE {db_name}')
    except psycopg2.ProgrammingError:
        pass

    cur.close()
    conn.close()

    # создаем таблицу для хранения информации по компаниям
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    url TEXT
                )
            """)

    # создаем таблицу для хранения информации по вакансиям
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancy (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    area TEXT,
                    salary_from INT,
                    salary_to INT,
                    salary_currency CHAR(3),
                    is_gross BOOLEAN,
                    is_premium BOOLEAN,
                    type VARCHAR(255),
                    published_date DATE,
                    is_archived BOOLEAN,
                    requirement TEXT,
                    responsibility TEXT,
                    experience VARCHAR(255),
                    employment VARCHAR(255),
                    url TEXT,
                    company_id INT REFERENCES companies(company_id) NOT NULL
                    
                )
            """)


def save_10random_companies_to_db(data: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Сохраняет 10 случайных компаний в БД"""
    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for company in data:
                cur.execute("""
                    INSERT INTO companies (company_id, company_name, url)
                    VALUES (%s, %s, %s)
                    """, (company['id'], company['name'], company['url']))
            conn.commit()


def get_10random_companies_data(companies_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """ Случайно отбирает информацию по 10 компаниям из передаваемого списка"""
    if len(companies_data) < 10:
        return companies_data
    return random.sample(companies_data, 10)


def get_vacancies_from_hh(random_10_companies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """ Возвращает информацию о вакансиях, открытых в переданных на вход компаниях"""

    # описание API вакансий https://api.hh.ru/openapi/redoc#tag/Poisk-vakansij/operation/get-vacancies

    url = 'https://api.hh.ru/vacancies'
    employer_id = [id_empl['id'] for id_empl in random_10_companies]
    premium = True
    per_page = 20
    page = 0
    result = []

    while True:
        params = {
            'employer_id': employer_id,
            'premium': premium,
            'per_page': per_page,
            'page': page
        }
        response = requests.get(url, params=params)
        data = response.json()
        if 'items' in data:
            result.extend(data['items'])
            print(f'Успешно получены и сохранены данные со страницы {page}')

        if 'pages' not in data:
            print(f'Успешно получены и сохранены данные со страницы {page}\n'
                  f'Достигнут предел глубины возвращаемых результатов по API')
            break

        if data['pages'] - 1 == page:
            print('Все страницы получены')
            break
        page += 1
    return result



def save_vacancies_to_db(vacancies: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """ Осуществляет сохранение в БД данных о вакансиях"""

    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            for vanancy in vacancies:
                cur.execute("""
                    INSERT INTO vacancy (id, 
                    name,
                    area,
                    salary_from,
                    salary_to,
                    salary_currency,
                    is_gross,
                    is_premium,
                    type,
                    published_date,
                    is_archived,
                    requirement,
                    responsibility,
                    experience,
                    employment,
                    url,
                    company_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (vanancy['id'], vanancy['name'], vanancy['area']['name'], vanancy['salary']['from'], vanancy['salary']['to'],
                          vanancy['salary']['currency'], vanancy['salary']['gross'], vanancy['premium'], vanancy['type']['name'],
                          vanancy['published_at'], vanancy['archived'], vanancy['snippet']['requirement'], vanancy['snippet']['responsibility'],
                          vanancy['experience']['name'], vanancy['employment']['name'], vanancy['alternate_url'], vanancy['employer']['id']))
            conn.commit()
            print('\nВакансии успешно сохранены в БД')