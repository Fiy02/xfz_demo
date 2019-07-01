function CourseCategory() {

}

CourseCategory.prototype.run = function () {
    this.ListenAddCategoryEvent();
    this.EditCategory();
    this.ListenDeleteCategoryEvent();
};

// 添加分类；
CourseCategory.prototype.ListenAddCategoryEvent = function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '添加课程分类',
            'placeholder': '请输入课程分类',
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/add_course_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            xfzalert.alertSuccess('添加成功！',function () {
                                window.location = window.location.href
                            })
                        } else {
                            xfzalert.close();
                        }
                    }
                })
            }
        })
    })
};

// 编辑分类；
CourseCategory.prototype.EditCategory = function () {
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var current = $(this);
        var tr = current.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        console.log(pk);
        console.log(name);
        xfzalert.alertOneInput({
            'title': '修改分类',
            'placeholder': '请输入新名称',
            'value': name,
            'confirmText': '修改',
            'confirmCallback': function (InputValue) {
                xfzajax.post({
                    'url': '/cms/edit_category/',
                    'data': {
                        'pk': pk,
                        'name': InputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            xfzalert.alertSuccess('‘恭喜，修改成功！', function () {
                                window.location = window.location.href;
                            })
                        } else {
                            xfzalert.close();
                        }
                    }
                })
            }
        })
    })
};

// 删除分类；
CourseCategory.prototype.ListenDeleteCategoryEvent = function () {
    var deleteBtn = $('.delete-btn');
    deleteBtn.click(function () {
        var current = $(this);
        var tr = current.parent().parent();
        var pk = tr.attr('data-pk');
        xfzalert.alertConfirm({
            'title': '是否删除该分类？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_course_category/',
                    'data': {
                        'pk': pk,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            xfzalert.alertSuccess('删除成功！',function () {
                                window.location = window.location.href
                            })
                        } else {
                        }
                    }
                })
            }
        })
    })
};

$(function () {
    var course = new CourseCategory();
    course.run();
});