from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse,HttpResponse
from utils import restful
from django.shortcuts import redirect,reverse
from utils.captcha.xfzcaptcha import Captcha
# 内存管道，存储Bytes类型的数据
from io import BytesIO
from utils.aliyunsdk import aliyunsms
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()

# cms登录；
# 1、form表单接收提交的数据，由authenticate进行验证，成功时获得user用户；
# 2、存在用户时判断是否为可用用户（is_active=True），可用时进行登录；
# 3、是否记住密码，设置session到期的值；
@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message="您的账号已经被冻结了！")
        else:
            return restful.params_error(message="手机号或者密码错误！")
    else:
        errors = form.get_errors()
        # {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
        return restful.params_error(message=errors)

# 注销；
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

# 图形验证码；
def img_captcha(request):
    text,image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的数据流；
    out = BytesIO()
    # 调用image的save方法，将image对象保存到BytesIO中；
    image.save(out,'png')
    # 将BytesIO的文件指针移到到最开始的位置;
    out.seek(0)
    response = HttpResponse(content_type='image/png')
    # 从BytesIO管道中，读取出图片数据，保存到response对象上；
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(),text.lower(),5*60)
    return response

# 短信验证码；
def sms_captcha(request):
    # /sms_captcha/?telephone=xxx
    telephone = request.GET.get('telephone')
    code = Captcha.gene_text()
    cache.set(telephone,code,5*60)
    # result = aliyunsms.send_sms(telephone,code)
    # print(result)
    print(code)
    return restful.ok()

# 注册；
@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(username=username,telephone=telephone,password=password)
        login(request,user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())

# 测试cache缓存；
def cache_test(request):
    cache.set('username','zhiliao',60)
    result = cache.get('username')
    print(result)
    return  HttpResponse('success')