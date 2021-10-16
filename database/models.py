from django.db import models


# Create your models here.
class GiftedChild(models.Model):
    CLASS = 'C'
    ART = 'A'
    SINGER = 'S'
    DEERS = 'D'
    PROFESSION_CHOICES = [
        (CLASS, 'Class'),
        (ART, 'Art'),
        (SINGER, 'Singer'),
        (DEERS, 'Deers'),
    ]

    uuid = models.IntegerField(primary_key=True)
    specialization = models.CharField(
        max_length=2,
        choices=PROFESSION_CHOICES,
        default=CLASS,
    )

    name = models.CharField(max_length=64, null=True, blank=True)
    surname = models.CharField(max_length=64, null=True, blank=True)
    bio = models.CharField(max_length=512, null=True, blank=True)
    subscribers = models.ManyToManyField('database.GiftedChild', null=True, blank=True,
                                         related_name="subs")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(models.Model):
    uuid = models.IntegerField(primary_key=True)
    fullname = models.CharField(max_length=64, null=True, blank=True)

    login = models.CharField(max_length=64, null=False, blank=False, default="login", unique=False)
    password = models.CharField(max_length=64, null=False, blank=False, default="login")

    user_level = models.IntegerField(null=False, blank=False, default=1)

    bio = models.CharField(max_length=512, null=True, blank=True)
    school = models.CharField(max_length=512, null=True, blank=True)
    organizations = models.CharField(max_length=512, null=True, blank=True)

    date_of_birth = models.DateTimeField(auto_now=False, null=True, blank=True)


class Talent(models.Model):
    uuid = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=64, null=False, blank=False, default="talent", unique=False)
    users = models.ManyToManyField(User, blank=True)


class Achievement(models.Model):
    uuid = models.IntegerField(primary_key=True)

    name = models.CharField(max_length=64, null=False, blank=False, default="achievement", unique=False)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    achievement_type = models.CharField(max_length=64, null=False, blank=True, default="")
    talent_points = models.IntegerField(null=False, blank=False, default=1)


class Challenge(models.Model):
    uuid = models.IntegerField(primary_key=True)

    challenge_name = models.CharField(max_length=64, null=False, blank=False, default="challenge")
    image_url = models.CharField(max_length=512, null=True, blank=True)
    req_talent_level = models.IntegerField(null=False, blank=False, default=1)
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=512, null=True, blank=True)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=False, blank=False)


class Task(models.Model):
    uuid = models.IntegerField(primary_key=True)

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=False, blank=False)
    task_name = models.CharField(max_length=64, null=False, blank=False, default="task")
    description = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    task_points = models.IntegerField(null=False, blank=False, default=0)
    task_number = models.IntegerField(null=False, blank=False, default=1)


class Step(models.Model):
    uuid = models.IntegerField(primary_key=True)

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    step_name = models.CharField(max_length=64, null=False, blank=False, default="step")
    action = models.CharField(max_length=64, null=False, blank=False, default="action")
    step_number = models.IntegerField(null=False, blank=False, default=1)
    step_text = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    button_text = models.CharField(max_length=512, null=True, blank=True)
    meta_type = models.CharField(max_length=64, null=True, blank=True)
    meta_urls = models.CharField(max_length=512, null=True, blank=True)

