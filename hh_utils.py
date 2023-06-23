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
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    conn.close()



def save_10random_companies_to_db(data: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Сохраняет 10 случайных компаний в БД"""
    return None
