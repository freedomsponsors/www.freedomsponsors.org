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

var mod = angular.module('taglist', ['soapi', 'tagapi']);
mod.directive('taglist', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            tags: "=",
            type: "@",
            objid: "@",
            editable: '='
        },
        templateUrl: '/static/js/tags/taglist.html',
        controller: function ($scope, $timeout, SOApi, TagApi) {
            $scope.poptags = [];
			$scope.editingTags = false;

            var timer = undefined;

            function restartTimer(){
                if(timer){
                    $timeout.cancel(timer);
                }
                timer = $timeout(getTags, 200);
            }

            function getTags(){
				if($scope.newtag.length>0){
					$scope.loading = true;
					SOApi.getTags($scope.newtag).success(function(result){
						$scope.loading = false;
						$scope.poptags = result.items;
					})
				}else{
					$scope.poptags = [];
				}
            }
			
			$scope.editTags = function(){
                $scope.editingTags = true;
				$scope.poptags = [];
				$scope.newtag = null;
				
            };

            $scope.tagChanged = function($event){
                restartTimer();
            };
			
			$scope.focus = function($event){
				if($scope.editingTags){
					$event.currentTarget.getElementsByClassName('newtag')[0].focus();
				}
            };

            $scope.addTag = function(t){
                $scope.tags.push(t.name);
                $scope.poptags = [];
				$scope.newtag = null;
                TagApi.addTag(t.name, $scope.type, $scope.objid);
            };

            $scope.remove = function(index){
                name = $scope.tags.splice(index, 1)[0];
                TagApi.removeTag(name, $scope.type, $scope.objid);
            };
        }
    }
});
