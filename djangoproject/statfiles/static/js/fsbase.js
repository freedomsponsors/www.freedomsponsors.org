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
