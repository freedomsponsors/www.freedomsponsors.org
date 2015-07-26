angular.module("fstemplates", []).run(["$templateCache", function($templateCache) {$templateCache.put("TEMPLATE_CACHE/editprofile/fseditprofile.html","<div>EDIT PROFILE</div>");
$templateCache.put("TEMPLATE_CACHE/home/fshome.html","<div><h1>FreedomSponsors. Crodfunding Free software, one issue at a time</h1><span>sponsored issues...</span> <span>proposed issues...</span></div>");
$templateCache.put("TEMPLATE_CACHE/issue/fsissue.html","<div>ISSUE</div>");
$templateCache.put("TEMPLATE_CACHE/login/fslogin.html","<div><div><input type=\"text\" placeholder=\"username\" ng-model=\"m.username\"></div><div><input type=\"password\" placeholder=\"password\" ng-model=\"m.password\"></div><button ng-click=\"m.login()\">OK</button> <span ng-show=\"m.loading\">loading...</span><h3>Social authentication</h3><div><a rel=\"nofollow\" href=\"/login/google-openidconnect?next=/spa\">Google</a><br><a rel=\"nofollow\" href=\"/login/github?next=/spa\">Github</a><br><a rel=\"nofollow\" href=\"/login/bitbucket?next=/spa\">Bitbucket</a><br><a rel=\"nofollow\" href=\"/login/facebook?next=/spa\">Facebook</a><br><a rel=\"nofollow\" href=\"/login/twitter?next=/spa\">Twitter</a><br><a rel=\"nofollow\" href=\"/login/yahoo?next=/spa\">Yahoo</a><br></div></div>");
$templateCache.put("TEMPLATE_CACHE/pages/docs.html","<html><head><meta name=\"viewport\" content=\"initial-scale=1\"><link rel=\"stylesheet\" href=\"./css/lib.css\"><link rel=\"stylesheet\" href=\"./css/fs.css\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=RobotoDraft:300,400,500,700,400italic\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/icon?family=Material+Icons\"><script src=\"./js/lib.js\"></script><!--FSJS--><!--FSJS END--><script>DOCS.angular_dependencies = [\'fsdocs\'];\n            FSDOCS.angular_dependencies = [];\n            if(FS.USE_TEAMPLE_CACHE){\n                DOCS.angular_dependencies.push(\'fstemplates\');\n                DOCS.angular_dependencies.push(\'docstemplates\');\n            }</script><!--DOCSJS--><!--DOCSJS END--><!--FSDOCSJS--><!--FSDOCSJS END--><script>angular.module(\'fsdocs\', FSDOCS.angular_dependencies);</script></head><body ng-app=\"docs_main\" layout=\"column\"><div layout=\"row\" flex><md-sidenav layout=\"column\" class=\"md-sidenav-left md-whiteframe-z2\" md-component-id=\"left\" md-is-locked-open=\"true\"><component-catalog-tree group=\"fs\"></component-catalog-tree></md-sidenav><div layout=\"column\" flex id=\"content\"><div ui-view></div></div></div></body></html>");
$templateCache.put("TEMPLATE_CACHE/pages/index.html","<html><head><meta name=\"viewport\" content=\"initial-scale=1\"><link rel=\"stylesheet\" href=\"./css/lib.css\"><link rel=\"stylesheet\" href=\"./css/fs.css\"><link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css?family=RobotoDraft:300,400,500,700,400italic\"><script src=\"./js/lib.js\"></script><!--FSJS--><!--FSJS END--></head><body ng-app=\"fs_main\" layout=\"column\" ng-controller=\"FSMainCtrl\"><md-toolbar layout=\"row\"><fstoolbar></fstoolbar></md-toolbar><div layout=\"row\" flex><div layout=\"column\" flex id=\"content\"><md-content layout=\"column\" flex class=\"md-padding\"><div ui-view></div></md-content></div></div></body></html>");
$templateCache.put("TEMPLATE_CACHE/project/fslistprojects.html","<div>PROJECT LIST</div>");
$templateCache.put("TEMPLATE_CACHE/project/fsproject.html","<div>PROJECT</div>");
$templateCache.put("TEMPLATE_CACHE/search/fssearch.html","<div><div><input type=\"text\" ng-model=\"m.searchform.text\" ng-keypress=\"$event.keyCode == 13 && m.search()\"> <span ng-show=\"m.loading\">loading...</span></div><div><table><tr><th>Project</th><th>Title</th></tr><tr ng-repeat=\"issue in m.issues\"><td>{[{issue.project_name}]}</td><td>{[{issue.title}]}</td></tr></table></div></div>");
$templateCache.put("TEMPLATE_CACHE/sponsor/fssponsor.html","<div>SPONSOR</div>");
$templateCache.put("TEMPLATE_CACHE/viewuser/fsviewuser.html","<div><div ng-if=\"m.loading\">loading...</div><div ng-if=\"!m.loading\"><div>login: {[{m.user.username}]}</div><div>name: {[{m.user.name}]}</div><div>Paypal: {[{m.user.has_paypal}]}</div><div>Bitcoin: {[{m.user.has_bitcoin}]}</div></div></div>");
$templateCache.put("TEMPLATE_CACHE/components/todo_example/todo.html","<div><md-content layout=\"row\" layout-sm=\"column\"><md-input-container><label>New task</label><input ng-model=\"m.newtodo\"></md-input-container><md-button class=\"md-raised md-primary\" ng-click=\"m.add()\">Add</md-button><md-progress-circular ng-if=\"m.adding\" md-mode=\"indeterminate\"></md-progress-circular></md-content><ul class=\"todo\"><li ng-repeat=\"todo in m.todos\"><span>{[{todo.description}]}</span><md-button class=\"md-raised\" ng-click=\"m.remove(todo)\">Remove</md-button></li></ul></div>");
$templateCache.put("TEMPLATE_CACHE/components/toolbar/fstoolbar.html","<div class=\"md-toolbar-tools\"><h1><a ui-sref=\"home\">FreedomSponsors</a></h1><a class=\"md-button\" ui-sref=\"listprojects\">Projects</a> <a class=\"md-button\" ui-sref=\"search\">Search</a> <a class=\"md-button\" href>etc</a> <span flex></span> <a class=\"md-button\" ui-sref=\"viewuser({login: auth.user.username})\" ng-if=\"auth.authenticated()\">{[{auth.user.username}]} <a><a class=\"md-button\" hreff ng-click=\"auth.logout()\" ng-if=\"auth.authenticated()\">Logout <a><a class=\"md-button\" ui-sref=\"login\" ng-if=\"!auth.authenticated()\">Login</a></a></a></a></a></div>");}]);
if(!window.FS){
    window.FS = {};
}
FS.BASE_URL = 'TEMPLATE_CACHE/';
FS.USE_TEAMPLE_CACHE = true;

if(!window.DOCS){
    window.DOCS = {};
}
DOCS.BASE_URL = 'TEMPLATE_CACHE/';
DOCS.SAMPLE_BASE_URL = './docs_samples/';

if(!window.FSDOCS){
    window.FSDOCS = {};
}
if(!FSDOCS.angular_dependencies){
	FSDOCS.angular_dependencies = [];
}

if(!window.FS){
	window.FS = {};
}

window.jsutils = {};

jsutils.has_ng_module = function(name){
	try{
		angular.module(name);
		return true;
	} catch(ex){
		return false;
	}
};
angular.module('fsngutils', []);
(function(){
	var deps = [
		'ngMaterial',
		'ui.router',
		'fsngutils',
		'fstoolbar',
		'fshome',
		'fslogin',
		'fsissue',
		'fsproject',
		'fslistprojects',
		'fssearch',
		'fssponsor',
		'fsviewuser',
		'fseditprofile',
		'fsapi',
	];
	if(FS.USE_TEAMPLE_CACHE){
		deps.push('fstemplates');
	}
	angular.module('fs_main', deps);

	angular.module('fs_main').config(function($interpolateProvider, $stateProvider, $urlRouterProvider) {
	    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');

	    $urlRouterProvider.otherwise('/');

	    $stateProvider
	        .state('home', {url: '/', template: '<fshome></fshome>'})
	        .state('login', {url: '/login', template: '<fslogin></fslogin>'})
	        .state('issue', {url: '/issue/:id/:slug', template: '<fsissue></fsissue>', controller: 'IssueStateCtrl'})
	        .state('project', {url: '/project/:id/:slug', template: '<fsproject></fsproject>', controller: 'ProjectStateCtrl'})
	        .state('listprojects', {url: '/project', template: '<fslistprojects></fslistprojects>'})
	        .state('search', {url: '/search', template: '<fssearch></fssearch>', controller: 'SearchStateCtrl'})
	        .state('sponsor', {url: '/sponsor', template: '<fssponsor></fssponsor>', controller: 'SponsorStateCtrl'})
	        .state('viewuser', {url: '/user/:login', template: '<fsviewuser></fsviewuser>', controller: 'ViewUserStateCtrl'})
	        .state('editprofile', {url: '/editprofile', template: '<fseditprofile></fseditprofile>'});
	});

	angular.module('fs_main').controller('FSMainCtrl', function($scope, FSAuth){
	});
})();

angular.module('fsauth', ['fsapi']);

angular.module('fsauth').factory('FSAuth', function(FSApi){
	var auth = {
		user: null,
		authenticated: authenticated,
		set_user: set_user,
		logout: logout,
	};

	function authenticated(){
		return auth.user !== null && auth.user !== undefined;
	}

	function set_user(user){
		auth.user = user;
	}

	function logout(){
		FSApi.logout().then(function(){
			auth.user = null;
		});
	}

	function _check_for_authentication(){
		FSApi.whoami().then(function(result){
			var _who = result.data;
			if(_who.authenticated){
				auth.user = _who.user;
			} else {
				auth.user = null;
			}
		});
	}

	_check_for_authentication();

	return auth;
});
angular.module('fsajax', ['ngCookies']);

angular.module('fsajax').config(
    function($httpProvider){
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    }
);

angular.module('fsajax').factory('FSAjax', function($http, $cookies, $log){

    var FSAjax = {
        get: get,
        post: post,
    };

    function get(url, params){
        if(!params){
            params = {};
        }
        return $http({
            method: 'GET',
            url: url,
            params: params
        });
    }

    function post(url, params){
        if(!params){
            params = {};
        }
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
        return $http({
            method: 'POST',
            url: url,
            data: $.param(params)
        });
    }

    return FSAjax;
});

angular.module('fseditprofile', ['fsapi']);

angular.module('fseditprofile').factory('FSEditProfileModel', function(FSApi){
	var m = {};

	return m;
});

angular.module('fseditprofile').directive('fseditprofile', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'editprofile/fseditprofile.html',
		controller: function($scope, FSEditProfileModel){

		},
	};
});
angular.module('fshome', ['fsapi']);

angular.module('fshome').factory('FSHomeModel', function(FSApi){
	var m = {};

	return m;
});

angular.module('fshome').directive('fshome', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'home/fshome.html',
		controller: function($scope, FSHomeModel){

		},
	};
});
angular.module('fsissue', ['fsapi']);

angular.module('fsissue').factory('FSIssueModel', function(FSApi){
	var m = {};

	return m;
});

angular.module('fsissue').controller('IssueStateCtrl', function($scope, $stateParams, FSIssueModel){

});

angular.module('fsissue').directive('fsissue', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'issue/fsissue.html',
		controller: function($scope, FSIssueModel){

		},
	};
});
angular.module('fslogin', ['fsapi']);

angular.module('fslogin').factory('FSLoginModel', function(FSAuth, FSApi, $state){
	var m = {
		username: '',
		password: '',
		loading: false,
		login: login,
	};

	function login(){
		m.loading = true;
		FSApi.login(m.username, m.password).then(function(result){
			var logged_user = result.data;
			if(logged_user){
				FSAuth.set_user(result.data);
				$state.go('home');
			} else {
				alert('wrong credentials');
			}
		}).finally(function(){
			m.loading = false;
		});
	}

	return m;
});

angular.module('fslogin').directive('fslogin', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'login/fslogin.html',
		controller: function($scope, FSLoginModel){
			$scope.m = FSLoginModel;
		},
	};
});

angular.module('fslistprojects', ['fsapi']);

angular.module('fslistprojects').factory('FSListProjectsModel', function(FSApi){
	var m = {};

	return m;
});

angular.module('fslistprojects').directive('fslistprojects', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'project/fslistprojects.html',
		controller: function($scope, FSListProjectsModel){

		},
	};
});
angular.module('fsproject', ['fsapi']);

angular.module('fsproject').factory('FSProjectModel', function(FSApi){
	var m = {};

	return m;
});

angular.module('fsproject').controller('ProjectStateCtrl', function($scope, $stateParams, FSProjectModel){

});

angular.module('fsproject').directive('fsproject', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'project/fsproject.html',
		controller: function($scope, FSProjectModel){

		},
	};
});
angular.module('fssearch', ['fsapi']);

angular.module('fssearch').factory('FSSearchModel', function(FSApi){
	var m = {
		searchform: {
			text: ''
		},
		loading: false,
		issues: []
	};
	angular.extend(m, {
		search: search
	});

	function search(evt){
		m.loading = true;
		FSApi.list_issues({q: m.searchform.text}).then(function(result){
			m.issues = result.data;
		}).finally(function(){
			m.loading = false;
		});
	}

	return m;
});

angular.module('fssearch').controller('SearchStateCtrl', function($scope, $stateParams, FSSearchModel){

});

angular.module('fssearch').directive('fssearch', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'search/fssearch.html',
		controller: function($scope, FSSearchModel){
			var m = $scope.m = FSSearchModel;
		},
	};
});

angular.module('fssponsor', ['fsapi']);

angular.module('fssponsor').factory('FSSponsorModel', function(FSApi){
	var m = {};

	return m;
});

angular.module('fssponsor').controller('SponsorStateCtrl', function($scope, $stateParams, FSSponsorModel){

});

angular.module('fssponsor').directive('fssponsor', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'sponsor/fssponsor.html',
		controller: function($scope, FSSponsorModel){

		},
	};
});
angular.module('fsviewuser', ['fsapi']);

angular.module('fsviewuser').factory('FSViewUserModel', function(FSApi){
	var m = {
		loading: false,
		user: null,
		load: load,
	};

	function load(username){
		m.loading = true;
		FSApi.get_user_details(username).then(function(result){
			m.user = result.data;
		}).finally(function(){
			m.loading = false;
		});
	}

	return m;
});

angular.module('fsviewuser').controller('ViewUserStateCtrl', function($scope, $stateParams, FSViewUserModel){
	var login = $stateParams.login;
	FSViewUserModel.load(login);
});

angular.module('fsviewuser').directive('fsviewuser', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'viewuser/fsviewuser.html',
		controller: function($scope, FSViewUserModel){
			$scope.m = FSViewUserModel;
		},
	};
});
angular.module('ng_bind_html_unsafe', []);
angular.module('ng_bind_html_unsafe').directive('ngBindHtmlUnsafe', ['$sce', function ($sce) {
    return function (scope, element, attr) {
        element.addClass('ng-binding').data('$binding', attr.ngBindHtmlUnsafe);
        scope.$watch(attr.ngBindHtmlUnsafe, function ngBindHtmlUnsafeWatchAction(value) {
            element.html(value || '');
        });
    };
}]);


//This is a toy component to demonstrate how to make them

angular.module('todo', ['fsapi']);

angular.module('todo').factory('TODOModel', function(FSApi){
    var m = {
        newtodo: '',
        adding: false,
        todos: [],
    };

    angular.extend(m, {
        add: add,
        remove: remove,
    });

    function add(){
        var todo = {description: m.newtodo};
        m.adding = true;
        FSApi.add(todo).then(function(result){
            var saved_todo = result.data;
            m.todos.push(saved_todo);
        }).finally(function(){
            m.adding = false;
        });
        m.newtodo = '';
    }

    function remove(todo){
        var idx = m.todos.indexOf(todo);
        m.todos.splice(idx, 1);
        //TODO: remove the todo using an API
    }

    return m;
});

angular.module('todo').directive('todo', function(){
    return {
        restrict: 'E',
        replace: true,
        scope: {},
        templateUrl: FS.BASE_URL+'components/todo_example/todo.html',
        controller: function($scope, TODOModel){
            var m = $scope.m = TODOModel;
        }
    };
});
angular.module('fstoolbar', ['fsauth']);

angular.module('fstoolbar').directive('fstoolbar', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: FS.BASE_URL+'components/toolbar/fstoolbar.html',
		controller: function($scope, FSAuth){
			$scope.auth = FSAuth;
		}
	};
});

angular.module('fsapi', ['fsajax']);

angular.module('fsapi').factory('FSApi', function(FSAjax){
	var fsapi = {
		add: todo,
		login: login,
		logout: logout,
		whoami: whoami,
		list_issues: list_issues,
		get_user_details: todo,
	};

	function todo(){}

	function login(username, password){
		return FSAjax.post('/api/login', {username: username, password: password});
	}

	function logout(){
		return FSAjax.get('/api/logout');
	}

	function whoami(){
		return FSAjax.get('/api/whoami');
	}

	function list_issues(filters){
		return FSAjax.get('/api/list_issues', {filters: angular.toJson(filters)});
	}

	return fsapi;
});
