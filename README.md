## Описание

Gazprom ID представляет собой программное обеспечение для построения организационных диаграмм, разработанное для того,
чтобы помочь компании управлять своей организационной структурой и визуализировать ее.

В рамках данного проекта был разработан RESTful API для управления организационными схемами,
справочниками сотрудников и командными структурами. 

Документация Swagger доступна по адресу: https://gazprom-id-6.online/api/schema/swagger-ui/

Отслеживать очередь задач можно по адресу: https://flower.gazprom-id-6.online/ (на данный момент доступно без аутентификации) 

В данном проекте было реализовано:
1. Конечные точки для CRUD операций (создание, чтение, обновление,
удаление) с данными сотрудников и организации, а именно с такими сущностями как: 
пользователь (сотрудник), департамент, продукт, команда, компонент, а также дополнительные поля и метрики.
2. Поиск и фильтрация по различным полям каждой сущности.
3. Разработаны схемы реляционной базы данных для безопасного и эффективного хранения организационных данных (PostgreSQL).
4. Обеспечена целостность данных и внедрены необходимые индексы для оптимизации производительности.
5. Внедрены безопасные механизмы аутентификации с использованием JWT. 
6. Разработано управление доступом на основе ролей для управления разрешениями (пользователь и суперпользователь).
7. Реализована стратегии кэширования для повышения производительности с использованием cachalot и Redis.
8. Настроено ведение журнала и мониторинг для отслеживания производительности системы и проблем с использованием Sentry.
9. Реализована отправка писем по email сотрудникам с использованием Celery и Redis (при восстановлении пароля, добавлении и удалении из команды).
10. Проект запущен на удаленном сервере с использованием Docker и Docker Compose.

## Авторы проекта

[Beliaev Mikhail](https://github.com/tooMike)

## Установка и запуск с Docker

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Gazprom-team-6/backend/
```

```
cd backend
```

Запустить сборку проекта:

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

Проект будет доступен по адресу

```
http://127.0.0.1:8000/
```

## Спецификация

При локальном запуске документация будет доступна по адресу:

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

## Основные технические требования

Python==3.12

## Примеры запросов к API

### Добавление нового сотрудника

Описание метода: Добавление нового сотрудника в сервис.

Права доступа: Доступно только суперпользователю.

Тип запроса: `POST`

Эндпоинт: `/api/users/`

Обязательные параметры: `password, employee_fio`

Пример запрос:

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

### Получение списка сотрудников

Описание метода: Получение списка сотрудников.

Права доступа: Доступно авторизированным пользователя.

Тип запроса: `GET`

Эндпоинт: `/api/users/`

Доступна фильтрация по полям: `department, grade, is_outsource, job_type, location, position, product, skill, team`

Доступен поиск по полям: `идентификатор, ФИО сотрудника, название отдела, должность, email, грейд, название продукта, локация (часовой пояс), название компонента, тип занятости, название команды, навыки, статус`

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

Описание метода: Получение списка корневых продуктов (продуктов у которых нет родительского продукта).

Права доступа: Доступно авторизированным пользователя.

Тип запроса: `GET`

Эндпоинт: `/api/product/product/root_products/`

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