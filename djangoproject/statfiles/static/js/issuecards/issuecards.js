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


var mod = angular.module('issuecards', []);
mod.directive('issueCards', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            issues: "=",
            title: "@"
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

            $scope.getInclude = function(issue){
                var template_sponsored = '/static/js/issuecards/issuecard_sponsored.html';
                var template_proposed = '/static/js/issuecards/issuecard_proposed.html';
                return issue.sponsor_status == 'SPONSORED' ? template_sponsored : template_proposed;
            }

        }
    };
});
