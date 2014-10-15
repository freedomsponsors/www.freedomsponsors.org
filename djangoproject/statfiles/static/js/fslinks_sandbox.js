var fsapi_mod = angular.module('fslinks', []);

fsapi_mod.factory('FSLinks', function(){

    function issue_link(issue){
        return "/sandbox/issue"
    }

    return {
        issue_link: issue_link
    }
})
