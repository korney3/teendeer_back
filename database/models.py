from django.db import models


# Create your models here.

class User(models.Model):
    fullname = models.CharField(max_length=64, null=False, blank=False)
    login = models.CharField(max_length=64, null=False, blank=False, default="login", unique=True)
    password = models.CharField(max_length=64, null=True, blank=True, default="password")

    user_level = models.IntegerField(null=False, blank=False, default=1)
    points = models.IntegerField(null=False, blank=False, default=0)

    bio = models.CharField(max_length=512, null=True, blank=True)
    school = models.CharField(max_length=512, null=True, blank=True)
    organizations = models.CharField(max_length=512, null=True, blank=True)

    date_of_birth = models.DateTimeField(auto_now=False, null=True, blank=True)

    user_sex = models.IntegerField(null=False, blank=False, default=1)
    vk_url = models.CharField(max_length=64, null=True, blank=True)
    vk_subscribers = models.IntegerField(null=True, blank=True)
    geo = models.CharField(max_length=512, null=True, blank=True)


class Talent(models.Model):

    name = models.CharField(max_length=64, null=False, blank=False, default="talent", unique=False)
    # users = models.ManyToManyField(User, blank=True)


class UserTalent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, null=False, blank=False)
    talent_level = models.IntegerField(null=False, blank=False, default=1)
    talent_points = models.IntegerField(null=False, blank=False, default=1)


class Achievement(models.Model):

    name = models.CharField(max_length=64, null=False, blank=False, default="achievement", unique=False)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    achievement_type = models.CharField(max_length=64, null=False, blank=True, default="")
    talent_points = models.IntegerField(null=False, blank=False, default=1)
    users = models.ManyToManyField(User, blank=True)


class Challenge(models.Model):

    challenge_name = models.CharField(max_length=64, null=False, blank=False, default="challenge")
    image_url = models.CharField(max_length=512, null=True, blank=True)
    req_talent_level = models.IntegerField(null=False, blank=False, default=1)
    talent = models.ForeignKey(Talent, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=512, null=True, blank=True)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, null=False, blank=False)


class Task(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=False, blank=False)
    task_name = models.CharField(max_length=64, null=False, blank=False, default="task")
    description = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    task_points = models.IntegerField(null=False, blank=False, default=0)
    task_number = models.IntegerField(null=False, blank=False, default=1)


class Step(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    step_name = models.CharField(max_length=64, null=False, blank=False, default="step")
    action = models.CharField(max_length=64, null=False, blank=False, default="action")
    step_number = models.IntegerField(null=False, blank=False, default=1)
    step_text = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    button_text = models.CharField(max_length=512, null=True, blank=True)
    meta_type = models.CharField(max_length=64, null=True, blank=True)
    meta_urls = models.CharField(max_length=512, null=True, blank=True)


class Product(models.Model):
    product_name = models.CharField(max_length=128, null=False, blank=False, default="product")
    description = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    price = models.IntegerField(null=False, blank=False, default=0)
    geo = models.CharField(max_length=512, null=True, blank=True)
    url = models.CharField(max_length=512, null=True, blank=True)
    product_type = models.CharField(max_length=64, null=True, blank=True)


class UserProduct(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    got_at = models.DateTimeField(auto_now_add=True)


class UserStep(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    steps = models.ForeignKey(Step, on_delete=models.CASCADE, null=False, blank=False)
    active = models.BooleanField(default=False)


class Post(models.Model):
    user_steps = models.ForeignKey(UserStep, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=512, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True)
    date_of_publication = models.DateTimeField(auto_now=False, null=True, blank=True)
    social_url = models.CharField(max_length=512, null=True, blank=True)
