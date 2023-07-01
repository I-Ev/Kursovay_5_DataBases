import hh_utils as utils
from config import config


def main():
    # задаем параметры подключения к БД через config.py
    params = config()

    # получаем список всех компаний по ID региона, по дефолту Москва (id = 1)
    data = utils.get_companies_from_hh()

    # выбираем из списка 10 случайных компаний
    random_10_companies = utils.get_10random_companies_data(data)

    # создаем БД и таблицы
    utils.create_db('headhunter', params)

    # сохраняем 10 ранее выбранных компаний в БД
    utils.save_10random_companies_to_db(random_10_companies, 'headhunter', params)

    # получаем информацию о вакансиях по сохраненным 10 компаниям
    vacancies = utils.get_vacancies_from_hh(random_10_companies)

    # сохраняем вакансии в БД
    utils.save_vacancies_to_db(vacancies, 'headhunter', params)


if __name__ == '__main__':
    main()

