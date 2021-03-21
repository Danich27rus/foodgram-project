[![foodgram-project](https://github.com/sorochinskii/foodgram-project/workflows/foodgram-workflow/badge.svg)](https://github.com/sorochinskii/foodgram-project/actions)

# **Foodgram-project**

https://radiogoogooradioga.ga

Дипломный проект программы Яндекс.Практикум **[Python-разработчик](https://praktikum.yandex.ru/backend-developer/)**

Foodgram - онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

При работе над проектом использован стек технологий: **[Django](https://www.djangoproject.com/)**, **[Python](https://www.python.org/)**, **[PostgreSQL](https://www.postgresql.org/)**, **[NGINX](https://nginx.org/)**, **[Docker](https://www.docker.com/)**, **[Docker-Compose](https://docs.docker.com/compose/)**, **[GitHub](https://github.com)**.

## Разворачивание проекта

1.  Клонируйте проект

        git clone https://github.com/sorochinskii/foodgram-project
    
    Создайте файл .env, содержащий переменные окружения. Необходимые имена переменных
    можно взять из файла .env.example

2.  Если пользователь, который использует docker, не root, то добавьте 
    его в группу docker.

3.  Запустите процесс сборки и запуска контейнеров:

        docker-compose up --build

4.  Войдите в контейнер проекта и запустите шелл.

        docker-compose exec web bash

5.  Мигрируйте модели в структуру базы данных

        python manage.py makemigrations
        python manage.py migrate

6.  Создайте пользователя с правами администратора:

        python manage.py createsuperuser

7.  Добавляем в базу ингредиенты и теги:

        python manage.py load_fixtures

8.  Запустите сбор статики:

        python manage.py collectstatic
