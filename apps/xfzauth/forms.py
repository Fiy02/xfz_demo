from django import forms
from apps.forms import FormMixin
from .models import User
from django.core.cache import cache

class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,error_messages={'max_length':'手机号码错误!'})
    password = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':'密码最多不能超过20个字符！','min_length':'密码最少不能小于6个字符！'})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    password1 = forms.CharField(max_length=20,min_length=6,error_messages={'max_length':'密码最多不能超过20个字符！','min_length':'密码最少不能小于6个字符！'})
    password2 = forms.CharField(max_length=20, min_length=6,error_messages={'max_length': '密码最多不能超过20个字符！','min_length': '密码最少不能小于6个字符！'})
    username = forms.CharField(max_length=20)
    sms_captcha = forms.CharField(max_length=4,min_length=4)
    img_captcha = forms.CharField(max_length=4,min_length=4)
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('两次密码不一致！')
        print(password1)
        print(password2)
        username = cleaned_data.get('username')
        print(username)

        img_captcha = cleaned_data.get('img_captcha')
        cached_img_captcha = cache.get(img_captcha.lower())
        print(img_captcha)
        print(cached_img_captcha)
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            raise forms.ValidationError('图形验证码错误')

        telephone = cleaned_data.get('telephone')
        print(telephone)
        sms_captcha = cleaned_data.get('sms_captcha')
        cached_sms_captcha = cache.get(telephone)

        print(sms_captcha)
        print(cached_sms_captcha)
        if not cached_sms_captcha or cached_sms_captcha.lower() != sms_captcha.lower():
            raise forms.ValidationError('短信验证码错误')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('该手机号已被注册！')