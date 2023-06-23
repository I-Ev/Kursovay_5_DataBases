


def main():

    get_my_companies_from_hh()
    create_db()
    save_my_companies_to_db()

    get_vacancies_from_hh()
    save_vacancies_to_db()



if __name__ == '__main__':
    main()
