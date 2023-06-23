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
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True  # установка autocommit в True
    cur = conn.cursor()
    try:
        cur.execute(f'CREATE DATABASE {db_name}')
    except psycopg2.ProgrammingError:
        pass

    cur.close()
    conn.close()

    # try:
    #     conn = psycopg2.connect(dbname=db_name, **params)
    # except psycopg2.OperationalError as e:
    #     print(f"Unable to connect to database: {e}")
    # else:
    #     with conn.cursor() as cur:
    #         cur.execute("""
    #             CREATE TABLE IF NOT EXISTS companies (
    #                 company_id SERIAL PRIMARY KEY,
    #                 company_name VARCHAR(255) NOT NULL,
    #                 url TEXT
    #             )
    #         """)
    #     conn.commit()
    # finally:
    #     conn.close()

    with psycopg2.connect(dbname=db_name, **params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    url TEXT
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
    return random.sample(companies_data, 10)
