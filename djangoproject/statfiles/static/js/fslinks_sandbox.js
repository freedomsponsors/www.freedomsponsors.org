angular.module('fslinks', []);

angular.module('fslinks').factory('FSLinks', function(){

    function issue_link(issue){
        return "/sandbox/issue"
    }

    return {
        issue_link: issue_link
    }
})
