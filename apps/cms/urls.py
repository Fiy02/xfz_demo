from django.urls import path
from . import views,course_views,staff_views

app_name = 'cms'

urlpatterns = [
    path('',views.index,name='index'),
    path('write_news/',views.WriteNewsView.as_view(),name='write_news'),
    path('news_category/',views.news_category,name='news_category'),
    path('add_news_category/',views.add_news_category,name='add_news_category'),
    path('news_list/',views.NewsListView.as_view(),name='news_list'),
    path('edit_news_category/',views.edit_news_category,name='edit_news_category'),
    path('edit_news/',views.EditNewsView.as_view(),name='edit_news'),
    path('delete_news/',views.delete_news,name='delete_news'),
    path('delete_category/',views.delete_category,name='delete_category'),
    path('upload_file/',views.upload_file,name='upload_file'),
    path('qntokon/',views.qntokon,name='qntokon'),
    path('banners/',views.banners,name='banners'),
    path('add_banners/',views.add_banner,name='add_banners'),
    path('banners_list/',views.banner_list,name='banners_list'),
    path('delete_banner/',views.delete_banner,name='delete_banner'),
    path('edit_banner/',views.edit_banner,name='edits_banner'),
]

# 课程管理url；
urlpatterns += [
    path('pub_course/',course_views.PubCourse.as_view(),name='pub_course'),
    path('course_category/',course_views.course_category,name='course_category'),
    path('add_course_category/',course_views.add_course_category,name='add_course_category'),
    path('edit_category/',course_views.edit_category,name='edit_category'),
    path('delete_course_category/',course_views.delete_course_category,name='delete_course_category'),
    path('course_list/',course_views.CourseListView.as_view(),name='course_list'),
    path('edit_course/',course_views.EditCourseView.as_view(),name='edit_course'),
]

# 员工管理url；
urlpatterns += [
    path('staff/',staff_views.staff_views,name='staff'),
    path('add_staff/',staff_views.AddStaffView.as_view(),name='add_staff'),
]