import hh_utils as utils
from config import config



def main():
    params = config()

    data = utils.get_companies_from_hh('63')
    random_10_companies = utils.get_10random_companies_data(data)
    utils.create_db('headhunter', params)
    utils.save_10random_companies_to_db(random_10_companies, 'headhunter', params)

    vacancies = utils.get_vacancies_from_hh(random_10_companies)
    utils.save_vacancies_to_db(vacancies)



if __name__ == '__main__':
    main()
