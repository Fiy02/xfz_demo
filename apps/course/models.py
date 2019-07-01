from django.db import models
from shortuuidfield import ShortUUIDField


# 课程分类；
class CourseCategory(models.Model):
    name = models.CharField(max_length=100)


# 讲师模板；
class Teacher(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.URLField()  # 头像
    jobtitle = models.CharField(max_length=100)
    profile = models.TextField()


# 课程模板；
class Course(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField(null=True)
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)


# 支付页面模板；
class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    course = models.ForeignKey("Course", on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("xfzauth.User", on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 支付渠道：1：代表支付宝支付；2：代表微信支付；
    istype = models.SmallIntegerField(default=1)
    # 支付状态：1：代表未支付；2：代表支付成功；
    status = models.SmallIntegerField(default=1)
