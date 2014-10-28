module.exports = function(grunt) {

    // var dados_comuns_disponiveis_pra_todas_as_tasks = {
    //     arquivosjs: [
    //         '../js/base2.js',
    //         '../js/ajax2.js',
    //         '../js/github_api3.js',
    //         '../js/components/gh-*/**/*.js',
    //         '../js/components/popup.js',
    //     ],
    //     pkg: grunt.file.readJSON('package.json')
    // };


    require('time-grunt')(grunt);

    var path = require('path');
    require('load-grunt-config')(grunt, {
        init: true,
        // configPath: path.join(process.cwd(), 'grunt'),
        data: {}
    });

};