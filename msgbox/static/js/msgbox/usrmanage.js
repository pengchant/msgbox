$(function () {

    // 测试数据
    var zNodes = [
        {id: 1, pId: 0, name: "父节点1 - 展开", open: true},
        {id: 11, pId: 1, name: "父节点11", open: true},
        {id: 111, pId: 11, name: "叶子节点111"},
        {id: 112, pId: 11, name: "叶子节点112"},
        {id: 113, pId: 11, name: "叶子节点113"},
        {id: 114, pId: 11, name: "叶子节点114"},
        {id: 12, pId: 1, name: "父节点12 - 折叠"},
        {id: 121, pId: 12, name: "叶子节点121"},
        {id: 122, pId: 12, name: "叶子节点122"},
        {id: 123, pId: 12, name: "叶子节点123"},
        {id: 124, pId: 12, name: "叶子节点124"},
        {id: 13, pId: 1, name: "父节点13 - 没有子节点", isParent: true},
        {id: 2, pId: 0, name: "父节点2 - 折叠"},
        {id: 21, pId: 2, name: "父节点21 - 展开", open: true},
        {id: 211, pId: 21, name: "叶子节点211"},
        {id: 212, pId: 21, name: "叶子节点212"},
        {id: 213, pId: 21, name: "叶子节点213"},
        {id: 214, pId: 21, name: "叶子节点214"},
        {id: 22, pId: 2, name: "父节点22 - 折叠"},
        {id: 221, pId: 22, name: "叶子节点221"},
        {id: 222, pId: 22, name: "叶子节点222"},
        {id: 223, pId: 22, name: "叶子节点223"},
        {id: 224, pId: 22, name: "叶子节点224"},
        {id: 23, pId: 2, name: "父节点23 - 折叠"},
        {id: 231, pId: 23, name: "叶子节点231"},
        {id: 232, pId: 23, name: "叶子节点232"},
        {id: 233, pId: 23, name: "叶子节点233"},
        {id: 234, pId: 23, name: "叶子节点234"},
        {id: 3, pId: 0, name: "父节点3 - 没有子节点", isParent: true}
    ];


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

    /**
     * 显示menu
     * @param type
     * @param x
     * @param y
     */
    function showRMenu(type, x, y) {
        console.log("右键,,,", type)
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
        console.log("===========================onBeforeRename===========================", treeNode)
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
        console.log("========================onRename====================父节点为:", treeNode.getParentNode(), "current->", treeNode)
        // TODO: 向后台发起（根据id判断是否存在 1：修改节点名称的请求； 2.新增节点请求），将返回的JSON数据重新刷新列表
    }

    /**
     * 删除之前
     * @param treeId
     * @param treeNode
     * @returns {boolean}
     */
    function onBeforeRemove(treeId, treeNode) {
        console.log("=======================onBeforeRemove=================", treeNode);
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
        console.log("============================onRemove==================", treeNode)
        // TODO:(先判断当前节点是否存在id)向后台发起删除节点的请求，将返回的JSON数据重新刷新列表
    }

    /**
     * 当点击节点时
     * @param event
     * @param treeId
     * @param treeNode
     * @param clickFlag
     */
    function onClick(event, treeId, treeNode, clickFlag) {
        console.log("==========CLICK TREE NODE==========", treeNode)
        // TODO:向后台发起相关的数据库操作请求（可选），用于查询数据
    }

    /**
     * 右键显示menu
     * @param event
     * @param treeId
     * @param treeNode
     * @constructor
     */
    function OnRightClick(event, treeId, treeNode) {
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
        var nodes = zTree.getSelectedNodes();
        if (nodes && nodes.length > 0) {
            if (nodes[0].children && nodes[0].children.length > 0) {
                var msg = "要删除的节点是父节点，如果删除将连同子节点一起删掉。\n\n请确认！";
                if (confirm(msg) == true) {
                    zTree.removeNode(nodes[0]);
                }
            } else {
                if (confirm("你确定要删除吗")) {
                    zTree.removeNode(nodes[0]);
                    onRemove(null, null, nodes[0]);
                }
            }
        }
    });

    /**
     * 右键-修改
     */
    $("#m_mod").click(function () {
        hideRMenu();
        var nodes = zTree.getSelectedNodes(), // 获取选择的节点
            treeNode = nodes[0]; // 获取选中的节点
        if (treeNode) {
            zTree.editName(treeNode[0]); // 设置编辑状态
        }
    });

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
     * 初始化组织树
     */
    $.fn.zTree.init($("#treeDemo"), setting, zNodes);
    zTree = $.fn.zTree.getZTreeObj("treeDemo"); // 获取ztree对象
    rMenu = $("#rMenu"); // 获取menu对象


});