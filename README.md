![yamdb_workflow](https://github.com/bogdanov2000/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)

# api_yamdb_final

## Описание 
Проект выполнен в учебных целях в работе с API (DRF).  
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на произвольные категории, например: «Книги», «Фильмы», «Музыка». 
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор. 
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.  
 
## Стек
API написан на Python с использованием фреймворков Django и Django Rest Framework. Авторизация по JWT токену с использованием библиотеки simple-jwt. Фильтрация запросов с использованием библиотеки django-filter.

## Установка
На локальном компьютере должен быть установлен Docker.

1. Склонировать данный репозиторий на свой локальный компьютер.
2. В директории api_yamdb создать файл .env и прописать в нем переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
3. В терминале в корневой директории приложения выполнить команду `docker-compose up`.
4. После запуска контейнера в новой вкладке терминала выполнить команду `docker container ls` и узнать id контейнера.
5. Перейти в контейнер выполнив команду `docker container exec -it <id контейнер> bash`.
6. Внутри контейнера выполнить команды `python manage.py makemigrations` и `python manage.py migrate`.
7. Создать суперпользователя командой `python manage.py createsuperuser`.
 
Проект доступен по адресу https://ogv.ru/api/v1/ 
 
 
### Итоговый проект курса "Работа с внешними API"   
#### Выполнили: 
- [Анна Карпенко]
- [Александр Королев]
- [Сергей Богданов]
