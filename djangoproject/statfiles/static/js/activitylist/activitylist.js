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

angular.module('activitylist', ['fsapi']);
angular.module('activitylist').directive('activitylist', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            projectId: '@'
        },
        templateUrl: '/static/js/activitylist/activitylist.html',
        controller: function ($scope, FSApi) {

            $scope.activities = [];

            var instrument = function(activity){
                try{
                    activity.new_dic = JSON.parse(activity.new_json);
                    activity.old_dic = JSON.parse(activity.old_json);
                } catch(err){
                    //that's ok
                }
            };

            var more = function(){
                $scope.loading = true;
                FSApi.get_latest_activity($scope.projectId, $scope.activities.length).onResult(function(result){
                    $scope.loading = false;
                    $scope.activities = $scope.activities.concat(result.activities);
                    $scope.count = result.count;
                    for(var i=0; i < $scope.activities.length; i++){
                        instrument($scope.activities[i])
                    }
                    $scope.$digest();
                });
            };

            more();

            $scope.show_more = function(){
                return $scope.activities.length < $scope.count;
            };

            $scope.more = function(){
                more();
            }

            $scope.show_detail = function(activity){
                $scope.selected_activity = activity;
                $('#activity_detail').modal()
            }
        }
    }
});
