function NewsList() {
    
}

// 评论事件；
NewsList.prototype.ListenSubmitEvent =function () {
    var submitBtn = $('.submit-btn');
    var textarea = $("textarea[name='comment']");
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = submitBtn.attr('data-news-id');
        xfzajax.post({
            'url': '/news/public_comment/',
            'data': {
                'content': content,
                'news_id': news_id,
            },
            'success': function (result) {
                if (result['code'] === 200){
                    var comment = result['data'];
                    tpl = template('comment-item',{'comment':comment});
                    var commentList = $('.comment-list');
                    // 将新评论前置；
                    commentList.prepend(tpl);
                    window.messageBox.showSuccess('评论发表成功！');
                    // 输入框填入空白数据；
                    textarea.val("");
                }else{
                    window.messageBox.showError(result['message'])
                }
            }
        })
    })
};

NewsList.prototype.run = function () {
    var self =this;
    self.ListenSubmitEvent();
};

$(function () {
    var news = new NewsList();
    news.run();
});