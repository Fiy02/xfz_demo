// 导航栏上的点击事件；
function FrontBase(){

}

FrontBase.prototype.run = function () {
    var self = this;
    self.listenAuthBoxHover();
};

// 处理用户个人中心的打开和隐藏；
FrontBase.prototype.listenAuthBoxHover = function () {
    var authBox = $('.auth-box');
    var userMoreBox = $('.user-more-box');
    authBox.hover(function () {
        userMoreBox.show();
    },function () {
        userMoreBox.hide();
    });
};

// 处理登录与注册；
function Auth() {
    var self = this;
    self.maskWrapper = $('.mask-wrapper');
    self.scrollWrapper = $('.scroll-wrapper');
    self.switchBtn = $('.switch');
    self.smsCaptcha = $('.SMS-captcha-btn');
}

// 点击打开登录注册框；
Auth.prototype.showEvent = function(){
    var self = this;
    self.maskWrapper.show();
};

// 关闭隐藏；
Auth.prototype.hideEvent = function(){
    var self = this;
    self.maskWrapper.hide();
};

// 监听打开登录注册及关闭按钮的事件；
Auth.prototype.listenShowHideEvent = function(){
    var self = this;
    var signinBtn = $('.signin-btn');
    var signupBtn = $('.signup-btn');
    var closeBtn = $('.close-btn');
    signinBtn.click(function () {
        self.showEvent();
        self.scrollWrapper.css({'left':0})
    });
    signupBtn.click(function () {
        self.showEvent();
        self.scrollWrapper.css({'left':-400})
    });
    closeBtn.click(function () {
        self.hideEvent();
    });
};

// 登录与注册的切换；
Auth.prototype.listenSwitchEvent = function () {
    var self = this;
    self.switchBtn.click(function () {
        // 当前打开窗口的位置，注册窗口<0<登录窗口；
        var currentLeft = self.scrollWrapper.css('left');
        currentLeft = parseInt(currentLeft);
        if(currentLeft < 0 ){
           self.scrollWrapper.animate({'left':'0'})
        }else{
           self.scrollWrapper.animate({'left':'-400px'})
        }
    });
};


// 登录；
Auth.prototype.listenSigninEvent = function () {
    var self = this;
    var signinGroup = $('.signin-group');
    var telephoneInput = signinGroup.find("input[name='telephone']");
    var passwordInput = signinGroup.find("input[name='password']");
    var rememberInput = signinGroup.find("input[name='remember']");

    var submitBtn = signinGroup.find(".submit-btn");
    submitBtn.click(function () {
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var remember = rememberInput.prop("checked");

        xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember?1:0
            },
            'success': function (result) {
                console.log(12111);
                window.location.reload();
            }
        });
    });
};

// 注册；
Auth.prototype.listenRegisterEvent = function(){
    var signupGroup = $('.signup-group');
    var submitBtn = signupGroup.find('.submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();     // 取消默认事件；
        var telephoneInput = signupGroup.find("input[name='telephone']");
        var usernameInput = signupGroup.find("input[name='username']");
        var password1Input = signupGroup.find("input[name='password1']");
        var password2Input = signupGroup.find("input[name='password2']");
        var imgCaptchaInput = signupGroup.find("input[name='img_captcha']");
        var smsCaptchaInput = signupGroup.find("input[name='sms_captcha']");
    
        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var img_captcha = imgCaptchaInput.val();
        var sms_captcha = smsCaptchaInput.val();
        xfzajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'username': username,
                'password1': password1,
                'password2': password2,
                'img_captcha': img_captcha,
                'sms_captcha': sms_captcha,
            },
            'success': function (result) {
                    window.location.reload();
            }
        })
    });
};

// 图形验证码点击事件；
Auth.prototype.listenImageCaptchaEvent  = function(){
    var imgCaptcha = $(".img-captcha");
    imgCaptcha.click(function () {
        imgCaptcha.attr("src","/account/img_captcha/"+"?random="+Math.random())
    });
};

// 成功发送短信验证码；
Auth.prototype.smsSuccessEvent = function(){
    var self = this;
    messageBox.showSuccess('短信验证码发送成功！');
    self.smsCaptcha.addClass('disabled');   // 添加另一个表示无法点击的类的样式；
    var count = 60;
    self.smsCaptcha.unbind('click');    // 解除点击事件；
    var timer = setInterval(function () {
        self.smsCaptcha.text(count+'s');
        count -= 1;
        if(count<=0){
            clearInterval(timer);
            self.smsCaptcha.removeClass('disabled');
            self.smsCaptcha.text('发送验证码');
            self.listenSmsCaptchaEvent();
        }
    },1000);
};

// 短信验证码点击事件；
Auth.prototype.listenSmsCaptchaEvent = function(){
    var self = this;
    var telephoneInput = $(".signup-group input[name='telephone']");
    self.smsCaptcha.click(function () {
        var telephone = telephoneInput.val();
        if(!telephone){
            messageBox.showInfo('请输入手机号码！');
        }
        xfzajax.get({
            'url': '/account/sms_captcha/',
            'data': {
                'telephone': telephone,
            },
            'success': function (result) {
                    self.smsSuccessEvent();
            },
        });
    });
};
// 运行；
Auth.prototype.run = function () {
    var self = this;
    self.listenShowHideEvent();
    self.listenSwitchEvent();
    self.listenSigninEvent();
    self.listenImageCaptchaEvent();
    self.listenSmsCaptchaEvent();
    self.listenRegisterEvent();
};

$(function () {
    var auth = new Auth();
    auth.run();
});

$(function () {
    var frontBase = new FrontBase();
    frontBase.run();
});

$(function () {
    if(window.template){
        // 使用arttemplate模板需重新定义时间过滤器；
        template.defaults.imports.timeSince = function (dateValue) {
            var date = new Date(dateValue);
            var datets = date.getTime();             //得到的是毫秒；
            var nowts = (new Date()).getTime();      // 得到当前时间戳；
            var timestamp = (nowts - datets) / 1000;   //除以1000得到秒；
            if (timestamp < 60) {
                return '刚刚';
            } else if (timestamp >= 60 && timestamp < 60 * 60) {
                minutes = parseInt(timestamp / 60);
                return minutes + '分钟前';
            } else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
                hours = parseInt(timestamp / 60 / 60);
                return hours + '小时前';
            } else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
                days = parseInt(timestamp / 60 / 60 / 24);
                return days + '天前';
            } else {
                var year = date.getFullYear();
                var month = date.getMonth();
                var day = date.getDay();
                var hour = date.getHours();
                var minutes = date.getMinutes();
                return year + '/' + month + '/' + day + ' ' + hour + ':' + minutes;
            }
        };
    }
});