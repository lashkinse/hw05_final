# Yatube
Данная платформа является социальной сетью, в которой пользователи могут публиковать свои персональные записи. В рамках разработки были реализованы функции пагинации постов и кэширования данных. Также была создана система регистрации пользователей, включающая верификацию предоставляемых данных, возможность смены пароля и восстановления доступа через почту. Для проверки работы сервиса были написаны и успешно выполнены тесты на unittest.

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

## Авторы
Лашкин Сергей
