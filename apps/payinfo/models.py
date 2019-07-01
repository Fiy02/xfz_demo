from django.db import models
from shortuuidfield import ShortUUIDField

# 付费资讯模板；
class Payinfo(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    profile = models.CharField(max_length=200)
    path = models.FilePathField()
    cover_url = models.URLField(null=True)

# 付费资讯订购模板；
class Payinfo_order(models.Model):
    uid = ShortUUIDField(primary_key=True)
    payinfo = models.ForeignKey('Payinfo',on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey('xfzauth.User',on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    istype = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(default=1)