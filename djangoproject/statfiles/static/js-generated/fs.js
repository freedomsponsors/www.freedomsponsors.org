if(!window.FS){
    window.FS = {};
}
if(!FS.dependencies){
    FS.dependencies = [];
}

angular.module('fs', FS.dependencies).config(
    function($interpolateProvider, $httpProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }
);

angular.module('fsapi', []);

angular.module('fsapi').factory('FSApi', function(){

    function list_issues(project_id, sponsoring, offset, count){
        var params = {
            project_id: project_id,
            sponsoring: sponsoring,
            offset: offset,
            count: count
        };
        return fs_ajax_async_result($.get, '/core/json/list_issue_cards', params)
    }

    function get_latest_activity(project_id, offset){
        var params = {
            project_id: project_id,
            offset: offset
        };
        return fs_ajax_async_result($.get, '/core/json/latest_activity', params)
    }

    function toggle_watch(entity, objid){
        var params = {
            entity: entity,
            objid: objid
        };
        return fs_ajax_async_result($.post, '/core/json/toggle_watch', params)
    }

    function check_username_availability(username){
        return fs_ajax_async_result($.get, '/core/json/check_username_availability/'+username)
    }

    return {
        list_issues: list_issues,
        get_latest_activity: get_latest_activity,
        toggle_watch: toggle_watch,
        check_username_availability: check_username_availability
    };
});

angular.module('fslinks', []);

angular.module('fslinks').factory('FSLinks', function(){

    function issue_link(issue){
        return issue.issue_link;
    }

    return {
        issue_link: issue_link
    };
})

function fs_timeout_async_result(result){
    var callback = undefined;
    var r = {
        onResult: function(cb){
            callback = cb;
        }
    };
    setTimeout(function(){
        callback(result)
    }, 1000);
    return r;
}


function fs_ajax_async_result(func, url, params){
    var r = {
        onResult: function(callback){
            r.callback = callback;
            return r;
        },
        onError: function(errorcallback){
            r.errorcallback = errorcallback;
            return r;
        }
    };
    func(url, params)
        .success(function(result){
            if (r.callback) {
                if(result){
                    try {
                        result = JSON.parse(result);
                    } catch(err){}
                }
                r.callback(result)
            }
        })
        .error(function(e){
            if (r.errorcallback) {
                r.errorcallback(e)
            }            
        });
    return r;
}

function get4Sponsors(issue){
    var empties = [];
    for(var i=0; i<4 - issue.four_sponsors.length; i++){
        empties.push({empty:true});
    }
    return empties.concat(issue.four_sponsors)
}


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

angular.module('angularutils', []);
angular.module('angularutils').directive('textWithMarkdownPreview', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            model:'=',
            nameid:'@',
            placeholder:'@'
        },
        templateUrl: '/static/js/angularutils/textarea-and-markdownpreview.html',
        controller: function ($scope) {
            $scope.markdown = function(s){
                var converter = new Showdown.converter();
                var html = converter.makeHtml(s);
                return html;
            }
        }
    }
});

angular.module('angularutils').directive('watchIssue', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            watchLink: '@',
            issueId: '@',
            watching: '='
        },
        templateUrl: '/static/js/angularutils/watch-issue.html',
        controller: function ($scope) {
            $scope.action = function(){
                return $scope.watching ? 'unwatch' : 'watch';
            };

            $scope.toggle = function(){
                if($scope.watchLink){
                    return;
                }
                var url = '/core/' + $scope.action() + '/issue/'+$scope.issueId;
                $scope.loading = true;
                $.get(url).success(function(data){
                    if(data == 'WATCHING'){
                        $scope.watching = true;
                    } else if (data == 'NOT_WATCHING'){
                        $scope.watching = false;
                    } else {
                        alert('unrecognized watch response: '+data);
                    }
                    $scope.loading = false;
                    $scope.$digest();
                })
            };
        }
    }
});

angular.module('angularutils').directive('multilineEllipsis', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            var $container = $(element).find('.ellipsis');
            var divh = $(element).height();
            setTimeout(function(){
                while ($container.outerHeight() > divh) {
                    $container.text(function (index, text) {
                        if(text.length > 400){
                            text = text.substring(0, 400);
                        }
                        var result = text.replace(/\W*\s(\S)*$/, '...');
                        if (result == text){
                            result = text.substring(0, text.length - 4)+'...';
                        }
                        return result;
                    });
                }
            }, 0);

        }
    };
});

angular.module('angularutils').directive('sortHeader', function () {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            label: '@',
            property: '@'
        },
        templateUrl: '/static/js/angularutils/sortHeader.html',
        controller: function ($scope, SortHeaderModel) {
            $scope.m = SortHeaderModel;
            $scope.toggle = function(){
                SortHeaderModel.toggle($scope.property);
            };
        }
    };
});


angular.module('angularutils').factory('SortHeaderModel', function (){
    var self = {
        property: null,
        asc: true
    };
    self.toggle = function(property){
        if(self.property == property){
            self.asc = !self.asc;
        } else {
            self.property = property;
        }
        if(self.onchange){
            self.onchange(self.property, self.asc);
        }
    };
    self.init = function(property, asc){
        self.property = property;
        self.asc = asc;
    };
    return self;
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
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
angular.module('contenteditable', []).
	directive('contenteditable', function () {
	return {
		restrict: 'A', // only activate on element attribute
		require: '?ngModel', // get a hold of NgModelController
		link: function (scope, element, attrs, ngModel) {
			if (!ngModel) return; // do nothing if no ng-model

			// Specify how UI should be updated
			ngModel.$render = function () {
				element.html(ngModel.$viewValue || '');
			};

			// Listen for change events to enable binding
			element.on('blur keyup change', function () {
				scope.$apply(readViewText);
			});

			// No need to initialize, AngularJS will initialize the text based on ng-model attribute

			// Write data to the model
			function readViewText() {
				var html = element[0].innerHTML;
				// When we clear the content editable the browser leaves a <br> behind
				// If strip-br attribute is provided then we strip this out
				if (attrs.stripBr) {
					html = html.replace(/<br>/g,"");
					element[0].innerHTML = html; // Firefox replaces caret at beginning after this
					placeCaretAtEnd(element[0]); // So we fix it here, otherwise if you type "html" you will get "lmth"
				}
				ngModel.$setViewValue(html);
			}
			
			// Places de caret at de end of element
			function placeCaretAtEnd(element) {
				element.focus();
				if (typeof window.getSelection != "undefined"
						&& typeof document.createRange != "undefined") {
					var range = document.createRange();
					range.selectNodeContents(element);
					range.collapse(false);
					var sel = window.getSelection();
					sel.removeAllRanges();
					sel.addRange(range);
				} else if (typeof document.body.createTextRange != "undefined") {
					var textRange = document.body.createTextRange();
					textRange.moveToElementText(element);
					textRange.collapse(false);
					textRange.select();
				}
			}
		}
	};
});
angular.module('issuecards', ['fsapi', 'fslinks', 'angularutils']);
angular.module('issuecards').directive('issueCards', function() {
    return {
        restrict: 'E',
        replace: true,
        scope:{
            issues: "=",
            label: "@",
            sponsoring: '@',
            projectId: '@'
        },
        templateUrl: '/static/js/issuecards/issuecards.html',
        controller: function ($scope, $rootScope, FSApi, FSLinks) {

            var is_sponsoring = $scope.sponsoring == 'true';

            $scope.offset = 0;
            $scope.count = 100;

            function load(){
                $scope.is_loading = true;
                FSApi.list_issues($scope.projectId, is_sponsoring, $scope.offset, 3).onResult(function(result){
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
                return _mixedValue(issue.total_paid_offers_usd, issue.total_paid_offers_usd);
            };

            $scope.getOfferedValue = function(issue){
                return _mixedValue(issue.total_open_offers_usd, issue.total_open_offers_btc);
            };

            $scope.getTitlePaid = function(issue){
                return _mixedTitle(issue.total_paid_offers_usd, issue.total_paid_offers_usd);
            };

            $scope.getTitleOffered = function(issue){
                return _mixedTitle(issue.total_open_offers_usd, issue.total_open_offers_btc);
            };
        }
    };
});

angular.module('soapi', []);

angular.module('soapi').factory('SOApi', function($http){
    var get_tags = "https://api.stackexchange.com/2.1/tags";


    function getTags(s){
        return $http({
            url: get_tags,
            method: "GET",
            params: {
                order: 'desc',
                sort: 'popular',
                inname: s,
                site: 'stackoverflow'
            }
        });
    }

    return {
        getTags: getTags
    };
})

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


angular.module('tagapi', []);

angular.module('tagapi').factory('TagApi', function($http) {
    var add_tag = '/core/json/add_tag';
    var remove_tag = '/core/json/remove_tag';

    function addTag(name, objtype, objid){
        return $http({
            method: 'POST',
            url: add_tag,
            data: $.param({
                name: name,
                objtype: objtype,
                objid: objid
            })
        })
    }
    function removeTag(name, objtype, objid){
        return $http({
            method: 'POST',
            url: remove_tag,
            data: $.param({
                name: name,
                objtype: objtype,
                objid: objid
            })
        })
    }

    return {
        addTag: addTag,
        removeTag: removeTag
    }
});

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

angular.module('taglist', ['soapi', 'tagapi']);
angular.module('taglist').directive('taglist', function() {
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

angular.module('fs').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('/static/js/activitylist/activitylist.html',
    "<div><div ng-repeat=\"activity in activities\"><div ng-switch on=activity.action><div ng-switch-when=EDIT_PROJECT><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.username }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>edited project details.</span> <a href ng-click=show_detail(activity)>View changes &raquo;</a></div></div></div></div></div><div ng-switch-when=PROJECT_ADD_TAG><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.username }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>added tag <span class=tag-list><span class=tag>{[{ activity.new_json }]}</span></span> to project.</span></div></div></div></div></div><div ng-switch-when=PROJECT_REMOVE_TAG><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.username }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>removed tag <span class=tag-list><span class=tag>{[{ activity.new_json }]}</span></span> from project.</span></div></div></div></div></div><div ng-switch-when=SPONSOR><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.username }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text><span class=green-text>sponsored</span> issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a> with a <span class=green-text>{[{ activity.new_dic.currency }]} {[{ activity.new_dic.price }]} offer</span>.</span></div></div></div></div></div><div ng-switch-when=CHANGE_OFFER><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.username }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>changed an offer on issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a> from <span class=green-text>USD 10</span> to <span class=green-text>USD 20</span>.</span></div></div></div></div></div><div ng-switch-when=REVOKE><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>revoked an <span class=green-text>{[{ activity.new_dic.currency }]} {[{ activity.new_dic.price }]} offer</span> on issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a>. Why?</span> <a href ng-click=show_detail(activity)>View comment &raquo;</a></div></div></div></div></div><div ng-switch-when=PROPOSE><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>proposed issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a>.</span></div><div class=\"card-status open\" style=bottom:0></div></div></div></div></div><div ng-switch-when=WORK><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>started working on issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a><span ng-hide=activity.issue_comment_content>.</span><span ng-show=activity.issue_comment_content>and added a comment.</span> <a href ng-click=show_detail(activity) ng-show=activity.issue_comment_content>View comment &raquo;</a></span></div><div style=width:100px></div></div><div class=\"card-status working\" style=bottom:0></div></div></div></div><div ng-switch-when=ABORT><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>stopped working on issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a>.</span><span ng-show=activity.issue_comment_content>Why?</span> <a href ng-click=show_detail(activity) ng-show=activity.issue_comment_content>View comment &raquo;</a></div></div></div></div></div><div ng-switch-when=RESOLVE><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>resolved issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a><span ng-hide=activity.issue_comment_content>.</span><span ng-show=activity.issue_comment_content>and added a comment.</span> <a href ng-click=show_detail(activity) ng-show=activity.issue_comment_content>View comment &raquo;</a><div class=\"card-status done\" style=bottom:0></div></span></div></div></div></div></div><div ng-switch-when=ADD_ISSUE_COMMENT><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>added a comment on issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a>.</span> <a href ng-click=show_detail(activity)>View comment &raquo;</a></div></div></div></div></div><div ng-switch-when=EDIT_ISSUE_COMMENT><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>edited a comment on issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a>.</span> <a href ng-click=show_detail(activity)>View changes &raquo;</a></div></div></div></div></div><div ng-switch-when=PAY><div class=column-wrapper><div class=\"fs-box column fit\"><div class=\"column-wrapper vcenter-content\" style=height:50px><div class=column><div class=user-picture><a href=\"{[{ activity.user_link }]}\"><img ng-src={[{activity.user_image}]}></a></div></div><div class=hgap-15></div><div class=\"column fit\"><div class=arial><a href=\"{[{ activity.user_link }]}\" class=font-size-14 title=\"Click to see user profile\">{[{ activity.user_screenname }]}</a><div class=\"hgap-10 inline\"></div><span class=\"light-grey-text font-size-12\" title=\"{[{ activity.creationDate }]}\">{[{ activity.when }]}</span></div><div class=vgap-5></div><span class=light-grey-text>made a <span class=green-text>{[{ activity.payment.currency }]} {[{ activity.payment.total }]} payment</span> for issue <a href=\"{[{ activity.issue.link }]}\">{[{ activity.issue.title }]}</a>.</span></div></div><div class=vgap-15></div><div class=reply-area><div ng-repeat=\"part in activity.payment.parts\"><div class=\"column-wrapper vcenter-content\" style=height:40px><div style=width:50px class=text-align-right><div><img class=\"user-picture thumb40\" ng-src={[{part.programmer_image}]}></div></div><div class=hgap-15></div><div class=\"column fit\"><h4 class=\"arial no-margin font-size-12\"><a href=\"{[{ part.programmer_link }]}\">{[{ part.programmer_screenname }]}</a></h4><div class=vgap-5></div><span>received<span class=green-text>{[{ activity.payment.currency }]} {[{ part.price }]}</span></span></div></div><div ng-if=!$last class=vgap-15></div></div></div></div></div></div><div ng-switch-default>Unknown activity: {[{activity.action }]}</div></div><div class=vgap-15></div></div><div ng-show=loading><img src=/static/img2/ajax-loader.gif></div><div ng-show=show_more()><a href ng-click=more() class=\"fs-button grey\">More...</a></div><div class=\"modal fade in\" id=activity_detail><div class=\"modal-dialog column-wrapper vertical\"><div class=\"column fit\"></div><div class=modal-content><div class=modal-header><button type=button class=close onclick=\"$('#activity_detail').modal('hide')\">&times;</button> <span class=\"modal-title font-size-20 ubahn grey-text\">{[{ selected_activity.action }]}</span></div><div class=\"divider small\"></div><div class=modal-body><div ng-switch on=selected_activity.action><div ng-switch-when=EDIT_PROJECT><ul><li>old image: {[{ selected_activity.old_dic.image3x1 }]}</li><li>new image: {[{ selected_activity.new_dic.image3x1 }]}</li><li>old home URL: {[{ selected_activity.old_dic.homeURL }]}</li><li>new home URL: {[{ selected_activity.new_dic.homeURL }]}</li><li>old description:<br><pre>{[{ selected_activity.old_dic.description }]}</pre></li><li>new description:<br><pre>{[{ selected_activity.new_dic.description }]}</pre></li></ul></div><div ng-switch-when=CHANGE_OFFER><ul><li>old value: {[{ selected_activity.old_dic.currency }]} {[{ selected_activity.old_dic.price }]}</li><li>new value: {[{ selected_activity.new_dic.currency }]} {[{ selected_activity.new_dic.price }]}</li><li>old acceptance criteria:<br><pre>{[{ selected_activity.old_dic.acceptanceCriteria }]}</pre></li><li>new acceptance criteria:<br><pre>{[{ selected_activity.new_dic.acceptanceCriteria }]}</pre></li></ul></div><div ng-switch-when=REVOKE>Revoke comment:<pre>\n" +
    "                                {[{ selected_activity.issue_comment_content }]}\n" +
    "                            </pre></div><div ng-switch-when=WORK>Work start comment:<pre>\n" +
    "                                {[{ selected_activity.issue_comment_content }]}\n" +
    "                            </pre></div><div ng-switch-when=ABORT>Abort work comment:<pre>\n" +
    "                                {[{ selected_activity.issue_comment_content }]}\n" +
    "                            </pre></div><div ng-switch-when=RESOLVE>Resolve comment:<pre>\n" +
    "                                {[{ selected_activity.issue_comment_content }]}\n" +
    "                            </pre></div><div ng-switch-when=ADD_ISSUE_COMMENT>New comment:<pre>\n" +
    "                                {[{ selected_activity.issue_comment_content }]}\n" +
    "                            </pre></div><div ng-switch-when=EDIT_ISSUE_COMMENT><ul><li>old comment:<br><pre>{[{ selected_activity.old_dic.content }]}</pre></li><li>new comment:<br><pre>{[{ selected_activity.new_dic.content }]}</pre></li></ul></div></div></div><div class=\"modal-footer inline-content\"><div class=\"column-wrapper vcenter-content\" style=height:28px><div class=\"hgap-15 inline\"></div><div><a href=# onclick=\"$('#activity_detail').modal('hide')\" class=\"fs-button green medium\">OK</a></div></div></div></div><div class=\"column fit\"></div></div></div></div>"
  );


  $templateCache.put('/static/js/angularutils/sortHeader.html',
    "<span><a href ng-click=toggle()>{[{label}]} <i ng-show=\"property == m.property\" ng-class=\"{'icon-chevron-up': m.asc, 'icon-chevron-down': !m.asc}\"></i></a></span>"
  );


  $templateCache.put('/static/js/angularutils/textarea-and-markdownpreview.html',
    "<div><textarea id=\"{[{ nameid }]}\" name=\"{[{ nameid }]}\" ng-model=model placeholder=\"{[{ placeholder }]}\"></textarea><p class=help-block>You can use <a target=_markdown href=\"http://blog.freedomsponsors.org/markdown_formatting/\">markdown</a> for formatting</p><div id=bootstrap-content ng-bind-html-unsafe=markdown(model)></div></div>"
  );


  $templateCache.put('/static/js/angularutils/watch-issue.html',
    "<span><a class=\"iconized watch\" ng-show=showWatchLink() href={[{watchLink}]}>{[{ action() }]}</a> <a class=\"iconized {[{ action() }]}\" ng-hide=showWatchLink() href ng-click=toggle()>{[{ action() }]}</a> <img src=/static/img2/ajax-loader.gif ng-show=loading></span>"
  );


  $templateCache.put('/static/js/issuecards/issuecard_proposed.html',
    "<div class=\"fs-box push-footer issue-card proposed\"><a href=\"{[{ issue_link(issue) }]}\" multiline-ellipsis class=\"font-size-18 darkblue-text ubahn issue-title\"><div class=ellipsis>{[{ issue.title }]}</div></a><div class=\"divider small\"></div><a href=\"{[{ issue.project_link }]}\"><div class=project-logo title=\"{[{ issue.project_name }]}\">linefix<img ng-src=\"{[{ issue.image_link }]}\"></div></a> <div class=\"orange-text sponsors-label\" align=right>No sponsors yet</div><div class=vgap-15></div><div multiline-ellipsis class=issue-description><p class=ellipsis ng-show=issue.description>{[{ issue.description }]}</p><p ng-hide=issue.description>[No description]</p></div><div class=vgap-15></div><a href=\"\" class=\"fs-button green\">Sponsor now!</a> <div class=\"fs-box-footer card-footer\"><div class=column-wrapper><span class=views></span> <span class=comments><a href=\"{[{ issue_link(issue) }]}\"><span class=comments-number>{[{ issue.commentcount }]}</span><span>comments</span></a></span></div></div></div>"
  );


  $templateCache.put('/static/js/issuecards/issuecard_sponsored.html',
    "<div class=\"fs-box push-footer issue-card sponsored\"><a href=\"{[{ issue_link(issue) }]}\" multiline-ellipsis class=\"font-size-18 darkblue-text ubahn issue-title\"><div class=ellipsis>{[{ issue.title }]}</div></a><div class=\"divider small\"></div><div class=column-wrapper><div class=\"column fit font-size-12\"><span class=paid-value title={[{getTitlePaid(issue)}]}>{[{ getPaidValue(issue) }]}</span><span>Paid</span></div><div class=\"column fit font-size-12 orange-text\" align=right><span class=offered-value title={[{getTitleOffered(issue)}]}>{[{ getOfferedValue(issue) }]}</span><span>Offered</span></div></div><div class=card-sponsors><div class=column-wrapper><div class=user-picture ng-class=\"{placeholder: sponsor.empty}\" ng-repeat=\"sponsor in issue.four_sponsors_places\"><a href=\"{[{ sponsor.sponsor_link }]}\"><img ng-hide=sponsor.empty ng-src=\"{[{ sponsor.image_link }]}\" alt=\"{[{ sponsor.username }]}\" title=\"{[{ sponsor.username }]}\"></a></div></div><a href=\"{[{ issue_link(issue) }]}\" class=sponsors-label>{[{ getMoreSponsors(issue) }]}</a></div><div multiline-ellipsis class=issue-description><p class=ellipsis ng-show=issue.description>{[{ issue.description }]}</p><p ng-hide=issue.description>[No description]</p></div><a href=\"{[{ issue.project_link }]}\"><div class=project-logo title=\"{[{ issue.project_name }]}\">linefix<img ng-src=\"{[{ issue.image_link }]}\"></div></a>  <a href=\"{[{ issue_link(issue) }]}\"><div class=\"card-status {[{ issue.status }]}\"></div></a> <div class=\"fs-box-footer card-footer\"><div class=column-wrapper><div class=\"column fit\"></div><div class=\"column fit\" align=right><a href=\"{[{ issue_link(issue) }]}\"><span class=comments-number>{[{ issue.commentcount }]}</span><span>comments</span></a></div></div></div></div>"
  );


  $templateCache.put('/static/js/issuecards/issuecards.html',
    "<div class=card-list-section><div class=card-list-header><h3 class=\"boxed medium\">{{ label }}</h3><a href class=\"fs-button square grey less\" ng-class=\"{'disabled' : no_less()}\" ng-click=less()>&laquo;</a> <a href class=\"fs-button square grey more\" ng-class=\"{'disabled' : no_more()}\" ng-click=more()>&raquo;</a> <img ng-show=is_loading src=/static/img2/ajax-loader.gif> <a href=\"/search/?project_id={[{ projectId }]}&operation={[{getViewAllOperation()}]}\" class=\"fs-button medium grey view-all right\">View All</a></div><div class=column-wrapper><div ng-repeat=\"issue in issues\" ng-include=getInclude()></div></div></div>"
  );


  $templateCache.put('/static/js/tags/taglist.html',
    "<div><a class=\"iconized tag right\" ng-hide=editingTags ng-click=editTags() style=margin:2px>edit tags</a> <a class=\"iconized done right\" ng-show=editingTags ng-click=\"editingTags=false\" style=margin:2px>done</a><div class=clearfix></div><div ng-class={fakeinput:editingTags} ng-click=focus($event)><span href class=tag ng-repeat=\"tag in tags\">{[{tag}]} <a href ng-show=editingTags ng-click=remove($index)>x</a></span><div style=position:relative!important;display:inline-block><span ng-show=editingTags><span class=newtag contenteditable=true strip-br=true ng-model=newtag ng-keypress=tagChanged($event) ng-change=tagChanged($event)></span><div class=poptags><div class=\"fs-box poptags\" ng-show=poptags><ul><li ng-repeat=\"poptag in poptags\" ng-click=addTag(poptag)><span class=no-wrap>{{ poptag.name }}</span></li></ul></div></div><img src=/static/img2/ajax-loader.gif ng-show=loading></span></div></div></div>"
  );

}]);
