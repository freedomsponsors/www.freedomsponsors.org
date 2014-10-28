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