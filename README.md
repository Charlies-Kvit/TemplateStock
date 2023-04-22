# Содержание
1. Описание
2. Документация по установке и запуску
3. Документация по API
## Описание
Это сайт, где... Рома, доделай
## ///
## Документация по API
### Что касается пользователей:
#### Для получения данных всех пользователей:
```text
GET
http://URL/api/users
```
#### Для получения данных одного пользователя:
```text
GET
http://URL/api/users/<id>
```
#### Для добавления данных нового пользователя:
POST запрос должен содержать json!!!
```text
POST
http://URL/api/users
```
JSON:
```json
{"login": "your_login", "email": "your_email", "surname": "your_surname", 
 "name": "your_name", "password": "your_password"}
```
Все поля обязательны!!!
#### Для изменения данных пользователя:
PUT запрос должен содержать json!!!
```text
PUT
http://URL/api/users
```
JSON:
```json
{"login": "your_login", "email": "your_email", "surname": "your_surname", 
 "name": "your_name"}
```
Все поля обязательны!!!
#### Для удаления пользователя:
```text
DELETE
http://URL/api/users/<id>
```
### Теперь что касается постов:
#### Для получения данных всех постов:
```text
GET
http://URL/api/posts
```
#### Для получения данных одного пользователя:
```text
GET
http://URL/api/post/<id>
```
#### Для добавления нового поста:
POST запрос должен содержать json!!!
```text
POST
http://URL/api/posts
```
JSON:
```json
{"title": "your_title", "content": "your_content", "is_private":  "True or False",
"user_id": "id of the user who created the post"}
```
Все поля обязательны!!!
#### Для изменения данных поста:
PUT запрос должен содержать json!!!
```text
PUT
http://URL/api/posts/<id>
```
JSON:
```json
{"title": "your_title", "content": "your_content", "is_private":  "True or False"}
```
Все поля обязательны!!!
#### Для удаления поста:
```text
DELETE
http://URL/api/posts/<id>
```
---
Это все, что касается работы с api на данный момент.
