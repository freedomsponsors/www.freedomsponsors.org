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

function fs_timeout_async_result(result){
    var callback = undefined;
    var r = {
        onResult: function(cb){
            callback = cb;
        }
    };
    setTimeout(function(){
        callback(result)
    }, 1000);
    return r;
}


function fs_ajax_async_result(func, url, params){
    var r = {
        onResult: function(callback){
            r.callback = callback;
            return r;
        },
        onError: function(errorcallback){
            r.errorcallback = errorcallback;
            return r;
        }
    };
    func(url, params)
        .success(function(result){
            if (r.callback) {
                if(result){
                    try {
                        result = JSON.parse(result);
                    } catch(err){}
                }
                r.callback(result)
            }
        })
        .error(function(e){
            if (r.errorcallback) {
                r.errorcallback(e)
            }            
        });
    return r;
}

function get4Sponsors(issue){
    var empties = [];
    for(var i=0; i<4 - issue.four_sponsors.length; i++){
        empties.push({empty:true});
    }
    return empties.concat(issue.four_sponsors)
}
