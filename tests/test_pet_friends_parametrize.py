import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def generate_string(num):  # генерация строки длиной num символов
    return "x" * num


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.fixture(autouse=True)
def get_api_key():
    # """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, pytest.key = pf.get_api_key(valid_email, valid_password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in pytest.key

    # yield

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    # assert pytest.status == 200


@pytest.mark.parametrize("filter",
                         [
                             generate_string(255),
                             generate_string(1001),
                             russian_chars(),
                             russian_chars().upper(),
                             chinese_chars(),
                             special_chars(),
                             123
                         ],
                         ids=
                         [
                             '255 symbols'
                             , 'more than 1000 symbols'
                             , 'russian'
                             , 'RUSSIAN'
                             , 'chinese'
                             , 'specials'
                             , 'digit'
                         ])
def test_get_all_pets_with_negative_filter(filter):
    """ Негативный тест проверка несуществующих фильтров"""
    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

    # Проверяем статус ответа
    assert pytest.status == 500


@pytest.mark.parametrize("filter",
                         ['', 'my_pets'],
                         ids=['empty string', 'only my pets'])
def test_get_all_pets_with_positive_key(filter):
    """ Позитивный тест проверка существующих фильтров"""
    pytest.status, result = pf.get_list_of_pets(pytest.key, filter)
    print(pytest.status)

    # Проверяем статус ответа
    assert pytest.status == 200
    assert len(result['pets']) > 0


@pytest.mark.parametrize("name"
    , ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
    , ['', generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
       special_chars(), '123']
    , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_add_new_pet_simple_positive(name, animal_type, age):
    """Проверяем, что можно добавить питомца с различными данными - 64 различных теста, декартово произведение"""

    # Добавляем питомца
    pytest.status, result = pf.add_new_pet_without_photo(pytest.key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                         ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                          russian_chars().upper(), chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1',
                              'specials', 'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple_negative(name, animal_type, age):
    # Добавляем питомца
    pytest.status, result = pf.add_new_pet_without_photo(pytest.key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 400