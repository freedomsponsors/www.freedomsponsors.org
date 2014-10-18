if(!window.FS){
    window.FS = {};
}
if(!FS.dependencies){
    FS.dependencies = [];
}

angular.module('fs', FS.dependencies).config(
    function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    }
);
