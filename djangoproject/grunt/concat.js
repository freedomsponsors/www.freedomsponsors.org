module.exports = function(grunt, options){
	var P = 'statfiles/static/js';
    return {
		build: {
			src: [
				P + '/fsbase.js',
				P + '/fsapi.js',
				P + '/fslinks.js',
				P + '/fsutil.js',
				P + '/activitylist/*.js',
				P + '/angularutils/*.js',
				P + '/contenteditable/*.js',
				P + '/issuecards/*.js',
				P + '/so/*.js',
				P + '/tags/tag_api.js',
				P + '/tags/taglist.js',
				'statfiles/static/js-generated/fs-templates.js'
			],
			dest: 'statfiles/static/js-generated/fs.js'
		}
    };
};