module.exports = function(grunt, options){
    return {
    	options: {
			banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
		},
		build: {
			src: ['tmp/myapp.js'],
			dest: 'tmp/myapp.min.js'
		}
    };
};