//面向对象
//1、添加属性：
//通过this关键字绑定属性，并指定值；
//Banner相当于类； banner.person = 类.属性
// function Banner() {
//这里的代码相当于python的“__init__”方法的代码
//     console.log('构造函数');
//     this.person = 'jack';
// }
// var banner = new Banner();
// console.log(banner.person);
//2、添加方法：
//在Banner.prototype上绑定方法;
//原型链：  banner.greet = 类.方法
// Banner.prototype.greet = function (word) {
//     console.log("hello ",word);
// };
// banner.greet('jack');
// 轮播图；
function Banner() {
    this.bannerWidth = 798;
    this.bannerGroup = $('#banner-group');
    this.index = 1;
    this.leftArrow = $('.left-arrow');
    this.rightArrow = $('.right-arrow');
    this.bannerUl = $('#banner-ul');
    this.liList = this.bannerUl.children("li");
    this.bannerCount = this.liList.length;
    this.pageControl = $('.page-control');
}

// 初始化轮播图的图片宽度及开始位置，根据bannerCount自动获取其宽度；
Banner.prototype.initBanner = function () {
    var self = this;
    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone();
    self.bannerUl.append(firstBanner);
    self.bannerUl.prepend(lastBanner);
    self.bannerUl.css({'width': self.bannerWidth * (self.bannerCount + 2), 'left': -self.bannerWidth})
};

// 根据图片数量自动生成小圆点数；
Banner.prototype.initPageControl = function () {
    var self = this;
    self.pageControl.css({'width': 2 * 8 + 16 * (self.bannerCount - 1) + 12 * self.bannerCount});
    for (var i = 0; i < self.bannerCount; i++) {
        var circle = $("<li></li>");    //创建li标签；
        self.pageControl.append(circle);
        if (i === 0) {
            circle.addClass("active");
        }
    }
};

//设置图标的显示与隐藏，给bannerGroup属性调用；
Banner.prototype.toggleArrow = function (isshow) {
    var self = this;
    if (isshow) {
        self.leftArrow.show();
        self.rightArrow.show();
    } else {
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

// 轮播并更新小圆点；
Banner.prototype.animate = function () {
    var self = this;
    var index = self.index;
    self.bannerUl.stop().animate({'left': -self.bannerWidth * self.index}, 500);
    if (index === 0) {
        index = self.bannerCount - 1;
    } else if (index === self.bannerCount + 1) {
        index = 0;
    } else {
        index = self.index - 1;
    }
    self.pageControl.children('li').eq(index).addClass("active").siblings().removeClass("active")
};

// setInterval：不断调用函数输出内容，可定义时间；（定时器）
// animate：设置自定义动画效果，往左移动的像素及时间,进行轮播；
// 先找到ID=banner-ul的ul标签，使其每两秒往左移动“-798*index”个像素
Banner.prototype.loop = function () {
    var self = this;
    this.timer = setInterval(function () {
        if (self.index >= self.bannerCount + 1) {
            self.bannerUl.css({'left': -self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    }, 2000);
};

// hover：选择鼠标悬浮的元素；
// clearInterval：可停止定时器的运行；
Banner.prototype.listenBannerHover = function () {
    var self = this;
    this.bannerGroup.hover(function () {
        //第一个函数，鼠标移动到banner上执行的函数；
        clearInterval(self.timer);
        self.toggleArrow(true);
    }, function () {
        //第二个函数，鼠标  从banner上移开执行的函数；
        self.loop();
        self.toggleArrow(false)
    })
};

//鼠标点击箭头进行跳转；
Banner.prototype.listenArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        if (self.index === 0) {
            self.bannerUl.css({'left': -self.bannerCount * self.bannerWidth});
            self.index = self.bannerCount - 1;
        } else {
            self.index--
        }
        self.animate();
    });
    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUl.css({'left': -self.bannerWidth});
            self.index = 2
        } else {
            self.index++
        }
        self.animate();
    })
};

// 监听点击小圆点时跳转的轮播图；
Banner.prototype.listenPageControl = function () {
    var self = this;
    self.pageControl.children("li").each(function (index, obj) {
        $(obj).click(function () {
            self.index = index + 1;
            self.animate();
        })
    })
};

Banner.prototype.run = function () {
    this.initBanner();
    this.initPageControl();
    this.loop();
    this.listenBannerHover();
    this.listenArrowClick();
    this.listenPageControl();
};


// 点击加载更多按钮的事件；
function Index() {
    var self = this;
    self.page = 2;
    self.category_id = 0;
    self.loadBtn = $('#load-more-btn');
}

// 监听加载更多的事件；
Index.prototype.ListenLoadMoreEvent = function () {
    var self = this;
    var loadBtn = $('#load-more-btn');
    loadBtn.click(function () {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'p': self.page,
                'category_id': self.category_id,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data'];
                    if (newses.length > 0) {
                        // template：返回arttemplate模板中定义的内容；template('test',data)；
                        var tpl = template('news-item', {'newses': newses});
                        var ul = $('.list_inner_group');
                        ul.append(tpl);
                        self.page += 1;
                    } else {
                        loadBtn.hide();
                    }
                }
            }
        })
    })
};

// 其它分类的显示事件；
Index.prototype.ListenCategorySwitchEvent = function () {
    var self = this;
    var tabGroup = $('.list_tab');
    tabGroup.children().click(function () {
        // this：代表当前选中的li标签；
        var li = $(this);
        var category_id = li.attr('data-category');
        page = 1;
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'category_id': category_id,
                'p': page,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var newses = result['data'];
                    var tpl = template('news-item', {'newses': newses});
                    var newsListGroup = $('.list_inner_group');
                    // empty：将标签下所有子元素删除；
                    newsListGroup.empty();
                    newsListGroup.append(tpl);
                    self.page = 2;
                    self.category_id = category_id;
                    li.addClass('active').siblings().removeClass('active');
                    self.loadBtn.show();
                }
            }
        })
        
    })
};

Index.prototype.run = function () {
    var self = this;
    self.ListenLoadMoreEvent();
    self.ListenCategorySwitchEvent();
};

// 表示需先运行所有的文本元素后再执行该函数；
$(function () {
    var banner = new Banner();
    banner.run();
    var index = new Index();
    index.run();
});


