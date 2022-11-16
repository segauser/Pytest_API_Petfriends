## Тестирование API Petfriends. Тестовый проект SkillFactory курса QA Python

#### Реализация и тестирование методовов API посредством библиотеки Pytest
#### Реализация методов API при помощи Postman. Импорт коллекций в папке postman_api 
#### Запуск некоторых TestSuite из файла tests/test_suite_pet_friends.py
#### Запуск отдельных TestCase из файла tests/test_pet_friends.py
#### Запуск отдельных TestCase из файла tests/test_pet_friends_fixture.py с использованием фикстур
#### Запуск отдельных TestCase из файла tests/test_pet_friends_parametrize.py с использованием параметризации

Для тестирования необходим:
----------------

1) #### Импорт зависимостей из requirements.txt:

    ```bash
    pip install -r requirements
    ```
2) #### Команда для запуска тестов:

    ```bash
    python -m pytest tests/test_suite_pet_friends.py
    ```
   
Описание каталога:
----------------
1) #### В директории /tests располагаются файлы с тестами

2) #### В директории /tests/images лежат картинки для теста добавления питомца и теста добавления отдельного изображения

3) #### В корневой директории лежит файл settings.py - содержит информацию о валидном логине и пароле, тестовых данных

4) #### В корневой директории лежит файл api.py, который является библиотекой к REST api сервису веб приложения Pet Friends https://petfriends.skillfactory.ru/
    ###### Ссылка на документацию Swager https://petfriends.skillfactory.ru/apidocs/

5) #### Библиотека api написана в классе, что соответствует принципам ООП и позволяет удобно пользоваться её методами.

6) #### При инициализации библиотеки объявляется переменная base_url которая используется при формировании url для запроса.

7) #### Методы имеют подробное описание. Тесты проверяют работу методов используя api библиотеку.

8) #### Файл conftest.py содержит фикстуры и функции для удобного вывода в консоль структуры описания тестов используя команду
    ```bash
    python -m pytest --collect-only
    ```
   
Дополнительно:
----------------

1) #### Ссылка на тест-сьюты и чек-лист по тестированию API оформленное в Excel 
###### https://docs.google.com/spreadsheets/d/1v7LG02N4ls31cQPPYjxevALCaf8hS-Nk/edit?usp=sharing&ouid=102433908555400589633&rtpof=true&sd=true
2) #### Пример тест дизайна для GET и POST запросов в MindMup 2.0 for Google Drive нужно подтвердить доступ к своему Google Drive 
###### https://drive.google.com/file/d/1XWKS8JerpHQPFmK5MqFbccQyI_uEPKKT/view?usp=sharing
3) #### Ссылка на чек-лист, тест-кейсы и баг-репорт по функциональному тестированию сайта PetFriends http://130.193.37.179/app/pets
###### https://docs.google.com/spreadsheets/d/1X7xB6zIuukiBnJcR33F1jRXPdWHfzCgk/edit?usp=sharing&ouid=102433908555400589633&rtpof=true&sd=true