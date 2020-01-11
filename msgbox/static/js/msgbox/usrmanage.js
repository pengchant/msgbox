$(function () {

    /**
     * 定义查询的条件
     * @type {{}}
     */
    var queryParams = {
        page: 1,
        pagesize: 10,
        condition: {
            usrname: '',
            workerid: '',
            orgid: '',
        }
    };
    // 获取封装的查询方法
    var query = $.pageQuery("/filterusrinfo", "page", "usrtbody", "tableTemp");
    // 初始化分页查询
    query(queryParams)
});