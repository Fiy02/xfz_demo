// 后台课程管理；
function PubCourse() {
    
}

// 使用富文本编辑；
PubCourse.prototype.initUEditor = function(){
    window.ue = UE.getEditor('editor',{
        'serverUrl': '/ueditor/upload/',
        // 指定高度；
        'initialFrameHeight': 300,
    })
};

// 发布课程；
PubCourse.prototype.ListenSubmitEvent = function(){
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var title = $("#title-input").val();
        var category_id = $("#category-input").val();
        var teacher_id = $("#teacher-input").val();
        var video_url = $("#video-input").val();
        var cover_url = $("#cover-input").val();
        var price = $("#price-input").val();
        var duration = $("#duration-input").val();
        var profile = window.ue.getContent();
        xfzajax.post({
            'url': '/cms/pub_course/',
            'data': {
                'title': title,
                'category_id': category_id,
                'teacher_id': teacher_id,
                'video_url': video_url,
                'cover_url': cover_url,
                'price': price,
                'duration': duration,
                'profile': profile
            },
            'success': function (result) {
                if(result['code' === 200]){
                    xfzalert.alertSuccess('恭喜，课程发布成功',function () {
                        window.location = window.location.href();
                    })
                }
            }
        })
    })
};

PubCourse.prototype.run = function () {
    this.initUEditor();
    this.ListenSubmitEvent();
};

$(function () {
    var course = new PubCourse();
    course.run();
});