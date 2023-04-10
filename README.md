# Yatube (hw05_final)
![python version](https://img.shields.io/badge/Python-3.9-green)
![django version](https://img.shields.io/badge/Django-2.2-green)
![pillow version](https://img.shields.io/badge/Pillow-8.3-green)
![pytest version](https://img.shields.io/badge/pytest-6.2-green)
![requests version](https://img.shields.io/badge/requests-2.26-green)

Данная платформа является социальной сетью, в которой пользователи могут публиковать свои персональные записи. В рамках разработки были реализованы функции пагинации постов и кэширования данных. Также была создана система регистрации пользователей, включающая верификацию предоставляемых данных, возможность смены пароля и восстановления доступа через почту. Для проверки работы сервиса были написаны и успешно выполнены тесты на unittest.

## Как запустить проект:

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас Windows

    ```
    .\venv\Scripts\activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

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
