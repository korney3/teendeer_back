from database.models import Talent, Achievement, Challenge, Task, Step, User, Product
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for _ in range(length))
    return rand_string


class DatabaseService:
    def save_talent(self, talents):
        for i in range(len(talents)):
            talent = talents.iloc[i]
            print(i)
            print(talent["talant_name"])
            ids = [x[0] for x in Talent.objects.values_list("id")]
            talent_db = Talent.objects.create(name=talent["talant_name"])

    def save_achievements(self, achievements):
        for i in range(len(achievements)):
            achievement = achievements.loc[i]
            ids = [x[0] for x in Achievement.objects.values_list("id")]
            achievement_db = Achievement.objects.create(name=achievement["achievement_name"],
                                                        image_url=achievement["achievement_name"],
                                                        description=achievement["image_url"],
                                                        achievement_type=achievement["type"],
                                                        talent_points=achievement["talant_points"]
                                                        )

    def save_challenges(self, challenges):
        for i in range(len(challenges)):
            challenge = challenges.loc[i]
            talent_db = Talent.objects.get(pk=int(challenge["talant_id"]))
            achievement_db = Achievement.objects.get(pk=int(challenge["achievement_id"]))
            challenge_db = Challenge.objects.create(challenge_name=challenge["challenge_name"],
                                                    image_url=challenge["image_url"],
                                                    req_talent_level=challenge["req_talant_level"],
                                                    description=challenge["challenge_description"],
                                                    talent=talent_db,
                                                    achievement=achievement_db)

    def save_tasks(self, tasks):
        for i in range(len(tasks)):
            task = tasks.loc[i]
            challenge_db = Challenge.objects.get(pk=int(task["challenge_id"]))
            task_db = Task.objects.create(challenge=challenge_db,
                                          task_name=task["task_name"],
                                          description=task["description"],
                                          image_url=task["url"],
                                          task_points=task["talant_points"],
                                          task_number=task["task_number"])

    def save_steps(self, steps):
        for i in range(len(steps)):
            step = steps.loc[i]
            task_db = Task.objects.get(pk=int(step["task_id"]))
            # ids = [x[0] for x in Step.objects.values_list("id")]
            # if len(ids) == 0:
            #     id_start = 0
            # else:
            #     id_start = max(ids)
            step_db = Step.objects.create(task=task_db,
                                          step_name=step["step_name"],
                                          step_number=step["step_number"],
                                          step_text=step["step_text"],
                                          image_url=step["image_url"],
                                          button_text=step["button_text"],
                                          meta_type=step["meta_type"],
                                          meta_urls=step["meta_urls"])

    def save_posts(self, events):
        for i in range(len(events)):
            event = events.loc[i]

            from urlextract import URLExtract
            extractor = URLExtract()
            urls = extractor.find_urls(event['attachments'])
            event = Product.objects.create(product_name="??????????",
                                           description=event["text"],
                                           price=random.randint(0, 20),
                                           url=urls[0],
                                           image_url=urls[-1],
                                           geo="",
                                           product_type="????????")

    def save_users(self, users):
        for i in range(len(users)):
            user = users.loc[i]

            user = User.objects.create(fullname=user['fullname'],
                                       login=generate_random_string(16),
                                       password='',
                                       user_level=0,
                                       points=0)

            try:
                user.date_of_birth = user['date_of_birth']
                user.save()
            except:
                pass

            try:
                user.bio = user['bio']
                user.save()
            except:
                pass

            try:
                user.school = user['schools']
                user.save()
            except:
                pass

            try:
                user.organizations = user['organizations']
                user.save()
            except:
                pass

            try:
                user.organizations = user['organizations']
                user.save()
            except:
                pass

            try:
                user.user_sex = user['sex']
                user.save()
            except:
                user.user_sex = 3
                user.save()

            try:
                user.geo = user['geo']
                user.save()
            except:
                user.user_sex = 3
                user.save()

            try:
                user.vk_url = user['vk_url']
                user.save()
            except:
                pass

            try:
                user.vk_subscribers = user['vk_subscribers']
                user.save()
            except:
                pass
