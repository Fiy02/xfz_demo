function News() {

}

News.prototype.run = function () {
    var self = this;
    self.ListenUploadFileEvent();
    // self.ListenQiniuuploadFileEvent();
    self.initUEditor();
    self.ListenSubmitEvent();
};

// 上传到自己的服务器；
News.prototype.ListenUploadFileEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200){
                    var url = result['data']['url'];
                    var thumbnailInput = $('#thumbnail-form');
                    thumbnailInput.val(url);
                }
            }
        })
    });
};

// 上传到七牛云；
News.prototype.ListenQiniuuploadFileEvent = function(){
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntokon/',
            'success': function (result) {
                if (result['code'] ===200 ){
                    
                    // token: 上传验证信息，前端通过接口请求后端获得；
                    var tokon = result['data']['tokon'];
                    
                    // key: 文件资源名(当前时间+文件格式);
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1];
                    
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png','image/jpeg','image/gif','video/x-ms-wmv','video/mp4','video/x-flv']
                    };
                    
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z2
                    };
                    
                    // 文件上传；
                    var observable = qiniu.upload(file,key,tokon,putExtra,config);
                    observable.subscribe({
                        'next': self.handFileUploadProcess,
                        'error': self.handFileUploadError,
                        'complete': self.handFileUploadComplete,
                    })
                }
            }
        })
    })
};

// 接收上传进度；
News.prototype.handFileUploadProcess = function(response){
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed() + '%';
    var progressGroup = News.progressGroup;
    progressGroup.show();
    var progressBar = $('.progress-bar');
    progressBar.css({"width":percentText});
    progressBar.text(percentText);
};

// 接收错误触发；
News.prototype.handFileUploadError = function(error){
    window.messageBox.showError(error.message);
    var progressGroup = News.progressGroup;
    progressGroup.hide();
    console.log(error.message);
};

// 接收上传完成后的返回信息；
News.prototype.handFileUploadComplete = function(response){
    console.log(response);
    var progressGroup = News.progressGroup;
    progressGroup.hide();
    var domain = 'http://ps96zui1h.bkt.clouddn.com/';
    var filename = response.key;
    var url = domain + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url)
};

// 富文本编辑；
News.prototype.initUEditor = function(){
    window.ue = UE.getEditor('editor',{
        'serverUrl': '/ueditor/upload/',
        'initialFrameHeight': 300,
    })
};

// 提交新闻按钮；
News.prototype.ListenSubmitEvent = function(){
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-news-id');
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        var url = '';
        if (pk){
            url = '/cms/edit_news/'
        }else{
            url = '/cms/write_news/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'desc': desc,
                'category': category,
                'content': content,
                'thumbnail': thumbnail,
                'pk': pk
            },
            'success': function (result) {
                if (result['code'] === 200){
                    xfzalert.alertSuccess('恭喜，新闻发表成功！',function () {
                        window.location.reload();
                    })
                }
            }
        })
    });
};

$(function () {
    var news = new News();
    news.run();
    News.progressGroup = $('#progress-group');
});
