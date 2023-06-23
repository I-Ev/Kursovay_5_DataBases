import requests


def get_my_companies_from_hh():
    """ Возвращает список с данными по компаниям"""
    # описание API https://api.hh.ru/openapi/redoc#tag/Rabotodatel/operation/get-employer-info

    url = 'https://api.hh.ru/employers'
    area = '1' # 1 - Москва
    company_with_vacancies = True # только те, у кого есть вакансии
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





get_my_companies_from_hh()
