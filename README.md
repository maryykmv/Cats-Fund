# Приложение QRKot
«Приложение QRKot»

## Оглавление
1. [Описание](#описание)
2. [Технологии](#технологии)
3. [Как запустить проект](#как-запустить-проект)
4. [Автор проекта](#автор-проекта)

## Описание
**Приложение для Благотворительного фонда поддержки котиков QRKot.** 
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых,
на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

**Проекты**
- В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
- Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

**Пожертвования**
- Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект.
- Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму.
- Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта.
- При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

**Пользователи**
- Целевые проекты создаются администраторами сайта. 
- Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
- Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

**Отчёт в Google Sheets для QRKot**
_[Google Report](http://127.0.0.1:8000/google/)_

**Технические подробности и требования**

Скачайте спецификацию проекта openapi.json:

Для просмотра документации загрузите файл на сайт https://redocly.github.io/redoc/ или https://editor.swagger.io/. 
Ваш API должен соответствовать всем требованиям документации.



## Технологии
- Python 3.9
- FastAPI 0.78.0
- SQLAlchemy
- SQLite
- Alembic==1.7.7

## Как запустить проект

- Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:wildcat3333/cat_charity_fund.git
```
- Переходим в директорию проекта:
```
cd cat_charity_fund
```

- Создаем и активируем виртуальное окружение:
```
python3 -m venv venv
```
* Если у вас Linux/macOS:
    ```
    source venv/bin/activate
    ```

* Если у вас windows:
    ```
    source venv/scripts/activate
    ```

- Пример заполнения конфигурационного .env файла
```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot
APP_DESCRIPTION=Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых,
на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=vvvvv
FIRST_SUPERUSER_EMAIL=qqq@yandex.ru
FIRST_SUPERUSER_PASSWORD=qqqqq
TYPE = service_account
PROJECT_ID = ffrvgg
PRIVATE_KEY_ID = 3453fefdgfdfs
PRIVATE_KEY = "-----BEGIN PRIVATE KEY\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL = 232432ededssdf
CLIENT_ID = 123123123123
AUTH_URI = https://accounts.google.com/o/oauth2/auth
TOKEN_URI = https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL = https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL = https://www.googleapis.com/robot/v1/metadata/x509/qqqqq
UNIVERSE_DOMAIN = googleapis.com
EMAIL = qqqqqqq@gmail.com
```

- Обновляем менеджер пакетов pip:
```
pip install --upgrade pip
```

- Устанавливаем зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

- Применить миграции
```
alembic upgrade head
```

- Запустит проект
```
uvicorn app.main:app
```

Документация к API досупна по адресам:
_[Swagger](http://127.0.0.1:8000/docs)_
_[Redoc](http://127.0.0.1:8000/redoc)_


## Автор проекта
_[Мария Константинова](https://github.com/wildcat3333)_, python-developer
