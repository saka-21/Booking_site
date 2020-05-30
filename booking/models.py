from django.conf import settings
from django.db import models
from django.utils import timezone


class Store(models.Model):
    """店舗"""
    name = models.CharField(verbose_name='店名', max_length=255)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """店舗スタッフ"""
    name = models.CharField(verbose_name='表示名', max_length=50)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             verbose_name='ログインユーザー',
                             on_delete=models.CASCADE)
    store = models.ForeignKey(to=Store,
                              verbose_name='店舗',
                              on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'store'],
                                               name='unique_staff')]

    def __str__(self):
        return f'{self.store.name} - {self.name}'


class Schedule(models.Model):
    """予約スケジュール"""
    start = models.DateTimeField(verbose_name='開始時間')
    end = models.DateTimeField(verbose_name='終了時間')
    name = models.CharField(verbose_name='予約者名', max_length=255)
    staff = models.ForeignKey(to='Staff',
                              verbose_name='スタッフ',
                              on_delete=models.CASCADE)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.name}{start} ~ {end}{self.staff}'

