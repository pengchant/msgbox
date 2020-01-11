$(function () {

    /**
     * ztree的配置
     * @type {{view: {selectedMulti: boolean, showLine: boolean}, data: {simpleData: {enable: boolean}}, edit: {removeTitle: string, enable: boolean, renameTitle: string, editNameSelectAll: boolean}, callback: {onClick: onClick, onRightClick: OnRightClick, beforeRemove: (function(*, *=): boolean), beforeRename: onBeforeRename, onRemove: onRemove, onRename: onRename}}}
     */
    var setting = {
        edit: { // 设置允许编辑
            enable: true,
            removeTitle: "删除组织", // 删除按钮的提示
            renameTitle: "重命名组织", // 重命名的按钮的提示
            editNameSelectAll: true, // 显示所有编辑
        },
        view: { // 设置line
            showLine: false, // 取消显示下划线
            selectedMulti: false, // 取消多选
        },
        data: {
            simpleData: {
                enable: true // 支持pid前端自动解析
            }
        },
        callback: {
            onClick: onClick, // 点击回调
            beforeRename: onBeforeRename, // 重命名之前事件
            beforeRemove: onBeforeRemove, // 删除之前事件
            onRemove: onRemove, // 删除之后
            onRename: onRename, // 重命名之后
            onRightClick: OnRightClick, // 右键显示menu
        }
    };

    // 组织树的列表
    var zNodes = [];
    // 初始化树状结构
    fetchOrg();
    rMenu = $("#rMenu"); // 获取menu对象
    $.fn.zTree.init($("#treeDemo"), setting, zNodes);

    /**
     * 重新刷新组织树
     * @param zNodes    从后台重新抓数据
     */
    function restTree(zNodes) {
        hideRMenu();
        if (zNodes) {
            $.fn.zTree.init($("#treeDemo"), setting, zNodes);
        }
    }

    /**
     * 抓取组织结构数据
     * @param handler 抓取数据后的回调函数,可以为NULL
     */
    function fetchOrg(handler) {
        $.ajax({
            url: '/allorg',
            type: 'post',
            dataType: 'json',
            async: false,
            contentType: 'application/json; charset=utf-8',
            success: function (result) {
                if (result.re_code == "0") {
                    zNodes = result.data
                    if (handler && handler instanceof Function) {
                        handler()
                    }
                } else {
                    swal("请求加载组织失败，请稍后重试", {
                        buttons: false,
                        timer: 1200
                    })
                }
            }
        })
    }

    /**
     * 新增组织
     * @param name
     * @param pid
     */
    function newOrg(name, pid) {
        $.post('/addorg', {
            'orgname': name,
            'pid': pid
        }, function (result) {
            if (result.re_code == "0") {
                zNodes = result.data
            } else {
                swal(result.msg, {
                    buttons: false,
                    timer: 1200
                })
            }
            restTree(zNodes);
        });
    }

    /**
     * 删除组织
     * @param id
     */
    function delorg(id) {
        $.post('/delorg?orgid=' + id, function (result) {
            if (result.re_code == "0") {
                zNodes = result.data
            } else {
                swal(result.msg, {
                    icon: 'error',
                    button: false,
                    timer: 1200,
                })
            }
            restTree(zNodes);
        });
    }

    /**
     * 重命名组织
     * @param id
     * @param name
     */
    function modifyorg(id, name) {
        $.post("/modiorg", {"id": id, "orgname": name}, function (result) {
            if (result.re_code == "0") {
                zNodes = result.data
            } else {
                swal(result.msg, {
                    buttons: false,
                    timer: 1200
                })
            }
            restTree(zNodes);
        })
    }


    /**
     * 显示menu
     * @param type
     * @param x
     * @param y
     */
    function showRMenu(type, x, y) {
        $("#rMenu ul").show();
        if (type == "root") { // 如果是根节点，则删除，修改隐藏
            $("#m_add").show();
            $("#m_del").hide();
            $("#m_mod").hide();
        } else { // 全部显示
            $("#m_add").show();
            $("#m_del").show();
            $("#m_mod").show();
        }
        rMenu.css({"top": y + "px", "left": x + "px", "visibility": "visible"});
        $("body").bind("mousedown", onBodyMouseDown);
    }

    /**
     * 隐藏menu
     */
    function hideRMenu() {
        if (rMenu) rMenu.css({"visibility": "hidden"});
        $("body").unbind("mousedown", onBodyMouseDown);
    }

    /**
     * 点击menu后隐藏
     * @param event
     */
    function onBodyMouseDown(event) {
        if (!(event.target.id == "rMenu" || $(event.target).parents("#rMenu").length > 0)) {
            rMenu.css({"visibility": "hidden"});
        }
    }


    /**
     * 在重命名之前
     * @param treeId
     * @param treeNode
     * @param newName
     * @param isCancel
     * @returns {boolean}
     */
    function onBeforeRename(treeId, treeNode, newName, isCancel) {
        if (newName.length == 0) {
            setTimeout(function () {
                var zTree = $.fn.zTree.getZTreeObj("treeDemo");
                zTree.cancelEditName();
                alert("节点名称不能为空.");
            }, 0);
            return false;
        }
        return true;
    }

    /**
     * 重命名操作(包含新增)
     * @param e
     * @param treeId
     * @param treeNode
     * @param isCancel
     */
    function onRename(e, treeId, treeNode, isCancel) {
        if (treeNode.id) { // 重命名
            modifyorg(treeNode.id, treeNode.name)
        } else { // 新增节点
            newOrg(treeNode.name, treeNode.getParentNode().id)
        }
    }

    /**
     * 删除之前
     * @param treeId
     * @param treeNode
     * @returns {boolean}
     */
    function onBeforeRemove(treeId, treeNode) {
        var zTree = $.fn.zTree.getZTreeObj("treeDemo");
        zTree.selectNode(treeNode);
        return confirm("确认删除节点吗？");
    }

    /**
     * 删除节点操作
     * @param e
     * @param treeId
     * @param treeNode
     */
    function onRemove(e, treeId, treeNode) {
        delorg(treeNode.id)
    }

    /**
     * 当点击节点时
     * @param event
     * @param treeId
     * @param treeNode
     * @param clickFlag
     */
    function onClick(event, treeId, treeNode, clickFlag) {
        queryParams.condition.orgid = treeNode.id
        query(queryParams)
    }

    /**
     * 右键显示menu
     * @param event
     * @param treeId
     * @param treeNode
     * @constructor
     */
    function OnRightClick(event, treeId, treeNode) {
        var zTree = $.fn.zTree.getZTreeObj("treeDemo");
        // 当点击其他地方取消已有的选择
        if (!treeNode && event.target.tagName.toLowerCase() != "button" && $(event.target).parents("a").length == 0) {
            zTree.cancelSelectedNode();
            showRMenu("root", event.clientX, event.clientY);
        } else if (treeNode && !treeNode.noR) { // 如果当前是节点,显示菜单
            zTree.selectNode(treeNode);
            showRMenu("node", event.clientX, event.clientY);
        }
    }

    // 右键-新增计数
    var newCount = 1;
    /**
     * 右键-新增
     */
    $("#m_add").click(function () {
        hideRMenu();
        var zTree = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = zTree.getSelectedNodes(), // 获取选择的节点
            treeNode = nodes[0]; // 获取选中的节点
        var newNode = {name: '新增' + (newCount++)};
        if (treeNode) { // 如果有节点
            newNode.checked = treeNode.checked;
            treeNode = zTree.addNodes(treeNode, newNode);
        } else { // 如果没有节点
            treeNode = zTree.addNodes(null, newNode);
        }
        if (treeNode) {
            zTree.editName(treeNode[0]);
        } else {
            alert("叶子节点被锁定，无法增加子节点");
        }
    });


    /**
     * 右键-删除
     */
    $("#m_del").click(function () {
        hideRMenu();
        var zTree = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = zTree.getSelectedNodes();
        if (nodes && nodes.length > 0) {
            // if (nodes[0].children && nodes[0].children.length > 0) {
            //     var msg = "要删除的节点是父节点，如果删除将连同子节点一起删掉。\n\n请确认！";
            //     if (confirm(msg) == true) {
            //         zTree.removeNode(nodes[0]);
            //     }
            // } else {
                if (confirm("你确定要删除吗")) {
                    zTree.removeNode(nodes[0]);
                    onRemove(null, null, nodes[0]);
                }
            // }
        }
    });

    /**
     * 右键-修改
     */
    $("#m_mod").click(function () {
        hideRMenu();
        var _zTree = $.fn.zTree.getZTreeObj("treeDemo");
        var nodes = _zTree.getSelectedNodes(), // 获取选择的节点
            treeNode = nodes[0]; // 获取选中的节点
        if (treeNode) {
            _zTree.editName(treeNode); // 设置编辑状态
        }
    });


});