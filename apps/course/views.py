from django.shortcuts import render
from .models import Course, CourseCategory, CourseOrder,Teacher
from django.http import Http404
from django.conf import settings
import time, os, hmac, hashlib
from utils import restful
from apps.xfzauth.decorators import xfz_login_required
from hashlib import md5
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt

# 课程首页；
def course_index(request):
    context = {
        'courses': Course.objects.all(),
        'categories': CourseCategory.objects.all()
    }
    return render(request, 'course/course_index.html', context=context)


# 获取特定‘ID’的课程详情；
def course_detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
        context = {
            'course': course,
            'buyed': buyed
        }
        return render(request, 'course/course_detail.html', context=context)
    except Course.DoesNotExist:
        raise Http404


# 获取tokon；（对应course_detail.js文件）
def course_token(request):
    # video：是视频文件的完整链接
    file = request.GET.get('video')
    # 判断用户是否已购买；
    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists():
        return restful.params_error(message="请先购买课程！")
    # 过期时间2小时；（当前时间戳+两个小时）；
    expiration_time = int(time.time()) + 2 * 60 * 60
    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    # 先获取扩展名；再通过‘/’分割取最后一个值，并将扩展名替换为空字符串；得到‘ID’；
    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    # 将‘USER_KEY’进行编码；后面的‘hmac.new()’只能接受bytes类型；
    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')

    # signature：生成签名；
    # disgestmod：指定加密方式；
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()

    # 利用下划线(_)连接signature，userId，expirationTime组合成token = String.format(“ % s_ % s_ % s”, signature, userId，expirationTime)
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})


# 购买课程；
@xfz_login_required
def course_order(request, course_id):
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.create(course=course, buyer=request.user, status=1, amount=course.price)
    context = {
        'goods': {
            'thumbnail': course.cover_url,
            'title': course.title,
            'price': course.price
        },
        'order': order,
        # 跳转链接：/course/notify_url/；
        'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
        'return_url': request.build_absolute_uri(reverse('course:course_detail', kwargs={"course_id": course.pk}))
    }
    return render(request, 'course/course_order.html', context=context)


# 获取“key”；用户登录的情况下；
@xfz_login_required
def course_order_key(request):
    goodsname = request.POST.get("goodsname")       # 商品名称;
    istype = request.POST.get("istype")             # 支付渠道；
    notify_url = request.POST.get("notify_url")     # 通知回调网址；
    orderid = request.POST.get("orderid")           # 商户自定义订单号；
    orderuid = str(request.user.pk)                 # 商户自定义客户号；
    price = request.POST.get("price")               # 价格；
    return_url = request.POST.get("return_url")     # 跳转网址；

    # 在官网个人账户设置中的“API接口信息”中获取“token”与“uid”的值:
    token = 'e6110f92abcb11040ba153967847b7a6'
    uid = '49dc532695baa99e16e01bc0'

    # 秘钥“key”的拼接顺序：goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    return restful.result(data={"key": key})


# 使用订单ID更新支付状态；（关闭CSRF保护）
@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()
