import os
from typing import Optional

import django
from django.db.models import Q
from pydantic import BaseModel

from services.UsersParsers import UsersParser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from fastapi import (FastAPI)
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database.models import (Talent, Challenge, User, UserTalent, Achievement, Task, Step, UserStep)

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
    step_info: Optional[list] = None

    achievement_ids: Optional[list] = None


class TalentFront(BaseModel):
    name: str


class ChallengeFront(BaseModel):
    challenge_name: str
    image_url: str = None
    req_talent_level: int = 1
    description: str = None
    talent_id: int = None
    achievement_id: int = None


class AchievementFront(BaseModel):
    name: str
    image_url: str = None
    description: str = None
    achievement_type: str = None
    talent_points: int = 1


class TaskFront(BaseModel):
    challenge_id: int
    task_name: str
    description: str = None
    image_url: str = None
    task_points: int = 1
    task_number: int = 1


class StepFront(BaseModel):
    task_id: int
    step_name: str
    action: str = None
    step_number: int = 1
    step_text: str = None
    image_url: str = None
    button_text: str = None
    meta_type: str = None
    meta_urls: str = None


@app.post("/user", tags=['user_post'],
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
    res["achievements"] = None
    return res


@app.get("/user/{login}", tags=['user_get'],
         summary='Получение юзера после авторизаци или регистрации')
async def get_user(login):
    userDb = User.objects.get(login=login)
    res = jsonable_encoder(userDb)
    user_id = userDb.id
    userTalentsDb = UserTalent.objects.filter(user_id=user_id)
    userStepsDb = UserStep.objects.filter(user_id=user_id)
    talent_infos = []
    step_infos = []
    for userTalentDb in userTalentsDb:
        talent_info = {
            "talent_id": userTalentDb.talent_id,
            "talent_points": userTalentDb.talent_points,
            "talent_level": userTalentDb.talent_level
        }
        talent_infos.append(talent_info)

    for userStepDb in userStepsDb:
        step_info = {
            "step_id": userStepDb.step_id,
            "active": userStepDb.active
        }
        step_infos.append(step_info)

    res["talent_info"] = talent_infos
    res["step_info"] = step_infos
    return res


@app.get("/user", tags=['user_get_all'],
         summary='Получение юзера после авторизации или регистрации')
async def get_all_user():
    logins = [i['login'] for i in User.objects.all().values("login")]

    ress = []
    for login in logins:
        userDb = User.objects.get(login=login)
        res = jsonable_encoder(userDb)
        user_id = userDb.id
        userTalentsDb = UserTalent.objects.filter(user_id=user_id)
        talent_infos = []
        userStepsDb = UserStep.objects.filter(users_id=user_id)
        step_infos = []

        for userTalentDb in userTalentsDb:
            talent_info = {
                "talent_id": userTalentDb.talent_id,
                "talent_points": userTalentDb.talent_points,
                "talent_level": userTalentDb.talent_level
            }
            talent_infos.append(talent_info)

        for userStepDb in userStepsDb:
            step_info = {
                "step_id": userStepDb.step_id,
                "active": userStepDb.active
            }
            step_infos.append(step_info)

        res["talent_info"] = talent_infos
        res["step_info"] = step_infos
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
        userTalentDb = UserTalent.objects.filter(Q(talent_id=userTalent["talent_id"]) & Q(user_id=id))
        if len(userTalentDb) == 0:
            userTalentDb = UserTalent.objects.create(
                user=userDb,
                talent=Talent.objects.get(id=userTalent["talent_id"]),
                talent_level=userTalent['talent_level'],
                talent_points=userTalent['talent_points']
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

    step_infos = []
    for userStep in user.step_info:
        userStepDb = UserStep.objects.filter(Q(steps_id=userStep["step_id"]) & Q(users_id=id))
        if len(userStepDb) == 0:
            userStepDb = UserStep.objects.create(
                user=userDb,
                step=Step.objects.get(id=userStep["step_id"]),
                active=userStep['active']
            )
        else:
            for x in userStepDb:
                userStepDb = x
                break

            userStepDb.active = userStep['active']
            userStepDb.save()
        step_infos.append(
            {"step_id": userStep['step_id'],
             "active": userStep['active']}
        )

    for achievement_id in user.achievement_ids:
        achievementDb = Achievement.get(id=achievement_id)
        userDb.achievement.add(achievementDb)
        userDb.save()

    res = jsonable_encoder(userDb)
    res["talent_info"] = talent_infos
    res["step_info"] = step_infos
    return res


@app.post("/talent", tags=['talent_post'],
          summary='Добавление таланта')
async def сreate_talent(talent: TalentFront):
    talentDb = Talent.objects.create(
        name=talent.name
    )
    res = jsonable_encoder(talentDb)

    return res


# /user - POST (добавление юзера после авторизаци или регистрации), { login: string, ..., name: '' } : models.User
# /user/:login - GET (получение модели юзера по логину) : models.Usersx
# /user/:login (:id) - PUT (изменить модель юзера), { ...models.Users }: models.Users

@app.get("/talent", tags=['talent_get'],
         summary='Получение таланта')
async def get_talent():
    talentsDb = list(Talent.objects.all())
    res = [jsonable_encoder(x) for x in talentsDb]

    return res


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


# /talent - POST (создание таланта), { name: string; } : models.Talent
# /talents - GET : models.Talent[]

@app.post("/achievement", tags=['achievement_post'],
          summary='Добавление ачивки')
async def сreate_achievement(achievement: AchievementFront):
    achievementDb = Achievement.objects.create(
        name=achievement.name,
        image_url=achievement.image_url,
        description=achievement.description,
        achievement_type=achievement.achievement_type,
        talent_points=achievement.talent_points
    )
    res = jsonable_encoder(achievementDb)

    return res


@app.get("/achievement", tags=['achievement_get'],
         summary='Получение ачивок')
async def get_achievements():
    achievementsDb = list(Achievement.objects.all())
    res = [jsonable_encoder(x) for x in achievementsDb]
    return res


@app.get("/challenge", tags=['challenge_all_get'],
         summary='Получение челленджей')
async def get_all_challenge():
    challengesDb = list(Challenge.objects.all())
    if len(challengesDb) == 0:
        res_with_talents = jsonable_encoder("")
    else:
        res = [jsonable_encoder(x) for x in challengesDb]
        res_with_talents = []
        for challengeJson in res:
            challengeJson["talent_id"] = Challenge.objects.get(id=challengeJson["id"]).talent_id
            res_with_talents.append(challengeJson)

    return res_with_talents


@app.post("/challenge", tags=['challenge_post'],
          summary='Добавление челленджей')
async def post_challenge(challenge: ChallengeFront):
    talentDb = Talent.objects.get(id=challenge.talent_id)
    achievementDb = Achievement.objects.get(id=challenge.achievement_id)

    challengeDb = Challenge.objects.create(
        challenge_name=challenge.challenge_name,
        image_url=challenge.image_url,
        req_talent_level=challenge.req_talent_level,
        description=challenge.description,
        talent=talentDb,
        achievement=achievementDb
    )

    res = jsonable_encoder(challengeDb)
    res["talent_id"] = challenge.talent_id
    res["achievement_id"] = challenge.achievement_id
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


@app.get("/parse")
async def parse_users_from_file():
    parser = UsersParser()
    parser.parse()


# /challenges - GET (список доступных челенджев, потом докрутим проверку) : models.Challenge[]
# /challenge - POST (создать челендж), { ...partial(models.Challenge) } : models.Challenge
# /challenge/:id - PUT (изменить модель челенджа), { ...models.Challenge } : models.Challenge
# /challenge/:id - DELETE #TO-DO

@app.get("/task/{challenge_id}", tags=['task_get'],
         summary='Получение  тасок')
async def get_task(challenge_id):
    tasksDb = list(Task.objects.filter(challenge__id=challenge_id))
    res = [jsonable_encoder(x) for x in tasksDb]
    res_with_challenges = []
    for taskJson in res:
        taskJson["challenge_id"] = challenge_id
        res_with_challenges.append(taskJson)

    return res_with_challenges


@app.get("/task", tags=['task_all_get'],
         summary='Получение всех тасок')
async def get_all_tasks():
    tasksDb = list(Task.objects.all())

    if len(tasksDb) == 0:
        res_with_challenges = jsonable_encoder("")
    else:
        res = [jsonable_encoder(x) for x in tasksDb]
        res_with_challenges = []
        for taskJson in res:
            taskJson["challenge_id"] = Task.objects.get(id=taskJson["id"]).challenge_id
            res_with_challenges.append(taskJson)

    return res_with_challenges


@app.post("/task", tags=['task_post'],
          summary='Добавление тасок')
async def post_task(task: TaskFront):
    challengeDb = Challenge.objects.get(id=task.challenge_id)

    taskDb = Task.objects.create(
        challenge=challengeDb,
        task_name=task.task_name,
        description=task.description,
        image_url=task.image_url,
        task_points=task.task_points,
        task_number=task.task_number
    )

    res = jsonable_encoder(taskDb)
    res["challenge_id"] = task.challenge_id

    return res


@app.put("/task/{id}", tags=['task_put'],
         summary='Обновление тасок')
async def put_task(id: int, task: TaskFront):
    taskDb = Task.objects.get(id=id)

    taskDb.task_name = task.name,
    taskDb.description = task.description,
    taskDb.image_url = task.image_url,
    taskDb.task_points = task.task_points,
    taskDb.task_number = task.task_number

    challengeDb = Challenge.objects.get(id=task.challenge_id)
    taskDb.challenge = challengeDb
    taskDb.save()
    res = jsonable_encoder(taskDb)
    res["challenge_id"] = task.challendge_id

    return res


# /task - POST (создать задачку), { partial(models.Task) } : models.Task
# /tasks/:challengeId - GET (список доступных задач, проверку сделаем потом) : models.Task[]
# /task/:id - PUT : models.Task
# /task/:id - DELETE

@app.get("/step/{task_id}", tags=['step_get'],
         summary='Получение  шагов')
async def get_step(task_id):
    stepDb = list(Step.objects.filter(task__id=task_id))
    res = [jsonable_encoder(x) for x in stepDb]
    res_with_tasks = []
    for stepJson in res:
        stepJson["task_id"] = task_id
        res_with_tasks.append(stepJson)

    return res


@app.get("/step", tags=['step_all_get'],
         summary='Получение всех шагов')
async def get_all_steps():
    stepsDb = list(Step.objects.all())

    if len(stepsDb) == 0:
        res_with_task = jsonable_encoder("")
    else:
        res = [jsonable_encoder(x) for x in stepsDb]
        res_with_task = []
        for stepJson in res:
            stepJson["task_id"] = Step.objects.get(id=stepJson["id"]).task_id
            res_with_task.append(stepJson)

    return res_with_task


@app.post("/step", tags=['step_post'],
          summary='Добавление шагов')
async def post_step(step: StepFront):
    taskDb = Task.objects.get(id=step.task_id)

    stepDb = Step.objects.create(
        task=taskDb,
        step_name=step.step_name,
        action=step.action,
        step_number=step.step_number,
        step_text=step.step_text,
        image_url=step.image_url,
        button_text=step.button_text,
        meta_type=step.meta_type,
        meta_urls=step.meta_urls
    )

    res = jsonable_encoder(stepDb)
    res["task_id"] = step.task_id

    return res


@app.put("/step/{id}", tags=['step_put'],
         summary='Обновление шагов')
async def put_step(id: int, step: StepFront):
    stepDb = Step.objects.get(id=id)

    stepDb.step_name = step.step_name
    stepDb.image_url = step.image_url
    stepDb.action = step.action
    stepDb.step_number = step.step_number
    stepDb.step_text = step.step_text
    stepDb.button_text = step.button_text
    stepDb.meta_type = step.meta_type
    stepDb.meta_urls = step.meta_urls

    taskDb = Task.objects.get(id=step.task_id)
    stepDb.task = taskDb
    stepDb.save()
    res = jsonable_encoder(stepDb)
    res["task_id"] = step.task_id

    return res

# /step - POST (создать задачку), { partial(models.Task) } : models.Task
# /steps/:taskId - GET (список доступных задач, проверку сделаем потом) : models.Task[]
# /step/:id - PUT : models.Task
# /step/:id - DELETE

# лучше стартовать из под консоли
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
