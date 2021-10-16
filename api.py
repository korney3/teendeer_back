import os
from typing import Optional

import django
from django.db.models import Q
from pydantic import BaseModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from fastapi import (FastAPI)
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database.models import (Talent, Challenge, User, UserTalent)

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
    user_sex: Optional[int] = 1
    vk_url: Optional[str] = None
    vk_subscribers: Optional[int] = None

    geo: Optional[str] = None
    talent_info: Optional[list] = None


class TalentFront(BaseModel):
    name: str


class ChallengeFront(BaseModel):
    challenge_name: str
    image_url: str = None
    req_talent_level: int = 1
    description: str = None
    talent_id: int


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
        date_of_birth=user.date_of_birth,
        user_sex=user.user_sex,
        vk_url=user.vk_url,
        vk_subscribers=user.vk_subscribers,
        geo=user.geo)

    res = jsonable_encoder(userDb)
    res["talent_info"] = None
    return res

@app.get("/user/{login}", tags=['user_get'],
         summary='Получение юзера после авторизаци или регистрации')
async def get_user(login):
    userDb = User.objects.get(login=login)
    res = jsonable_encoder(userDb)
    user_id = userDb.id
    userTalentsDb = UserTalent.objects.filter(user_id=user_id)
    talent_infos = {}
    for userTalentDb in userTalentsDb:
        talent_info = {
            "talent_id": userTalentDb.talent_id,
            "talent_points": userTalentDb.talent_points,
            "talent_level": userTalentDb.talent_level
        }
        talent_infos.append(talent_info)

    res["talent_info"] = talent_infos
    return res

@app.get("/user", tags=['user_get_all'],
         summary='Получение юзера после авторизации или регистрации')
async def get_all_user():
    logins =[i['login'] for i in User.objects.all().values("login")]

    ress = []
    for login in logins:
        userDb = User.objects.get(login=login)
        res = jsonable_encoder(userDb)
        user_id = userDb.id
        userTalentsDb = UserTalent.objects.filter(user_id=user_id)
        talent_infos = []
        for userTalentDb in userTalentsDb:
            talent_info = {
                "talent_id": userTalentDb.talent_id,
                "talent_points": userTalentDb.talent_points,
                "talent_level": userTalentDb.talent_level
            }
            talent_infos.append(talent_info)
    
        res["talent_info"] = talent_infos
        ress.append(res)


    return jsonable_encoder(ress)


@app.put("/user/{id}", tags=['user_put'],
         summary='Изменение пользователя')
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
    userDb.vk_url = user.vk_url
    userDb.vk_subscribers = user.vk_subscribers
    userDb.geo = user.geo
    userDb.save()
    talent_infos = []
    for userTalent in user.talent_info:
        userTalentDb = UserTalent.objects.filter(Q(talent_id = userTalent["talent_id"]) & Q(user_id = id))
        if len(userTalentDb)==0:
            userTalentDb = UserTalent.objects.create(
                user=userDb,
                talent = Talent.objects.get(id = userTalent["talent_id"]),
                talent_level = userTalent['talent_level'],
                talent_points = userTalent['talent_points']
            )
        else:

            for x in userTalentDb:
                userTalentDb = x
                break

            userTalentDb.talent_level = userTalent['talent_level']
            userTalentDb.talent_points = userTalent['talent_points']
            userTalentDb.save()
        talent_infos.append(
            {"talent_id": userTalent['talent_id'],
             "talent_points": userTalent['talent_points'],
             "talent_level": userTalent['talent_level']}
        )

    res = jsonable_encoder(userDb)
    res["talent_info"] = talent_infos
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

@app.get("/challenge/{talent_id}", tags=['challenge_get'],
         summary='Получение челленджей')
async def get_challenge(talent_id):
    challengesDb = list(Challenge.objects.filter(talent__id=talent_id))
    res = [jsonable_encoder(x) for x in challengesDb]
    res_with_talents = []
    for challengeJson in res:
        challengeJson["talent_id"] = talent_id
        res_with_talents.append(challengeJson)

    return res_with_talents


@app.post("/challenge", tags=['challenge_post'],
          summary='Добавление челленджей')
async def post_challenge(challenge: ChallengeFront):
    challengeDb = Challenge.objects.create(
        challenge_name=challenge.name,
        image_url=challenge.url,
        req_talent_level=challenge.req_talent_level,
        description=challenge.description
    )
    talentDb = Talent.objects.get(id=challenge.talent_id)
    challengeDb.talent = talentDb
    challengeDb.save()
    res = jsonable_encoder(challengeDb)
    res["talent_id"] = challenge.talent_id
    return res


@app.put("/challenge/{id}", tags=['challenge_put'],
         summary='Обновление челленджей')
async def put_challenge(id: int, challenge: ChallengeFront):
    challengeDb = Challenge.objects.get(id=id)
    challengeDb.challenge_name = challenge.challenge_name
    challengeDb.image_url = challenge.url
    challengeDb.req_talent_level = challenge.req_talent_level
    challengeDb.description = challenge.description

    talentDb = Talent.objects.get(id=challenge.talent_id)
    challengeDb.talent = talentDb
    challengeDb.save()
    res = jsonable_encoder(challengeDb)
    res["talent_id"] = challenge.talent_id
    return res

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
