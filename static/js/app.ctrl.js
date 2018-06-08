
var app = angular.module("myApp", []);

app.controller("appCtrl", [
    "$scope", "$timeout", "$location", "$http",
    function ($scope, $timeout, $location, $http) {

        /* 定义页面参数 */
        $scope.pageData = {
            // 页面标题
            title: "激活",

            // 填写信息
            formInfo: {
                coName      : "",           // 公司名
                userName    : "",           // 用户名
                jobType     : "",           // 职务
                tel         : "",           // 联系电话
                email       : "",           // 邮箱

                // 特征码获取
                featureCode : (function () {
                    var absUrl = $location.$$absUrl;
                    var param = absUrl.split("?")[1];
                    if (!param) { return ""; }
                    return param.split("=")[1];
                })()
            },

            showLoading     : false,        // 显示 加载弹窗
            showRes         : false,        // 显示 是否已经调用接口并返回

            promptSize      : "",

            // TODO 接口返回的信息 需要通过接口 动态赋值
            resInfo: {
                success     : true,
                msg         : "申请已提交，请耐心等待"
            }
        };





        // 提交
        $scope.submit = function () {
            if (!$scope.getValidation()) { return; }

            $scope.pageData.showLoading = true;
            $scope.pageData.showRes = false;

            var formInfo = $scope.pageData.formInfo;
            console.log("提交信息 -> ", formInfo);

            // TODO 模拟调用接口 $http 请求
            $timeout(function () {
                $scope.pageData.showLoading = false;
                $scope.pageData.showRes = true;
            }, 3000);
        };

        // 关闭 H5 页面
        $scope.close = function () {
            WeixinJSBridge.call("closeWindow");
        };

        // 隐藏提示文字
        $scope.hidePromptSize = function () {
            $scope.pageData.promptSize = "";
        };

        // 简单验证提交信息
        $scope.getValidation = function () {
            var pageData = $scope.pageData;
            var formInfo = pageData.formInfo;

            if (!formInfo.coName) {
                pageData.promptSize = "请输入公司名称";
                return false;
            }

            if (formInfo.coName.length < 4) {
                pageData.promptSize = "请输入完整公司名称";
                return false;
            }

            if (!formInfo.userName) {
                pageData.promptSize = "请输入姓名";
                return false;
            }

            if (!formInfo.jobType) {
                pageData.promptSize = "请输入职务";
                return false;
            }

            if (!formInfo.tel) {
                pageData.promptSize = "请输入联系电话";
                return false;
            }

            var reg = new RegExp(/^1(3|4|5|7|8)\d{9}$/);
            if (!reg.test(formInfo.tel)) {
                pageData.promptSize = "请输入正确电话号码";
                return false;
            }

            if (!formInfo.email) {
                pageData.promptSize = "请输入电子邮箱";
                return false;
            }

            reg = new RegExp(/^[A-Za-z0-9_\.\-]+@([_A-Za-z0-9]+\.)+[A-Za-z0-9]{2,3}$/);
            if (!reg.test(formInfo.email)) {
                pageData.promptSize = "请输入正确电子邮箱";
                return false;
            }

            return true;
        };


}]);
