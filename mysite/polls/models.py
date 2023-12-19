import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_short_desc = models.CharField(max_length=50, verbose_name="Краткое описание")
    question_desc = models.CharField(max_length=200, verbose_name="Полное описание")
    question_image = models.ImageField(verbose_name="Изображение", upload_to="images/", blank=True)
    question_votes = models.IntegerField(verbose_name="Количество голосовавших на посте", default=0)
    pub_date = models.DateTimeField('Дата публикации')

    @property
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def percentage(self):
        percents = self.votes * 100 / self.question.question_votes
        return percents


class AdvUser(AbstractUser):
    avatar = models.ImageField(verbose_name="Изображение пользователя", blank=False, upload_to='images/')


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
