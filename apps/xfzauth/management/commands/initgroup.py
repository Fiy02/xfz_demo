from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.news.models import News,NewsCategory,Banner,Comment
from apps.course.models import Course,Teacher,CourseOrder,CourseCategory
from apps.payinfo.models import Payinfo,Payinfo_order

# 用户分组管理
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1、编辑组（管理新闻、课程、评论、轮播图等）
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(Payinfo),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        edit_Group = Group.objects.create(name='编辑组')
        edit_Group.permissions.set(edit_permissions)
        edit_Group.save()
        self.stdout.write(self.style.SUCCESS('编辑组创建成功'))

        # 2、财务组（课程订单、付费资讯订单）
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(Payinfo_order),
        ]
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
        finance_Group = Group.objects.create(name='财务组')
        finance_Group.permissions.set(finance_permissions)
        finance_Group.save()
        self.stdout.write(self.style.SUCCESS('财务组创建成功'))

        # 3、管理员组（编辑组+财务组）
        admin_permissions = edit_permissions.union(finance_permissions)
        admin_Group = Group.objects.create(name='管理员组')
        admin_Group.permissions.set(admin_permissions)
        admin_Group.save()
        self.stdout.write(self.style.SUCCESS('管理员组创建成功'))
