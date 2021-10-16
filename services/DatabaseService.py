from database.models import Talent, Achievement, Challenge, Task, Step


class DatabaseService:

    def save_talent(self, talents):
        for i in range(len(talents)):

            talent = talents.iloc[i]
            print(i)
            print(talent["talant_name"])
            ids = [x[0] for x in Talent.objects.values_list("id")]
            if len(ids)==0:
                id_start = 0
            else:
                id_start = max(ids)
            talent_db = Talent.objects.create(uuid = id_start, name=talent["talant_name"])

    def save_achievements(self, achievements):
        for i in range(len(achievements)):
            achievement = achievements.loc[i]
            ids = [x[0] for x in Achievement.objects.values_list("id")]
            if len(ids) == 0:
                id_start = 0
            else:
                id_start = max(ids)
            achievement_db = Achievement.objects.create(uuid = id_start, name=achievement["achievement_name"],
                                                        image_url=achievement["achievement_name"],
                                                        description=achievement["image_url"],
                                                        achievement_type=achievement["type"],
                                                        talent_points=achievement["talant_points"]
                                                        )

    def save_challenges(self, challenges):
        for i in range(len(challenges)):
            challenge = challenges.loc[i]
            talent_db = Talent.objects.get(pk=int(challenge["talant_id"])).values()[0]
            achievement_db = Achievement.objects.get(pk=int(challenge["achievement_id"])).values()[0]
            ids = [x[0] for x in Challenge.objects.values_list("id")]
            if len(ids) == 0:
                id_start = 0
            else:
                id_start = max(ids)
            challenge_db = Challenge.objects.create(uuid = id_start, challenge_name=challenge["challenge_name"],
                                                    image_url=challenge["image_url"],
                                                    req_talent_level=challenge["req_talant_level"],
                                                    description=challenge["challenge_description"],
                                                    talent=talent_db,
                                                    achievement=achievement_db)

    def save_tasks(self, tasks):
        for i in range(len(tasks)):
            task = tasks.loc[i]
            challenge_db = Challenge.objects.get(pk=int(task["challenge_id"])).values()[0]
            ids = [x[0] for x in Task.objects.values_list("id")]
            if len(ids) == 0:
                id_start = 0
            else:
                id_start = max(ids)
            task_db = Task.objects.create(uuid = id_start,challenge=challenge_db,
                                          task_name=task["task_name"],
                                          description=task["description"],
                                          image_url=task["url"],
                                          task_points=task["talant_points"],
                                          task_number=task["task_number"])

    def save_steps(self, steps):
        for i in range(len(steps)):
            step = steps.loc[i]
            task_db = Task.objects.get(pk=int(step["task_id"])).values()[0]
            ids = [x[0] for x in Step.objects.values_list("id")]
            if len(ids) == 0:
                id_start = 0
            else:
                id_start = max(ids)
            step_db = Step.objects.create(uuid = id_start,task=task_db,
                                          step_name=step["step_name"],
                                          step_number=step["step_number"],
                                          step_text=step["step_text"],
                                          image_url=step["image_url"],
                                          button_text=step["button_text"],
                                          meta_type=step["meta_type"],
                                          meta_urls=step["meta_urls"])

