module.exports = function(grunt, options){
    return {
		fs: {
			src: 'static/js/**/*.html',
			dest: 'statfiles/static/js-generated/fs-templates.js',
			cwd: 'statfiles/',
			options: {
				prefix: '/',
				htmlmin: {
					collapseBooleanAttributes:      false,
					collapseWhitespace:             true,
					removeAttributeQuotes:          true,
					removeComments:                 true, // Only if you don't use comment directives!
					removeEmptyAttributes:          false,
					removeRedundantAttributes:      false,
					removeScriptTypeAttributes:     true,
					removeStyleLinkTypeAttributes:  true
				}
			}
		}
    };
};