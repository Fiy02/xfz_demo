from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.news.models import NewsCategory, News
from .forms import EditNewscategoryForm, WriteNewsForm, AddBannerForm, EditBannerForm,EditNewsForm
from utils import restful
from django.conf import settings
import os
import qiniu
from apps.news.models import Banner
from apps.news.serializers import BannerSerializer
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from apps.xfzauth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


# 使用装饰器只允许员工登录；非员工跳转至首页；
@staff_member_required(login_url='index')
def index(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'cms/news/index.html',context=context)


# 编辑发布新闻；
@method_decorator(permission_required(perm='news.add_news',login_url='/'),name='dispatch')
class WriteNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'cms/news/write_news.html', context=context)

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, content=content, category=category, thumbnail=thumbnail,
                                author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

# 修改新闻内容；
@method_decorator(permission_required(perm='news.change_news',login_url='/'),name='dispatch')
class EditNewsView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)

        context = {
            'news': news,
            'categories': NewsCategory.objects.all()
        }
        return render(request, 'cms/news/write_news.html', context=context)
    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get('pk')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(title=title, desc=desc, content=content, category=category,thumbnail=thumbnail)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

# 删除新闻；
@permission_required(perm='news.delete_news',login_url='/')
@require_POST
def delete_news(request):
    news_id = request.POST.get('news_id')
    News.objects.filter(pk=news_id).delete()
    return restful.ok()

# 新闻分类；
@require_GET
@permission_required(perm='news.add_newscategory',login_url='/')
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news/news_category.html', context=context)


# 添加新闻分类；
@require_POST
@permission_required(perm='news.add_newscategory',login_url='/')
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已存在！')


# 修改分类；
@require_POST
@permission_required(perm='news.change_newscategory',login_url='/')
def edit_news_category(request):
    form = EditNewscategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
        except:
            return restful.params_error(message='该分类不存在!')
        return restful.ok()
    else:
        return restful.params_error(message=form.get_error())


# 删除分类;
@require_POST
@permission_required(perm='news.delete_newscategory_news',login_url='/')
def delete_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在！')


# 文件上传；
@require_POST
@staff_member_required(login_url='index')
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # 获取整个url链接地址；
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': url})


# 上传七牛云；
@require_GET
@staff_member_required(login_url='index')
def qntokon(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY
    bucket = settings.QINIU_BUCKET_NAME
    # 创建授权信息q；
    q = qiniu.Auth(access_key, secret_key)
    # 生成上传凭证'tokon'，传给前端；
    tokon = q.upload_token(bucket)
    return restful.result(data={'tokon': tokon})


# 后台轮播图管理；
@permission_required(perm='news.add_banner',login_url='/')
def banners(request):
    return render(request, 'cms/news/banners.html')


# 后台轮播图管理保存事件视图；
def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, image_url=image_url, link_to=link_to)
        return restful.result(data={'banner_id': banner.pk})
    else:
        return restful.params_error(form.get_errors())


# 显示序列化轮播图；
@permission_required(perm='news.add_banner',login_url='/')
def banner_list(request):
    banners = Banner.objects.all()
    serialize = BannerSerializer(banners, many=True)
    return restful.result(data=serialize.data)


# 删除轮播图；
@permission_required(perm='news.delete_banner',login_url='/')
def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


# 修改轮播图；
@permission_required(perm='news.change_banner',login_url='/')
def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        image_url = form.cleaned_data.get('image_url')
        priority = form.cleaned_data.get('priority')
        link_to = form.cleaned_data.get('link_to')
        Banner.objects.filter(pk=pk).update(image_url=image_url, priority=priority, link_to=link_to)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


# 轮播图列表；
@method_decorator(permission_required(perm='news.change_news',login_url='/'),name='dispatch')
class NewsListView(View):
    def get(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # request.GET.get(参数，默认值)
        # 默认值只有在参数没有传递的时候才会使用；如果传递的是一个空的字符串，也不会使用默认值；
        category_id = int(request.GET.get('category',0) or 0)
        newses = News.objects.select_related('category', 'author')
        # 判断是否进行时间筛选；
        if start or end:
            if start:
                start_date = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_date = datetime(year=2019,month=1,day=1)
            if end:
                end_date = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = News.objects.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))
        if title:
            newses = News.objects.filter(title__icontains=title)
        if category_id:
            newses = News.objects.filter(category=category_id)
        # 页数默认为1；
        page = int(request.GET.get('p', 1))
        # 分页默认显示2项内容；
        paginator = Paginator(newses, 2)
        # 获取当前页的对象；
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator, page_obj)
        # 在HTML模板中使用到的数据；
        context = {
            'categories': NewsCategory.objects.all(),
            # 通过‘object_list’得到当前页的数据；
            'newses': page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj,
            'start': start,
            'end': end,
            'title': title,
            'category_id': category_id,
            # url查询的参数，使网页在进行查询时拼接该链接能使用正确的url，使翻页时url不会被重置以致查询失败；
            'url_query': '&' + parse.urlencode({
                'start': start or '',
                'end': end or '',
                'title': title or '',
                'category': category_id or '',
            })
        }
        # print(context['url_query'])
        # & start = ? & end = ? & title = ? & category = ? ；
        context.update(context_data)
        return render(request, 'cms/news/news_list.html', context=context)

    # 实现分页的算法；
    def get_pagination_data(self, paginator, page_obj, around_count=2):
        # 当前页；
        current_page = page_obj.number
        # 总页数；
        num_pages = paginator.num_pages
        left_has_more = False
        right_has_more = False

        # 左边页数的显示区间；
        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        # 右边页数的显示区间；
        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)
        return {
            # 当前页；
            'current_page': current_page,
            # 总页数；
            'num_pages': num_pages,
            'right_pages': right_pages,
            'left_pages': left_pages,
            'right_has_more': right_has_more,
            'left_has_more': left_has_more,
        }
