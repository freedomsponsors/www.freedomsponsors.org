/**
 *
 Copyright (C) 2013  FreedomSponsors

 The JavaScript code in this page is free software: you can
 redistribute it and/or modify it under the terms of the GNU
 AFFERO GENERAL PUBLIC LICENSE (GNU AGPL) as published by the Free Software
 Foundation, either version 3 of the License, or (at your option)
 any later version.  The code is distributed WITHOUT ANY WARRANTY;
 without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU GPL for more details.

 As additional permission under GNU GPL version 3 section 7, you
 may distribute non-source (e.g., minimized or compacted) forms of
 that code without the copy of the GNU GPL normally required by
 section 4, provided you include this license notice and a URL
 through which recipients can access the Corresponding Source.

 For more information, refer to
 https://github.com/freedomsponsors/www.freedomsponsors.org/blob/master/AGPL_license.txt
 */


var fsapi_mod = angular.module('fsapi', []);

fsapi_mod.factory('FSApi', function(){

    function list_issues(project_id, sponsoring, offset, count){
        var params = {
            project_id: project_id,
            sponsoring: sponsoring,
            offset: offset,
            count: count
        };
        return fs_ajax_async_result($.get, '/core/json/list_issue_cards', params)
    }

    function get_latest_activity(project_id){
        var params = {
            project_id: project_id
        };
        return fs_ajax_async_result($.get, '/core/json/latest_activity', params)
    }

    function toggle_watch(entity, objid){
        var params = {
            entity: entity,
            objid: objid
        };
        return fs_ajax_async_result($.post, '/core/json/toggle_watch', params)
    }

    return {
        list_issues: list_issues,
        get_latest_activity: get_latest_activity,
        toggle_watch: toggle_watch
    };
})
