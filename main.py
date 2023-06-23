import hh_utils as utils
from config import config



def main():
    params = config()

    # utils.get_companies_from_hh('63')
    utils.create_db('HeadHunter', params)
    # utils.save_10random_companies_to_db(data, 'HeadHunter', params)

    # get_vacancies_from_hh()
    # save_vacancies_to_db()



if __name__ == '__main__':
    main()
