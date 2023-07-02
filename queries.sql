-- Запрос для получения списка всех компаний и количества вакансий
--get_companies_and_vacancies_count
SELECT c.company_name, COUNT(v.id) FROM companies c LEFT JOIN vacancy v ON c.company_id = v.company_id GROUP BY c.company_id;

-- Запрос для получения списка всех вакансий
--get_all_vacancies
SELECT * FROM vacancy LEFT JOIN companies ON vacancy.company_id = companies.company_id;

-- Запрос для получения средней зарплаты по вакансиям
--get_avg_salary
SELECT AVG(salary_to) FROM vacancy;

-- Запрос для получения списка вакансий с зарплатой выше средней
--get_vacancies_with_higher_salary
SELECT * FROM vacancy WHERE salary_to > (SELECT AVG(salary_to) FROM vacancy);

-- Запрос на получение списка всех вакансий, в названии которых содержатся переданные в метод слова
--get_vacancies_with_keyword
SELECT * FROM vacancy WHERE name ILIKE %s;