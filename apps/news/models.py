from django.db import models

class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

# 新闻模板；
class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('NewsCategory',on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey('xfzauth.User',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['-pub_time']

# 评论模板；
class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey("News",on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE)
    class Meta:
        ordering = ['-pub_time']


# 后台轮播图管理保存事件模板；
class Banner(models.Model):
    image_url = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)
    link_to = models.URLField()
    priority = models.IntegerField(unique=True,error_messages={'unique':'优先级已存在,请重新赋值！'})
    class Meta:
        ordering = ['priority']