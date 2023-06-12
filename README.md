# Содержание
1. Описание
2. Документация по установке и запуску
3. Документация по API
---
## Описание
Это сайт, где вы сможете выкладывать шаблоны и проекты на общее обозрение.
Здесь вы также сможете поставить цену за доступ к вашему исходному коду проекта, 
или найти другие проекты и шаблоны.
Его можно поситить по этой ссылке: https://evanescent-invented-basketball.glitch.me/

---
## Документация по установке и запуску
1. Для начала склонируйте проект: ```git clone https://github.com/Charlies-Kvit/Flask-project```
2. Запустите скрипт start.sh: ```./start.sh```. Если выскакивает permission denied - попробуйте `chmod +x start.sh` а затем снова запустить

Если хотите, можете это сделать в виртуальной среде, но с этим разбирайтесь [здесь](https://python.ivan-shamaev.ru/python-virtual-env-packages-virtualenv-venv-requirements-txt/#:~:text=Venv%20%2D%D1%8D%D1%82%D0%BE%20%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%2C%20%D0%BF%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D1%8F%D0%B5%D0%BC%D1%8B%D0%B9%20%D1%81,%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2%2C%20%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8B%D1%85%20%D0%B2%20%D0%B4%D1%80%D1%83%D0%B3%D0%B8%D1%85%20%D1%81%D1%80%D0%B5%D0%B4%D0%B0%D1%85).

Всё!

---
## Документация по API
your_key - ключ, его можно получить только лично у разрабов
### Что касается пользователей:
#### Для получения данных всех пользователей:
```text
GET
http://URL/api/users/your_key
```
Пример ответа:
```json
{
  "users": [
    {
      "date_change": "2023-04-21 18:31:53",
      "date_create": "2023-04-21 18:31:53",
      "email": "aaaaa@gmail.com",
      "id": 1,
      "login": "popgdser",
      "name": "Артем",
      "surname": "Лебедев"
    },
    {
      "date_change": "2023-04-21 21:11:29",
      "date_create": "2023-04-21 20:42:19",
      "email": "ame@gmail.com",
      "id": 2,
      "login": "Popgdse",
      "name": "Рома",
      "surname": "Еськин"
    },
    {
      "date_change": "2023-04-22 23:24:06",
      "date_create": "2023-04-22 21:21:42",
      "email": "ma@mail.ru",
      "id": 3,
      "login": "Charlies_Kviter",
      "name": "Александр",
      "surname": "Гутор"
    }
  ]
}
```
#### Для получения данных одного пользователя:
```text
GET
http://URL/api/users/<id>/your_key
```
Пример ответа на запрос ```http://URL/api/users/1``` :

```json
{
  "user": {
      "date_change": "2023-04-21 18:31:53",
      "date_create": "2023-04-21 18:31:53",
      "email": "aaaaa@gmail.com",
      "id": 1,
      "login": "popgdser",
      "name": "Артем",
      "surname": "Лебедев"
      "img": "../static/img/default.png"
    }
}
```
#### Для добавления данных нового пользователя:
POST запрос должен содержать json!!!
```text
POST
http://URL/api/users/your_key
```
JSON:
```json
{
  "login": "your_login", 
  "email": "your_email", 
  "surname": "your_surname", 
  "name": "your_name", 
  "password": "your_password"
  "img": "Путь к фалу на сервере"
}
```
Все поля обязательны!!! \
Ответ:
```json
{"success": "OK"}
```
#### Для изменения данных пользователя:
PUT запрос должен содержать json!!!
```text
PUT
http://URL/api/users/your_key
```
JSON:
```json
{
  "login": "your_login", 
  "email": "your_email", 
  "surname": "your_surname", 
  "name": "your_name"
}
```
Все поля обязательны!!! \
Ответ:
```json
{"success": "OK"}
```
#### Для удаления пользователя:
```text
DELETE
http://URL/api/users/<id>/your_key
```
Ответ:
```json
{"success": "OK"}
```
---
### Теперь что касается постов:
#### Для получения данных всех постов:
```text
GET
http://URL/api/posts/your_key
```
Пример ответа на запрос ```http://URL/api/posts```:
```json
{
  "posts": [
    {
      "created_date": "2023-04-25 20:29:13",
      "tags": "", 
      "img": "", 
      "title": "Это первый нормальный пост!",
      "user_id": 1,
      "id": 1,
      "content": "Э"
    },
    {
      "created_date": "2023-04-25 20:31:25", 
      "tags": "Free",
      "img": "https://i.imgur.com/D4CIMOG.jpeg", 
      "title": "Это действительно первый нормальный пост", 
      "user_id": 1, "id": 2, "content": "это действиетльно нормальный пост"
    },
    {
      "created_date": "2023-04-26 19:49:54", 
      "tags": "dsadasdasdasdasd", 
      "img": "sdasdasdasdasdasd", 
      "title": "asasdasdasdasd", 
      "user_id": 1, 
      "id": 3, 
      "content": "sdasdasdasdasdasd"
    }
  ]
}
```
#### Для получения данных одного пользователя:
```text
GET
http://URL/api/post/<id>/your_key
```
Пример ответа на запрос ```http://URL/api/posts/1```
```json
{
  "post": {
    "created_date": "2023-04-25 20:29:13",
    "tags": "", 
    "img": "", 
    "title": "Это первый нормальный пост!",
    "user_id": 1,
    "id": 1,
    "content": "Э"
  }
}
```
#### Для добавления нового поста:
POST запрос должен содержать json!!!
```text
POST
http://URL/api/posts/your_key
```
JSON:
```json
{
  "title": "your_title", 
  "content": "your_content", 
  "is_private":  "True or False",
  "user_id": "id of the user who created the post"
}
```
Все поля обязательны!!!
Ответ:
```json
{"success": "OK"}
```
#### Для изменения данных поста:
PUT запрос должен содержать json!!!
```text
PUT
http://URL/api/posts/<id>/your_key
```
JSON:
```json
{
  "title": "your_title", 
  "content": "your_content", 
  "is_private":  "True or False"
}
```
Все поля обязательны!!!
Ответ:
```json
{"success": "OK"}
```
#### Для удаления поста:
```text
DELETE
http://URL/api/posts/<id>/your_key
```
Ответ:
```json
{"success": "OK"}
```
---
Это все, что касается работы с api на данный момент.
