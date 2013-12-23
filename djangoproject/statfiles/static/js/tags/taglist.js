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
 https://github.com/freedomsponsors/www.freedomsponsors.org/blob/master/AGPL_license.txt
 */

var mod = angular.module('taglist', ['soapi' /*'tagsapi'*/]);
mod.directive('taglist', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            type: "@",
            objid: "@"
        },
        templateUrl: '/static/js/tags/taglist.html',
        controller: function ($scope, $timeout, SOApi /*, TagApi, SOApi*/) {
            $scope.tags = ["java", "python"];
            $scope.poptags = [];

            var timer = undefined;

            function restartTimer(){
                if(timer){
                    $timeout.cancel(timer);
                }
                timer = $timeout(getTags, 200);
            }

            function getTags(){
                $scope.loading = true;
                SOApi.getTags($scope.newtag).success(function(result){
                    $scope.loading = false;
                    $scope.poptags = result.items;
                })
            }

            $scope.keypress = function(){
                restartTimer();
            };

            $scope.addTag = function(t){
                $scope.tags.push(t.name);
                $scope.poptags = [];
            }
        }
    }
});
