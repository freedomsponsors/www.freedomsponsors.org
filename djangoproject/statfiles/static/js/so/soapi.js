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
