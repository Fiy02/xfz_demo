from django import forms
from apps.forms import FormMixin
from apps.news.models import News,Banner
from apps.course.models import Course

class EditNewscategoryForm(forms.Form):
    pk = forms.IntegerField(error_messages={'required':'必须传入分类的ID！'})
    name = forms.CharField(max_length=100)

# 发布新闻；
class WriteNewsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['category','author','pub_time']

# 修改新闻；
class EditNewsForm(forms.ModelForm,FormMixin):
    pk = forms.IntegerField()
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category','author','pub_time']

# 后台轮播图管理保存事件表单；
class AddBannerForm(forms.ModelForm,FormMixin):
    class Meta:
        model = Banner
        fields = ('priority','image_url','link_to')


# 修改轮播图；
class EditBannerForm(forms.ModelForm,FormMixin):
    pk = forms.IntegerField()
    priority = forms.IntegerField()
    class Meta:
        model = Banner
        fields = ('link_to','image_url')

# 发布课程；
class PubCourseForm(forms.ModelForm,FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ['category','teacher']

# 编辑课程；
class EditCourseForm(forms.ModelForm,FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ['category','teacher']

# 编辑分类；
class EditCoursecategoryForm(forms.Form,FormMixin):
    pk = forms.IntegerField(error_messages={'required':'必须传入分类的ID！'})
    name = forms.CharField(max_length=100)
