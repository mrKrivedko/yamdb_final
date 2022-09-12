# yamdb_final
![yamdb_final](https://github.com/mrKrivedko/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Адрес сайта
http://62.84.124.198/api/v1/

## Описание
Сайт является - базой отзывов о фильмах, книгах и музыке.
Пользователи могут оставлять рецензии на произведения, а также комментировать эти рецензии.
Администрация добавляет новые произведения и категории (книга, фильм, музыка и т.д.)
Также присутствует файл docker-compose, позволяющий , быстро развернуть контейнер базы данных (PostgreSQL), контейнер проекта django + gunicorn и контейнер nginx
## Как запустить

## Необходимое ПО

Docker: https://www.docker.com/get-started <br />
Docker-compose: https://docs.docker.com/compose/install/

для сборки контейнера запустить комманду docker compose up -d --build
в папке infra размкщается файл .env В файле переменные для settings.py: SECRET_KEY настройки для postgresql:

DJANGOKEY='..'

DB_ENGINE='..'

DB_NAME='..'

POSTGRES_USER='..'

POSTGRES_PASSWORD='..'

DB_HOST='..'

DB_PORT='..'

после сборки контейнера выполнить миграции: docker compose exec web python manage.py migrate

после сборки контейнера выполнить миграции: docker compose exec web python manage.py createsuperuser

после сборки контейнера выполнить миграции: docker compose exec web python manage.py collectstatic --no-input

для загрузки дампа: docker compose exec web python manage.py loaddata fixtures.json
