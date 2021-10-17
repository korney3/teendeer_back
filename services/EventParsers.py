import pandas as pd
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackathon.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from database.models import Talent, Achievement, Step, Challenge, Task
from services.DatabaseService import DatabaseService

class EventParser(DatabaseService):
    def __init__(self, path_to_file = "./data/posts.csv"):
        self.path_to_file = path_to_file

    def parse(self):
        posts = pd.read_csv(self.path_to_file, nrows = 20)
        self.save_posts(posts)

def main():
    parser = EventParser()
    parser.parse()

