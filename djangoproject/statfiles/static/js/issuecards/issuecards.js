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


var mod = angular.module('issuecards', ['fsapi', 'fslinks', 'angularutils']);
mod.directive('issueCards', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            issues: "=",
            label: "@",
            sponsoring: '@'
        },
        templateUrl: '/static/js/issuecards/issuecards.html',
        controller: function ($scope, $rootScope, FSApi, FSLinks) {

            var is_sponsoring = $scope.sponsoring == 'true';

            $scope.offset = 0;
            $scope.count = 100;

            function load(){
                $scope.is_loading = true;
                FSApi.list_issues(is_sponsoring, $scope.offset, 3).onResult(function(result){
                    $scope.count = result.count;
                    $scope.issues = result.issues;
                    $scope.is_loading = false;

                    if(is_sponsoring){
                        for(var i=0; i < $scope.issues.length; i++){
                            var issue = $scope.issues[i];
                            issue.four_sponsors_places = get4Sponsors(issue);
                        }
                    }

                    $rootScope.$digest();
                });
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

            $scope.get4Sponsors = function(issue){
                var empties = [];
                for(var i=0; i<4 - issue.four_sponsors.length; i++){
                    empties.push({empty:true});
                }
                return empties.concat(issue.four_sponsors)
            };

            $scope.getMoreSponsors = function(issue){
                var n = issue.four_sponsors.length;
                if(n == 0){
                    return "No sponsors";
                } else if (n == 1) {
                    return "1 sponsor";
                } else if (n < 4) {
                    return n+" sponsors";
                } else if (n == 4){
                    if(issue.moresponsors){
                        return "and "+issue.moresponsors+" more sponsors";
                    } else {
                        return "4 sponsors";
                    }
                } else {
                    return 'ERROR';
                }
            };

            $scope.getInclude = function(){
                var template_sponsored = '/static/js/issuecards/issuecard_sponsored.html';
                var template_proposed = '/static/js/issuecards/issuecard_proposed.html';
                return is_sponsoring ? template_sponsored : template_proposed;
            };

            $scope.getViewAllOperation = function(){
                return is_sponsoring ? 'SPONSOR' : 'KICKSTART';
            };

            $scope.issue_link = function(issue){
                return FSLinks.issue_link(issue);
            };

            function _mixedValue(usd, btc){
                usd = parseFloat(usd);
                btc = parseFloat(btc);
                if(btc == 0){
                    return "US$ " + usd.toFixed(2);
                } else if(usd == 0){
                    return "BTC " + btc + "*";
                }
                var btcusd = BTC2USD * btc;
                var usdbtc = usd / BTC2USD;
                if(usd > btcusd){
                    return "US$ "+(usd + btcusd).toFixed(2)+"*";
                } else {
                    return "BTC "+(btc + usdbtc).toFixed(3)+"*";
                }
            }

            function _mixedTitle(usd, btc){
                usd = parseFloat(usd);
                btc = parseFloat(btc);
                if(usd > 0 && btc == 0){
                    return ""
                } else if(btc > 0 && usd == 0) {
                    return "(1BTC = US$" + BTC2USD.toFixed(2) + ")"
                } else {
                    return "BTC " + btc + " + " + "US$ " + usd + "(1BTC = US$" + BTC2USD.toFixed(2) + ")"
                }
            }


            $scope.getPaidValue = function(issue){
                return _mixedValue(issue.totalPaidPriceUSD, issue.totalPaidPriceBTC);
            };

            $scope.getOfferedValue = function(issue){
                return _mixedValue(issue.totalOffersPriceUSD, issue.totalOffersPriceBTC);
            };

            $scope.getTitlePaid = function(issue){
                return _mixedTitle(issue.totalPaidPriceUSD, issue.totalPaidPriceBTC);
            };

            $scope.getTitleOffered = function(issue){
                return _mixedTitle(issue.totalOffersPriceUSD, issue.totalOffersPriceBTC);

            };

        }
    };
});
