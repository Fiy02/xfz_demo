from rest_framework import serializers
from .models import NewsCategory,News,Comment,Banner
from apps.xfzauth.serializers import UserSerializer

# 序列化（用法类似于表单form）；
class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

# 定义首页中，文章显示出来的内容；
class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','author','category','pub_time')

# 评论区显示序列化；
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('id','content','pub_time','author')

# 轮播图管理显示序列化；
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','image_url','priority','link_to')