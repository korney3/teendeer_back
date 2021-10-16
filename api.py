import os

import django

from services.ChallengesParser import ChallengesParser

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

from database.models import (GiftedChild, Talent, Achievement, Step, Challenge, Task)




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
    Talent.objects.all().delete()
    Achievement.objects.all().delete()
    Step.objects.all().delete()
    Challenge.objects.all().delete()
    Task.objects.all().delete()

    parser = ChallengesParser("./data/Challenges_DS29.xlsx")
    parser.parse()
    return jsonable_encoder([i for i in Talent.objects.all().values()])

#лучше стартовать из под консоли
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
