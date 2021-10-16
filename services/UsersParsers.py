import pandas as pd
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from database.models import Talent, Achievement, Step, Challenge, Task
from services.DatabaseService import DatabaseService

class UsersParser(DatabaseService):
    def __init__(self, path_to_file = "../data/nb_yanao_members.csv"):
        self.path_to_file = path_to_file

    def parse(self):
        users = pd.read_csv(self.path_to_file)
        self.save_users(users)

def main():
    parser = UsersParser()
    parser.parse()

