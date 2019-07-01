function CMSNewsList() {
    
}

// 新闻列表管理的时间搜索;
CMSNewsList.prototype.initDatePicker = function(){
    var startPicker = $('#start-picker');
    var endPicker = $('#end-picker');
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();
    var option = {
        // 显示下方的“今日”与“清除”按钮；
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2019/1/1',
        'endDate': todayStr,
        'language': 'zh-CN',
        // 显示“今日”按钮；
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true,
    };
    startPicker.datepicker(option);
    endPicker.datepicker(option);
};

// 删除新闻；
CMSNewsList.prototype.ListenDeleteEvent = function(){
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var btn = $(this);
        var news_id = btn.attr('data-news-id');
        xfzalert.alertConfirm({
            'text': '您是否要删除该新闻？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_news/',
                    'data': {
                        'news_id': news_id
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location = window.location.href;
                        }
                    }
                })
            }
        })
    })
};

CMSNewsList.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.ListenDeleteEvent();
};

$(function () {
    var newsList = new CMSNewsList();
    newsList.run();
});