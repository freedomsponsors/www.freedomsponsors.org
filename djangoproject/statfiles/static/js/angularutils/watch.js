angular.module('fswatch', ['fsapi']);

angular.module('fswatch').directive('watchEntity', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            watchLink: '=',
            entity: '@',
            objid: '@',
            watching: '='
        },
        templateUrl: '/static/js/angularutils/watch-issue.html',
        controller: function ($scope, FSApi) {
            $scope.action = function(){
                return $scope.watching ? 'unwatch' : 'watch';
            };

            $scope.showWatchLink = function(){
                return $scope.watchLink.length > 0;
            };

            $scope.toggle = function(){
                if($scope.watchLink){
                    return;
                }
                $scope.loading = true;
                FSApi.toggle_watch($scope.entity, $scope.objid).onResult(function(data){
                    if(data == 'WATCHING'){
                        $scope.watching = true;
                    } else if (data == 'NOT_WATCHING'){
                        $scope.watching = false;
                    } else {
                        alert('unrecognized watch response: '+data);
                    }
                    $scope.loading = false;
                    $scope.$digest();
                });
//                var url = '/core/' + $scope.action() + '/issue/'+$scope.issueId;
//                $.get(url).success(function(data){
//                })
            };
        }
    }
});