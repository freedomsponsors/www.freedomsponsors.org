/**
 *
 Copyright (C) 2013  FreedomSponsors

 The JavaScript code in this page is free software: you can
 redistribute it and/or modify it under the terms of the GNU
 AFFERO GENERAL PUBLIC LICENSE (GNU AGPL) as published by the Free Software
 Foundation, either version 3 of the License, or (at your option)
 any later version.  The code is distributed WITHOUT ANY WARRANTY;
 without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU GPL for more details.

 As additional permission under GNU GPL version 3 section 7, you
 may distribute non-source (e.g., minimized or compacted) forms of
 that code without the copy of the GNU GPL normally required by
 section 4, provided you include this license notice and a URL
 through which recipients can access the Corresponding Source.

 For more information, refer to
 https://github.com/freedomsponsors/www.freedomspons

 ors.org/blob/master/AGPL_license.txt
 */


var mod = angular.module('fswatch', ['fsapi']);

mod.directive('watchEntity', function() {
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