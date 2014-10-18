module.exports = function(grunt, options){
    return {
		before: ['build', 'tmp'],
		after: ['tmp']
    };
};



