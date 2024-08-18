## Gazprom ID

Gazprom ID — это программное обеспечение для построения и управления организационными диаграммами. Оно помогает компании управлять своей организационной структурой и визуализировать ее.

В рамках проекта был разработан RESTful API для управления организационными схемами, справочниками сотрудников и командными структурами.

### Основные возможности

1. CRUD-операции для работы с данными сотрудников и организационными структурами (пользователи, департаменты, продукты, команды, компоненты, дополнительные поля и метрики).
2. Поиск и фильтрация данных по различным полям каждой сущности.
3. Реляционная база данных PostgreSQL для безопасного и эффективного хранения данных.
4. Обеспечена целостность данных и внедрены необходимые индексы для оптимизации производительности.
5. Поддержка аутентификации на основе JWT и управление доступом на основе ролей (пользователь и суперпользователь).
6. Кэширование с использованием cachalot и Redis для повышения производительности.
7. Ведение журналов и мониторинг с использованием Sentry.
8. Отправка email-уведомлений с использованием Celery и Redis (при восстановлении пароля, добавлении и удалении из команды). 
9. Проект развернут на удаленном сервере с использованием Docker и Docker Compose.

## Документация

Swagger документация доступна по адресу: [Swagger UI](https://gazprom-id-6.online/api/schema/swagger-ui/)

Мониторинг очереди задач: [Flower Dashboard](https://flower.gazprom-id-6.online/) (на данный момент доступно без аутентификации)

## Авторы проекта

[Beliaev Mikhail](https://github.com/tooMike) – [Telegram](https://t.me/gusoyn)

## Установка и запуск с Docker

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Gazprom-team-6/backend/
```

```
cd backend
```

Запустить сборку проекта (для запуска необходимо добавить файл с секретами .env):

```
docker compose up
```

Выполнить сбор статики в контейнере backend:

```
docker compose exec backend python manage.py collectstatic
```

Выполнить миграции в контейнере backend:

```
docker compose exec backend python manage.py migrate
```

Проект будет доступен по адресу:

```
http://localhost:8000/
```

Flower будет доступен по адресу:

```
http://localhost:5555
```

## Спецификация

При локальном запуске документация будет доступна по адресу:

```
http://localhost:8000/api/schema/swagger-ui/
```

## Стэк 

Python, Django, Django REST Framework (DRF), PostgreSQL, Redis, Docker, Docker Compose, Nginx, Gunicorn, Sentry, Swagger

Использованы дополнительные библиотеки, фреймворки:
* [DRF](https://www.django-rest-framework.org/)
* [djoser](https://djoser.readthedocs.io/en/latest/index.html)
* [drf_spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
* [django_filters](https://django-filter.readthedocs.io/en/stable/guide/usage.html)
* [cachalot](https://django-cachalot.readthedocs.io/en/latest/)
* [celery](https://docs.celeryq.dev/en/stable/)
* [flower](https://flower.readthedocs.io/en/latest/)

## Примеры запросов к API

### Добавление нового сотрудника

* Описание метода: Добавление нового сотрудника в сервис.
* Права доступа: Доступно только суперпользователю.
* Тип запроса: `POST`
* Эндпоинт: `/api/users/`
* Обязательные параметры: `password, employee_fio`

Пример запроса:

```
{
  "password": "string",
  "employee_fio": "string",
  "email": "user@example.com",
  "employee_position": "string",
  "employee_date_of_birth": "2024-08-18",
  "employee_date_of_hire": "2024-08-18",
  "employee_telegram": "string",
  "employee_telephone": "+59824185046837",
  "employee_type_job": "full_time",
  "employee_status": "working",
  "employee_location": "string",
  "employee_grade": "1",
  "employee_description": "string",
  "is_superuser": true,
  "is_employee_outsource": true,
  "skills": [
    0
  ],
  "employee_departament": 0
}
```

Пример успешного ответа:

```
{
  "id": 0,
  "employee_fio": "string",
  "email": "user@example.com",
  "employee_position": "string",
  "employee_date_of_birth": "2024-08-18",
  "employee_date_of_hire": "2024-08-18",
  "employee_telegram": "string",
  "employee_telephone": "+8227190211950",
  "employee_type_job": "full_time",
  "employee_status": "working",
  "employee_location": "string",
  "employee_grade": "1",
  "employee_description": "string",
  "is_superuser": true,
  "is_employee_outsource": true,
  "skills": [
    0
  ],
  "employee_departament": 0
}
```

### Получение токена

* Описание метода: Получение токена пользователя.
* Права доступа: Доступно всем пользователям.
* Тип запроса: `POST`
* Эндпоинт: `/api/users/auth/jwt/create/`
* Обязательные параметры: `email, password`

Пример запроса:

```
{
  "email": "root@mail.ru",
  "password": "root"
}
```

Пример успешного ответа:

```
{
  "access": "string",
  "refresh": "string"
}
```

### Получение списка сотрудников

* Описание метода: Получение списка сотрудников.
* Права доступа: Доступно авторизированным пользователя.
* Тип запроса: `GET`
* Эндпоинт: `/api/users/`
* Доступна фильтрация по полям: `department, grade, is_outsource, job_type, location, position, product, skill, team`
* Доступен поиск по полям: `идентификатор, ФИО сотрудника, название отдела, должность, email, грейд, название продукта, локация (часовой пояс), название компонента, тип занятости, название команды, навыки, статус`

Пример успешного ответа:

```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "employee_fio": "string",
      "employee_avatar": "string",
      "employee_position": "string",
      "employee_departament": 0,
      "employee_telegram": "string",
      "employee_telephone": "+4883496733",
      "email": "user@example.com",
      "employee_type_job": "full_time",
      "employee_grade": "1"
    }
  ]
}
```

### Получение списка корневых продуктов

* Описание метода: Получение списка корневых продуктов (продуктов у которых нет родительского продукта).
* Права доступа: Доступно авторизированным пользователя.
* Тип запроса: `GET`
* Эндпоинт: `/api/product/product/root_products/`

Пример успешного ответа:

```
xample Value
Schema
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "product_name": "string",
      "product_description": "string",
      "product_manager": {
        "id": 0,
        "employee_fio": "string",
        "employee_avatar": "string",
        "employee_position": "string",
        "employee_grade": "1"
      },
      "components": [
        {
          "id": 0,
          "component_name": "string"
        }
      ]
    }
  ]
}
```

## Планы развития проекта

1. Разработка конечных точек API для упрощения импорта/экспорта данных.
2. Разработка дополнительных конечных точек API для упрощения и улучшения взаимодействия с frontend (на момент окончания первой стадии разработки frontend не был реализован в полном объеме)
3. Реализация комплексной обработки ошибок
4. Реализация юнит тестирования
5. Разработка более полной системы уведомлений сотрудников при внесении изменений в структуру компании (email и telegram)
6. Настройка интеграции с внешними системами управления персоналом для синхронизации данных

