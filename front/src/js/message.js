// 错误消息提示框

function Message() {
    var self = this;
    self.isAppended = false;
    self.wrapperHeight = 48;
    self.wrapperWidth = 350;
    self.initStyle();
    self.initElement();     // 初始化元素；
    self.listenCloseEvent();
}

// 定义各类提示框的显示颜色；
Message.prototype.initStyle = function () {
    var self = this;
    self.errorStyle = {
        'wrapper':{
            'background': '#f2dede',
            'color': '#993d3d'
        },
        'close':{
            'color': '#993d3d'
        }
    };
    self.successStyle = {
        'wrapper':{
            'background': '#dff0d8',
            'color': '#468847'
        },
        'close': {
            'color': "#468847"
        }
    };
    self.infoStyle = {
        'wrapper': {
            'background': '#d9edf7',
            'color': '#5bc0de'
        },
        'close': {
            'color': '#5bc0de'
        }
    }
};

// 提示框的样式；
Message.prototype.initElement = function () {
    var self = this;
    // 创建div用来存储错误消息；
    self.wrapper = $("<div></div>");
    self.wrapper.css({
        'padding': '10px',
        'font-size': '14px',
        'width': '350px',
        'position': 'fixed',
        'z-index': '10000',
        'left': '50%',
        'top': '-48px',
        'margin-left':'-150px',
        'height': '48px',
        'box-sizing': 'border-box',
        'border': '1px solid #ddd',
        'border-radius': '4px',
        'line-height': '24px',
        'font-weight': 700
    });
    // 关闭按钮；
    self.closeBtn = $("<span>×</span>");
    self.closeBtn.css({
        'font-family': 'core_sans_n45_regular,"Avenir Next","Helvetica Neue",Helvetica,Arial,"PingFang SC","Source Han Sans SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi MicroHei",sans-serif;',
        'font-weight': '700',
        'float': 'right',
        'cursor': 'pointer',
        'font-size': '22px'
    });
    // 用来存储错误消息的文本；
    self.messageSpan = $("<span class='xfz-message-group'></span>");

    self.wrapper.append(self.messageSpan);
    self.wrapper.append(self.closeBtn);
};

// 关闭时错误框上移，即隐藏到页面后面；
Message.prototype.listenCloseEvent = function () {
    var self = this;
    self.closeBtn.click(function () {
        self.wrapper.animate({"top":-self.wrapperHeight});
    });
};

Message.prototype.showError = function (message) {
    this.show(message,'error');
};

Message.prototype.showSuccess = function (message) {
    this.show(message,'success');
};

Message.prototype.showInfo = function (message) {
    this.show(message,'info');
};

// 添加错误信息并将错误框像下移动，显示在页面中；
Message.prototype.show = function (message,type) {
    var self = this;
    if(!self.isAppended){
        $(document.body).append(self.wrapper);
        self.isAppended = true;
    }
    self.messageSpan.text(message);
    if(type === 'error') {
        self.wrapper.css(self.errorStyle['wrapper']);
        self.closeBtn.css(self.errorStyle['close']);
    }else if(type === 'info'){
        self.wrapper.css(self.infoStyle['wrapper']);
        self.closeBtn.css(self.infoStyle['close']);
    }else{
        self.wrapper.css(self.successStyle['wrapper']);
        self.closeBtn.css(self.successStyle['close']);
    }
    self.wrapper.animate({"top":0},function () {
        setTimeout(function () {
            self.wrapper.animate({"top":-self.wrapperHeight});
        },3000);
    });
};

// 将Message对象绑定到window窗口，一个全局对象；
window.messageBox = new Message();