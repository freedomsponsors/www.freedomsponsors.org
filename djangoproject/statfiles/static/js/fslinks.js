angular.module('fslinks', []);

angular.module('fslinks').factory('FSLinks', function(){

    function issue_link(issue){
        return issue.issue_link;
    }

    return {
        issue_link: issue_link
    };
})
