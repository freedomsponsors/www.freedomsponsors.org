module.exports = function(grunt, options){
    var phantom = grunt.option('phantom') || false;
    return {
		unit: {
			configFile: '../test/karma-unit.conf.js',
			autoWatch: false,
			browsers: phantom ? ["PhantomJS"] : ["Chrome"],
			singleRun: true
		}
    };
};