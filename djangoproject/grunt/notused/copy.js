module.exports = function(grunt, options){
    return {
        myapp: {
            cwd: 'tmp',
            expand: true,
            src: '**/*.js',
            dest: 'build/js/',
        }
    };
};