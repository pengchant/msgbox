/**
 * 将表单序列化为json对象
 * @returns {{}}
 */
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
}

$.extend({
    /**
     * 延时关闭layui自身
     */
    lay_close_self: function () {
        setTimeout(function () {
            parent.location.reload(true);//刷新父级页面
            var index = parent.layer.getFrameIndex(window.name);
            parent.layer.close(index);
        }, 1100)
    },
    /**
     * 及时关闭模态框
     */
    lay_close_rightnow: function () {
        var index = parent.layer.getFrameIndex(window.name);
        parent.layer.close(index);
    }
})