# Meteo microservice
Микровервис для работы с метео-данными в "Цифровом двойнике".

## Разработано с помощью:
- Python 3.11
- FastAPI
- PostgreSQL 
- SQLAlchemy v2
- Pydantic v2
- AppScheduler

## Сборка и запуск проекта:


Если не создана docker-сеть `agronetwork`, то:

    docker create network agronetwork

Выполнить миграции (при необходимости):

    docker compose run migrations

Из корневой папки проекта:

    docker compose up -d 

Swagger: `http://0.0.0.0:8003/docs`
