from django.shortcuts import render
from .forms import PubCourseForm,EditCourseForm,EditCoursecategoryForm
from apps.course.models import Course,CourseCategory,Teacher
from django.views.generic import View
from utils import restful
from django.views.decorators.http import require_POST,require_GET
from django.core.paginator import Paginator
from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

# 发布课程；
@method_decorator(permission_required(perm='course.add_course',login_url='/'),name='dispatch')
class PubCourse(View):
    def get(self,request):
        context = {
            'categories': CourseCategory.objects.all(),
            'teachers': Teacher.objects.all()
        }
        return render(request, 'cms/courses/pub_course.html', context=context)

    def post(self,request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            teacher_id = form.cleaned_data.get('teacher_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            Course.objects.create(title=title,category=category,teacher=teacher,video_url=video_url,
                                  cover_url=cover_url,price=price,duration=duration,profile=profile)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

# 修改课程；
@method_decorator(permission_required(perm='course.change_course',login_url='/'),name='dispatch')
class EditCourseView(View):
    def get(self,request):
        # course_id 在HTML模板的编辑按钮的url后添加该id；
        course_id = request.GET.get('course_id')
        courses = Course.objects.get(pk=course_id)
        context = {
            'courses': courses
        }
        return render(request,'cms/courses/pub_course.html',context=context)

    def post(self,request):
        form = EditCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            teacher_id = form.cleaned_data.get('teacher_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            pk = form.cleaned_data.get('pk')
            Course.objects.filter(pk=pk).update(title=title,category=category,teacher=teacher,video_url=video_url,
                                  cover_url=cover_url,price=price,duration=duration,profile=profile)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

# 删除课程；
@require_POST
@permission_required(perm='course.delete_course',login_url='/')
def delete_course(request):
    course_id = request.POST.get('course_id')
    Course.objects.filter(pk=course_id).delete()
    return restful.ok()

# 课程分类；
@require_GET
@permission_required(perm='course.add_coursecategory',login_url='/')
def course_category(request):
    categories = CourseCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request,'cms/courses/course_category.html',context=context)

# 添加分类；
@require_POST
@permission_required(perm='course.add_coursecategory',login_url='/')
def add_course_category(request):
    name = request.POST.get('name')
    exists = CourseCategory.objects.filter(name=name).exists()
    if not exists:
        CourseCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已存在！')

# 修改分类；
@require_POST
@permission_required(perm='course.change_coursecategory',login_url='/')
def edit_category(request):
    form = EditCoursecategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        CourseCategory.objects.filter(pk=pk).update(name=name)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())



# 删除分类；
@require_POST
@permission_required(perm='course.delete_coursecategory',login_url='/')
def delete_course_category(request):
    pk = request.POST.get('pk')
    CourseCategory.objects.filter(pk=pk).delete()
    return restful.ok()

# 课程列表；
@method_decorator(permission_required(perm='course.change_course',login_url='/'),name='dispatch')
class CourseListView(View):
    def get(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        # request.GET.get(参数，默认值)
        # 默认值只有在参数没有传递的时候才会使用；如果传递的是一个空的字符串，也不会使用默认值；
        category_id = int(request.GET.get('category',0) or 0)
        courses = Course.objects.select_related('category', 'teacher')
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
            courses = Course.objects.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))
        if title:
            courses = Course.objects.filter(title__icontains=title)
        if category_id:
            courses = Course.objects.filter(category=category_id)
        # 页数默认为1；
        page = int(request.GET.get('p', 1))
        # 分页默认显示2项内容；
        paginator = Paginator(courses, 2)
        # 获取当前页的对象；
        page_obj = paginator.page(page)
        context_data = self.get_pagination_data(paginator, page_obj)
        # 在HTML模板中使用到的数据；
        context = {
            'categories': CourseCategory.objects.all(),
            # 通过‘object_list’得到当前页的数据；
            'courses': page_obj.object_list,
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
        return render(request, 'cms/courses/course_list.html', context=context)

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
