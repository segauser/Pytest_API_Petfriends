import pytest
import requests
import json
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder
from settings import valid_email, valid_password, invalid_email, invalid_password
# python3 -m pytest test_pet_friends.py --collect-only

@pytest.fixture(autouse=True)  # setup and teardown
def time_delta_fixture():
    print('Замеряем время теста')
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print(f"Тест шел: {end_time - start_time}")


@pytest.fixture(scope='class')
def get_key():
    # переменные email и password нужно заменить своими учетными данными
    response = requests.get(url='https://petfriends.skillfactory.ru/api/key',
                            headers={"email": valid_email, "password": valid_password})
    assert response.status_code == 200, 'Запрос выполнен успешно'
    assert 'key' in response.text, 'В запросе передан ключ авторизации'
    result = ""
    try:
        result = response.json()
    except json.decoder.JSONDecodeError:
        result = response.text
    return result


@pytest.fixture()  # пользовательская фикстура получения питомцев
def get_my_pets_fixture(get_key, filter='my_pets'):
    headers = {'auth_key': get_key['key']}  # значение ключа из фикстуры
    filter = {'filter': filter}

    res = requests.get(url='https://petfriends.skillfactory.ru/api/pets', headers=headers, params=filter)
    status = res.status_code
    result = ""
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text

    assert status == 200
    assert len(result['pets']) > 0

    return result


@pytest.fixture()
def request_fixture(request):
    return(f'\n-----log------\
        \nНазвание фикстуры: {request.fixturename}\
        \nОбласть видимости фикстуры: {request.scope}\
        \nНазвание теста: {request.function.__name__}\
        \nКласс теста: {request.cls}\
        \nНазвание модуля теста: {request.module.__name__}\
        \nПуть к тестам: {request.fspath}\
        \n-----log------')


def get_test_case_docstring(item):
    """ Данная функция получает строку документа из тестового примера и форматирует ее,
        что бы показывать эту строку документа вместо имени тестового примера в отчетах.
    """

    full_name = ''

    if item._obj.__doc__:
        # Remove extra whitespaces from the doc string:
        name = str(item._obj.__doc__.split('.')[0]).strip()
        full_name = ' '.join(name.split())

        # Generate the list of parameters for parametrized test cases:
        if hasattr(item, 'callspec'):
            params = item.callspec.params

            res_keys = sorted([k for k in params])
            # Create List based on Dict:
            res = ['{0}_"{1}"'.format(k, params[k]) for k in res_keys]
            # Add dict with all parameters to the name of test case:
            full_name += ' Parameters ' + str(', '.join(res))
            full_name = full_name.replace(':', '')

    return full_name


def pytest_itemcollected(item):
    """ Данная функция изменяет имена тестовых случаев "on the fly" во время выполнения тест-кейсов.
    """

    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)

# pytest --collect-only test_labirint.py
def pytest_collection_finish(session):
    """ Данная функция изменяет имена тестовых случаев "on the fly",
        когда мы используем параметр --collect-only для pytest
        (чтобы получить полный список всех существующих тестов).
    """

    if session.config.option.collectonly is True:
        for item in session.items:
            # If test case has a doc string we need to modify it's name to
            # it's doc string to show human-readable reports and to
            # automatically import test cases to test management system.
            if item._obj.__doc__:
                full_name = get_test_case_docstring(item)
                print(full_name)

        pytest.exit('Выполнено!')