module.exports = function(grunt, options){
    return {
		js: {
			files: options.arquivosjs.concat(['../js/**/*.html']),
			tasks: ['concamina_cache']
		},
    };
};