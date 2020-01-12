/**
 * 定义查询的条件
 * @type {{}}
 */
var queryParams = {
    page: 1,
    pagesize: 10,
    condition: {
        status: '',
        sysname: '',
    }
};

// 获取封装的查询方法
var query = $.pageQuery("/filtersys", "page", "systbody", "tableTemp");


$(function () {
    // 初始化分页查询
    query(queryParams);

    // 模糊查询
    $("#filtersearch").click(function () {
        status = $("#sysstate").val()
        sysname = $("#sysname").val()
        queryParams.condition.status = status
        queryParams.condition.sysname = sysname
        query(queryParams)
    });

    // 刷新页面
     $("#btn_refresh").click(function () {
        location.reload();
    });
});