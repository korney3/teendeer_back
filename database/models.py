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
    fullname = models.CharField(max_length=64, null=True, blank=True)

    login = models.CharField(max_length=64, null=False, blank=False)
    password = models.CharField(max_length=64, null=False, blank=False)

    user_level = models.IntegerField(null=False, blank=False)

    bio = models.CharField(max_length=512, null=True, blank=True)
    school = models.CharField(max_length=512, null=True, blank=True)
    organizations = models.CharField(max_length=512, null=True, blank=True)

    date_of_birth = models.DateTimeField(auto_now=False)


class Talent(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)


class Challenge(models.Model):
    challenge_name = models.CharField(max_length=64, null=False, blank=False)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    req_talent_level = models.IntegerField(primary_key=False)
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE)


class Task(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=64, null=False, blank=False)
    description = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    task_points = models.IntegerField(primary_key=False)

