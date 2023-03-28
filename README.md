# Yatube
Социальная сеть для публикации личных дневников. Реализована пагинация постов и кэширование данных, так же реализована регистрация пользователей с верификацией данных, сменой и восстановлением пароля через почту. Написаны тесты на unittest, проверяющие работу сервиса.

## Как запустить проект:

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Создать пользователя:
```
python manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```

## Технологии
Python 3.9, Django 2.2.16, SQLite

## Авторы
Лашкин Сергей
