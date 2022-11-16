import pytest
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from settings import valid_email, valid_password, invalid_email, invalid_password
import logging

LOGGER = logging.getLogger(__name__)

# _______<TASK>______
# как написать декоратор-логгирования?

"""Напишите декоратор, который будет логировать наши запросы в API тестах. Этим декоратором мы помечаем функции, 
которые отправляют запросы в тестируемое приложение.
После прохождения теста на жёстком диске появляется файл pytest.log, в котором две секции: в первой перечислены
заголовки запроса, параметры пути, параметры строки и тело запроса; во второй — код ответа, тело ответа.
"""

def log(res, test_name=''):
    LOGGER.info(f'\nНазвание теста: {test_name},\nЗаголовок запроса: {res.request.headers}, \nПараметр пути: {res.request.path_url}'
                f'\nПараметр строки: {res.request.path_url[res.request.path_url.find("?") + 1::]}'
                f'\nТело запроса: {res.request.body}')
    LOGGER.info(f'\nКод ответа: {res.status_code}, \nТело ответа: {json.dumps(res.json(), indent=4)},\n--------------')

# def log(func):
#     def wrapper():
#         print('\nПередаём test')
#         x = func()
#         print('Test вернул нам <class "requests.models.Response"> здесь мы напишем логику логирования ')
#         return x
#     return wrapper

# _______</TASK>______

# _______INFO______
# pytest tests/test_pet_friends_fixture.py -v -m "get_pets or add_info" for terminal users mark !!!!

class TestClassPets:
    """ Тестовый класс с логированием тестов и записью в pytest.log"""
    # отрабатывает только через запуск внутри Pycharm, через Terminal log не пишется

    @pytest.mark.get_pets
    def test_get_my_pets_with_valid_key(self, get_key, request, request_fixture, filter='my_pets'):
        headers = {'auth_key': get_key['key']}  # значение ключа из фикстуры
        filter = {'filter': filter}

        res = requests.get(url='https://petfriends.skillfactory.ru/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        test_name = request.function.__name__   # request фикстура библиотеки pytest
        log(res, test_name)

        assert status == 200
        assert len(result['pets']) > 0

        return res


    @pytest.mark.get_pets
    def test_get_all_pets_with_valid_key(self, get_key, request, filter=''):
        headers = {'auth_key': get_key['key']}  # значение ключа из фикстуры
        filter = {'filter': filter}

        res = requests.get(url='https://petfriends.skillfactory.ru/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        test_name = request.function.__name__
        log(res, test_name)

        assert status == 200
        assert len(result['pets']) > 0

    @pytest.mark.add_info
    def test_add_new_pet_without_photo(self, get_key, request, name='', animal_type='dog',
                                       age='4'):
        """Проверяем что можно добавить питомца с корректными данными без фото"""

        headers = {'auth_key': get_key['key']}  # значение ключа из фикстуры

        # Добавляем питомца
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(url='https://petfriends.skillfactory.ru/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        test_name = request.function.__name__
        log(res, test_name)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name

    @pytest.mark.add_info
    def test_successful_add_self_pet_photo(self, get_key, get_my_pets_fixture, pet_photo='images/dogTV.jpg'):
        """Проверяем возможность добавления фото для питомца"""

        # запрашиваем список своих питомцев
        my_pets = get_my_pets_fixture  # получение списка питомцев из фикстуры

        # Берём id первого питомца из списка и отправляем запрос на добавление фото
        pet_id = my_pets['pets'][0]['id']
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {'auth_key': get_key['key'], 'Content-Type': data.content_type}

        res = requests.post(url='https://petfriends.skillfactory.ru/api/pets/set_photo/' + pet_id, headers=headers,
                            data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        log(res)

        # Ещё раз запрашиваем список своих питомцев
        my_pets = get_my_pets_fixture

        # Проверяем что статус ответа равен 200 и в списке питомцев питомцев имя нашего обновляемого питомца
        assert status == 200
        assert result['name'] == my_pets['pets'][0]['name']

    @pytest.mark.delete_pets
    def test_successful_delete_self_pet(self, get_key, get_my_pets_fixture):
        """Проверяем возможность удаления питомца"""

        # Получаем ключ auth_key и запрашиваем список своих питомцев
        headers = {'auth_key': get_key['key']}  # значение ключа из фикстуры
        my_pets = get_my_pets_fixture  # получение списка питомцев из фикстуры

        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']

        res = requests.delete(url='https://petfriends.skillfactory.ru/api/pets/' + pet_id, headers=headers)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        # Ещё раз запрашиваем список своих питомцев
        my_pets = get_my_pets_fixture

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()


@pytest.mark.skip(reason="Несуществующий пользователь")
def test_get_api_key_for_invalid_user(get_key):
    """ Проверяем что запрос api ключа возвращает статус 403 при передаче несуществующего юзера"""

    response = requests.get(url='https://petfriends.skillfactory.ru/api/key',
                            headers={"email": invalid_email, "password": invalid_password})
    assert response.status_code == 403


@pytest.mark.delete_pets
@pytest.mark.xfail(reason="Ожидаем ошибку 400 несуществующий питомец")
def test_delete_self_pet_with_invalid_pet_id(get_key, get_my_pets_fixture):
    """Проверяем возможность удаления питомца c несуществующим id"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    headers = {'auth_key': get_key['key']}  # значение ключа из фикстуры
    my_pets = get_my_pets_fixture  # получение списка питомцев из фикстуры

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']

    # Берём id первого питомца из списка, переворачиваем id и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id'][::-1]
    res = requests.delete(url='https://petfriends.skillfactory.ru/api/pets/' + pet_id, headers=headers)
    status = res.status_code

    # Проверяем что статус ответа равен 400 - неверный id
    assert status == 400
