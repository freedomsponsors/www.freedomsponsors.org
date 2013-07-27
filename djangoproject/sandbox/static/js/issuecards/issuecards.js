var mod = angular.module('issuecards', []);
mod.directive('issueCards', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            issues: "="
        },
        templateUrl: '/static/js/issuecards/issuecards.html',
        controller: function ($scope) {

            $scope.offset = 0;
            $scope.count = 100;

            function load(){
                var params = {
                    offset: $scope.offset,
                    count: 3
                };
                $scope.is_loading = true;
                $.get('/core/json/list_issue_cards', params).success(function(result){
                    result = JSON.parse(result)
                    $scope.count = result.count;
                    $scope.issues = result.issues;
                    $scope.is_loading = false;
                    $scope.$digest();
                })
            }

            $scope.more = function(){
                if(!$scope.no_more()){
                    $scope.offset += 3;
                    load();
                }
            };

            $scope.less = function(){
                if(!$scope.no_less()){
                    $scope.offset -= 3;
                    load();
                }
            };

            $scope.no_more = function(){
                return $scope.offset >= $scope.count - 3;
            };

            $scope.no_less = function(){
                return $scope.offset <= 0;
            };

        }
    };
});
