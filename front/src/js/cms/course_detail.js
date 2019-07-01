function CourseDetail() {

}

// 视频播放；
CourseDetail.prototype.initPlayer = function () {
    var videoInfoSpan = $('#video-info');
    var video_url = videoInfoSpan.attr('data-video-url');
    var cover_url = videoInfoSpan.attr('data-cover-url');
    var course_id = videoInfoSpan.attr('data-course-id');
    var player = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: video_url,            // 视频链接；
        image: cover_url,           // 封面图链接；
        autostart: false,           // 是否自动播放；
        stretching: 'uniform',      // 扩大；
        repeat: false,              // 是否重复；
        volume: 100,                // 音量；
        controls: true,             // 底部控制栏；
        primary: "flash",           // 使用flash；
        tokenEncrypt: true,         // 采用token加密；
        ak: '86dc62e1dbd4455080ab1cfc5e587b17', // AccessKey;
    });
    
    // 视频播放前的事件；
    player.on('beforePlay', function (e) {
        if (!/m3u8/.test(e.file)) {
            return;
        }
        xfzajax.get({
            'url': '/course/course_token/',
            'data': {
                'video': video_url,
                'course_id': course_id,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    // 将‘tokon’设置入‘player’中，使播放器获取视频密码；
                    player.setToken(e.file, token);
                } else {
                    window.messageBox.showInfo(result['message'])
                }
            },
            'fail': function (error) {
                console.log(error)
            }
        })
    })
};

CourseDetail.prototype.run = function () {
    this.initPlayer();
};

$(function () {
    var course = new CourseDetail();
    course.run()
});

