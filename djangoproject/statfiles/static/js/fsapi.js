angular.module('fsapi', []);

angular.module('fsapi').factory('FSApi', function(){

    function list_issues(project_id, sponsoring, offset, count){
        var params = {
            project_id: project_id,
            sponsoring: sponsoring,
            offset: offset,
            count: count
        };
        return fs_ajax_async_result($.get, '/core/json/list_issue_cards', params)
    }

    function get_latest_activity(project_id, offset){
        var params = {
            project_id: project_id,
            offset: offset
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

    function check_username_availability(username){
        return fs_ajax_async_result($.get, '/core/json/check_username_availability/'+username)
    }

    return {
        list_issues: list_issues,
        get_latest_activity: get_latest_activity,
        toggle_watch: toggle_watch,
        check_username_availability: check_username_availability
    };
});
