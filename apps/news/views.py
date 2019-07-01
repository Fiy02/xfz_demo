from .models import News, NewsCategory
from django.conf import settings
from utils import restful
from django.shortcuts import render
from .serializers import NewsSerializer,CommentSerializer
from django.http import Http404
from .forms import PublicCommentForm
from .models import Comment,Banner
from apps.xfzauth.decorators import xfz_login_required
from django.db.models import Q

# 首页；
def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    # 使用select_related优化从数据库中提取数据的次数；
    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners': Banner.objects.all(),
    }
    return render(request, 'news/index.html', context=context)


# 通过页数的方式获取每次显示的数据；
def news_list(request):
    # 通过p参数指定要获取第几页的数据;
    # p参数：通过查询字符串的方式传过来的/news/list/?p=2；默认值为：1；
    page = int(request.GET.get('p', 1))
    # 分类为0时，表示不进行任何分类；
    category_id = int(request.GET.get('category_id',0))
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category','author').filter(category_id=category_id)[start:end]
    # 使用序列化：{'id':1,'title':'abc','category':{'id':1,'name':'热点'}}
    # many：表示newses中含有多个数据，且需全部进行序列化；
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)

    # 没使用序列化的情况；{'id':1,'title':'abc','category':1};
    # newses = News.objects.order_by('-pub_time')[start:end].values()
    # for news in newses:
    #     print(news)
    # return restful.ok()

# 新闻详情页面；
def new_detail(request, news_id):
    try:
        # select_realated：提取使用的外键的数据；
        # prefetch_related：作为他人的外键来进行反向提取数据；（先一次性获取comments的数据，再一次性获取其中author的数据；只进行两次请求，避免评论区中评论过多时需每次获取其用户及其数据；）
        news = News.objects.select_related('category','author').prefetch_related("comments__author").get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/new_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404

# 评论区；
@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_errors())

# 搜索页面；
def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context['newses'] = newses
    return render(request, 'search/search.html',context=context)
