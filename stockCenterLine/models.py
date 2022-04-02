from django.contrib.auth.models import User
from django.db import models


class Monitoring(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_count = models.IntegerField('계산횟수', default=0)
    setting_count = models.IntegerField('환경저장횟수', default=0)

    def __str__(self):
        return f"{self.user.username} ({self.query_count})"


class Setting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField('가중치')
    max_value = models.IntegerField('최대값')
    min_value = models.IntegerField('최소값')
    unit = models.IntegerField('단위')
    selected = models.CharField('선택여부', max_length=100)

    def __str__(self):
        return f"{self.user.username} settings"
