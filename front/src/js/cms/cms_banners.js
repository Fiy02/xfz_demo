// 轮播图管理；
function Banners() {

}

// 添加轮播图以及上限数量；
Banners.prototype.ListenAddBannerEvent = function () {
    var self = this;
    var addBtn = $('#add-banner-btn');
    addBtn.click(function () {
        var bannerListGroup = $('.banner-list-group');
        // 使用‘children’拿到‘bannerListGroup’下所有的子元素，即所有轮播图；
        var length = bannerListGroup.children().length;
        if (length >= 6){
            window.messageBox.showInfo('最多只能添加6张轮播图！');
            return;
        }
        self.CreateBannerItem();
    })
};

// 序列化显示轮播图；
Banners.prototype.LoadData = function(){
    var self = this;
    xfzajax.get({
        'url': '/cms/banners_list/',
        'success': function (result) {
            if (result['code'] === 200){
                var banners = result['data'];
                // 遍历banners中所有的数据，并单独添加到模板中；
                for(var i=0; i<banners.length;i++){
                    var banner = banners[i];
                    self.CreateBannerItem(banner);
                }
            }
        }
    })
};

// 创建bannerItem；
Banners.prototype.CreateBannerItem = function(banner){
    var self = this;
    var tpl = template('banner-item',{'banner':banner});
    // 装载轮播图的盒子；
    var bannerListGroup = $('.banner-list-group');
    var bannerItem = null;
    if(banner){
        // 从数据库遍历出来的数据都往后添加；
        bannerListGroup.append(tpl);
        bannerItem = bannerListGroup.find(".banner-item:last");
    }else{
        // 找到bannerListGroup盒子中的第一个表的数据；
        bannerListGroup.prepend(tpl);
        bannerItem = bannerListGroup.find(".banner-item:first");
    }
    self.AddImageSelectEvent(bannerItem);
    self.AddRemoveBannerEvent(bannerItem);
    self.AddSaveBannerEvent(bannerItem);
};


// 点击图片事件；
Banners.prototype.AddImageSelectEvent = function(bannerItem){
    // 点击图片时相当于点击了隐藏的file文件；
    // var image = bannerItem.find('.thumbnail');
    // image.click(function () {
    //     var that = $(this);
    //     var imageInput = that.siblings('.image-input');
    //     imageInput.click();
    // });
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image-input');
    image.click(function () {
        imageInput.click();
    });
    // 上传文件；
    imageInput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('file',file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200){
                    var url = result['data']['url'];
                    image.attr('src',url);
                }
            }
        })
    })
};

// 点击关闭按钮事件；
Banners.prototype.AddRemoveBannerEvent = function(bannerItem){
    var closeBtn = bannerItem.find('.close-btn');
    closeBtn.click(function () {
        var bannerid = bannerItem.attr('data-banner-id');
        if(bannerid){
            xfzalert.alertConfirm({
                'text': '是否确定删除该轮播图？',
                'confirmCallback': function () {
                    xfzajax.post({
                        'url': '/cms/delete_banner/',
                        'data': {
                            'banner_id': bannerid
                        },
                        'success': function (result) {
                            if (result['code'] === 200){
                                console.log(bannerid);
                                bannerItem.remove();
                                window.messageBox.showSuccess('轮播图删除成功！')
                            }
                        }
                    })
                }
            })
        }else{
            bannerItem.remove();
        }
    })
};

// 点击保存按钮事件；（进行保存或者修改事件）
Banners.prototype.AddSaveBannerEvent = function(bannerItem){
    var self = this;
    var saveBtn = bannerItem.find('.save-btn');
    var prioriySpan = bannerItem.find("span[class=priority]");
    var imageTag = bannerItem.find('.thumbnail');
    var priorityTag = bannerItem.find("input[name='priority']");
    var linktoTag = bannerItem.find("input[name='link_to']");
    var bannerId = bannerItem.attr('data-banner-id');
    var url = '';
    if (bannerId){
        url = '/cms/edit_banner/'
    }
    else{
        url = '/cms/add_banners/'
    }
    saveBtn.click(function () {
        var image_url = imageTag.attr('src');
        var priority = priorityTag.val();
        var link_to = linktoTag.val();
        xfzajax.post({
            'url': url,
            'data': {
                'image_url': image_url,
                'priority': priority,
                'link_to': link_to,
                'pk': bannerId,
            },
            'success': function (result) {
                if (result['code'] === 200){
                    if(bannerId){
                        bannerItem.attr('priority',priority);
                        window.messageBox.showSuccess('轮播图修改成功。')
                    }else{
                        // 这里不能使用var定义bannerID，它会在if前添加‘var bannerId = undefind’使该值为空；
                        bannerId = result['data']['banner_id'];
                        // 给属性‘data-banner-id’添加‘bannerID’的值，不然后期无法获取该图的‘bannerId’进行修改操作；
                        bannerItem.attr('data-banner-id',bannerId);
                        window.messageBox.showSuccess('添加成功！');
                    }
                    // 修改优先级span标签的内容；
                    prioriySpan.text('优先级：'+ priority);
                }
            }
        })
    })
};

// 运行；
Banners.prototype.run = function () {
    var self = this;
    self.ListenAddBannerEvent();
    self.LoadData();
};

$(function () {
    var banners = new Banners();
    banners.run();
});