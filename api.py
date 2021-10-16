import os
from typing import Optional

import django

from services.ChallengesParser import ChallengesParser
from pydantic import BaseModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from fastapi import (FastAPI,
                     HTTPException,
                     Depends,
                     status,
                     BackgroundTasks)
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database.models import (GiftedChild, Talent, Achievement, Step, Challenge, Task, User)

# Main app
app = FastAPI()

# CORS не трогайте, всё открыто
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/children/all", tags=['children'],
          summary='Возвращает инфу о всех детях в ДБ')
async def all_children():
    return jsonable_encoder([i for i in GiftedChild.objects.all().values()])


@app.get("/talent/all", tags=['talent'],
         summary='Возвращает все таланты')
async def all_talent():
    return jsonable_encoder([i for i in Talent.objects.all().values()])


class UserFront(BaseModel):
    fullname: str
    login: str
    password: Optional[str] = None

    user_level: Optional[int] = 1
    points: Optional[int] = 0

    bio: Optional[str] = None
    school: Optional[str] = None
    organizations: Optional[list] = None

    date_of_birth: Optional[str] = None
    talents: Optional[list] = None

class TalentFront(BaseModel):
    name: str

class ChallengeFront(BaseModel):
    challenge_name: str
    image_url : str = None
    req_talent_level : int = 1
    description: str = None


@app.post("/user/", tags=['user_post'],
          summary='Добавление юзера после авторизаци или регистрации')
async def сreate_user(user: UserFront):
    userDb = User.objects.create(
        fullname=user.fullname,
        login=user.login,
        password=user.password,
        bio=user.bio,
        school=user.school,
        organizations=user.organizations,
        date_of_birth=user.date_of_birth
    )
    res = jsonable_encoder(userDb)
    res["talents"] = None
    return res


@app.get("/user/{login}", tags=['user_get'],
         summary='Получение юзера после авторизаци или регистрации')
async def get_user(login):
    userDb = User.objects.get(login=login)
    res = jsonable_encoder(userDb)
    res["talents"] = [x[0] for x in Talent.objects.filter(users__login=login).values_list("id")]

    return res


@app.put("/user/{id}", tags=['user_put'],
         summary='Получение юзера после авторизаци или регистрации')
async def change_user(id: int, user: UserFront):
    userDb = User.objects.get(id=id)
    userDb.fullname = user.fullname
    userDb.login = user.login
    userDb.password = user.password
    userDb.bio = user.bio
    userDb.school = user.school
    userDb.organizations = user.organizations
    userDb.date_of_birth = user.date_of_birth
    userDb.points = user.points
    userDb.user_level = user.user_level
    userDb.save()
    for id_talent in user.talents:
        talentDb = Talent.objects.get(id = id_talent)
        talentDb.users.add(userDb)
        talentDb.save()
    res = jsonable_encoder(userDb)
    res["talents"] = [x[0] for x in Talent.objects.filter(users__id=id).values_list("id")]
    return res

# /user - POST (добавление юзера после авторизаци или регистрации), { login: string, ..., name: '' } : models.User
# /user/:login - GET (получение модели юзера по логину) : models.Usersx
# /user/:login (:id) - PUT (изменить модель юзера), { ...models.Users }: models.Users

@app.post("/talent/", tags=['talent_post'],
          summary='Добавление таланта')
async def сreate_talent(talent: TalentFront):
    talentDb = Talent.objects.create(
        name=talent.name
    )
    res = jsonable_encoder(talentDb)

    return res

@app.get("/talent/", tags=['talent_get'],
          summary='Получение таланта')
async def get_talent():
    talentsDb = list(Talent.objects.all())
    res = [jsonable_encoder(x) for x in talentsDb]

    return res

# /talent - POST (создание таланта), { name: string; } : models.Talent
# /talents - GET : models.Talent[]



# /challenges - GET (список доступных челенджев, потом докрутим проверку) : models.Challenge[]
# /challenge - POST (создать челендж), { ...partial(models.Challenge) } : models.Challenge
# /challenge/:id - PUT (изменить модель челенджа), { ...models.Challenge } : models.Challenge
# /challenge/:id - DELETE

# /task - POST (создать задачку), { partial(models.Task) } : models.Task
# /tasks/:challengeId - GET (список доступных задач, проверку сделаем потом) : models.Task[]
# /task/:id - PUT : models.Task
# /task/:id - DELETE

# /step - POST (создать задачку), { partial(models.Task) } : models.Task
# /steps/:taskId - GET (список доступных задач, проверку сделаем потом) : models.Task[]
# /step/:id - PUT : models.Task
# /step/:id - DELETE

# лучше стартовать из под консоли
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
