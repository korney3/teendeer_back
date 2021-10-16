import pandas as pd



import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from database.models import Talent, Achievement, Step, Challenge, Task
from services.DatabaseService import DatabaseService

class ChallengesParser(DatabaseService):
    def __init__(self, path_to_file = "../data/Challenges_DS29.xlsx"):
        self.path_to_file = path_to_file

    def parse(self):
        challenges = pd.read_excel(self.path_to_file, sheet_name="Challenges")
        tasks = pd.read_excel(self.path_to_file, sheet_name="Tasks")
        steps = pd.read_excel(self.path_to_file, sheet_name="Steps")
        achievements = pd.read_excel(self.path_to_file, sheet_name="Achievements")
        talents = pd.read_excel(self.path_to_file, sheet_name="Talants")

        self.save_talent(talents)
        self.save_achievements(achievements)
        self.save_challenges(challenges)
        self.save_tasks(tasks)
        self.save_steps(steps)


def main():
    Talent.objects.all().delete()
    Achievement.objects.all().delete()
    Step.objects.all().delete()
    Challenge.objects.all().delete()
    Task.objects.all().delete()

    parser = ChallengesParser()
    parser.parse()

if __name__ == "__main__":
    main()


