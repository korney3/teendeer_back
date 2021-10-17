# TeenDeer Backend

Решение команды **DS29** кейса по созданию персональной бонусной системы [Хакатона на Полярном Круге](https://hackymal.com/).

Репозиторий содержит backend часть приложения **TeenDeer**. **TeenDeer** - платформа для саморазвития молодежи, наполненная образовательными ресурсами и геймификацией для выявления и развития юных талантов. 

## Описание

В репозитории содержатся инструменты для работы с базой данных приложения **TeenDeer**.  

## Getting Started

### Dependencies

Requirements are described in `requirements.txt`

### Installing

```
pip install -r requirements.txt
```

### Executing program

#### Database

```
python3 manage.py makemigrations
```

```
python3 manage.py migrate
```

#### Server

```
uvicorn api:app --reload --port 5000 --host=0.0.0.0
```
## Functional

Схема базы данных и сущности расположены в файле [models.py](database/models.py)

С возможными CRUD операциями с базой данных можно ознакомиться в [api.py](api.py) 

## Authors

[Анастасия Кишкун](https://github.com/Kichkun)

[Антон Шишов](https://github.com/wecoastca)

Полина Малютина

[Алиса Аленичева](https://github.com/korney3)

[Евгений Быковских](https://github.com/redzumi)

