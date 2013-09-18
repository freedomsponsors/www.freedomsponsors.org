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

var lero = "Neste sentido, a determinação clara de objetivos assume importantes posições no estabelecimento do remanejamento dos quadros funcionais. Todavia, a consulta aos diversos militantes deve passar por modificações independentemente dos modos de operação convencionais. Ainda assim, existem dúvidas a respeito de como o desafiador cenário globalizado pode nos levar a considerar a reestruturação do impacto na agilidade decisória. Evidentemente, a complexidade dos estudos efetuados afeta positivamente a correta previsão dos índices pretendidos. As experiências acumuladas demonstram que a percepção das dificuldades cumpre um papel essencial na formulação da gestão inovadora da qual fazemos parte.";
leros = lero.split(" ");
var statuses = ['open', 'working', 'done']
var gravatares = [
    "http://www.gravatar.com/avatar/7ae5b251f74c82d72b579fe6b4191bb9?d=identicon&s=48",
    "http://www.gravatar.com/avatar/ad9ed1ab4a962efffe5add677ca85b22?d=identicon&s=48",
    "http://www.gravatar.com/avatar/b1f458499807b5dbd4019bfc9714f644?d=identicon&s=48",
    "http://www.gravatar.com/avatar/70f96152e4da06e994e9c6b0fd50a718?d=identicon&s=48",
    "http://www.gravatar.com/avatar/328de31775d6584cbf9ed230e27a7666?d=identicon&s=48",
    "http://www.gravatar.com/avatar/b7985aaf04af0ee974fbfb3b540180b3?d=identicon&s=48",
    "http://www.gravatar.com/avatar/6a6088b3d7b3fc812938bb7540dec798?d=identicon&s=48",
    "http://www.gravatar.com/avatar/f1c76b37f910f684d31b15cd994a68a9?d=identicon&s=48"
]
var usernames = [
    'ThomasLéveil',
    'Seth',
    'leonmax',
    'NeilConnolly',
    'EamonnLinehan',
    'vadipp',
    'jakob',
    'cmayeux',
    'DominikKupschke',
]
var project_images = [
    '/static/img2/default_project_logo.jpg',
    '/static/img2/github_logo.jpg',
    '/static/img2/project_logos/freedomsponsors_logo.png'
]

function random_int(num){
    return Math.floor(Math.random() * num)
}

function random_float(num){
    return (Math.random() * num).toFixed(2)
}

function random_string(){
    var idx = random_int(leros.length);
    return leros[idx];
}

function random_text(num){
    var s = '';
    for(var i=0; i<num; i++){
        s += random_string() + ' ';
    }
    return s;
}

function random_status(num){
    var idx = random_int(statuses.length);
    return statuses[idx];
}

function random_sponsors(num){
    var count = random_int(4) + 1;
    var result  = [];
    for(var i=0; i<count; i++){
        result.push({
            "image_link": random_gravatar(),
            "screen_name": random_username()
        })
    }
    return result;
}

function random_gravatar(){
    var idx = random_int(gravatares.length);
    return gravatares[idx];
}

function random_username(){
    var idx = random_int(usernames.length);
    return usernames[idx];
}

function random_image(){
    var idx = random_int(project_images.length);
    return project_images[idx];
}

var COUNT = 0;

function randomSponsoredIssue(){
    COUNT++;
    return {
        "status": random_status(),
        "sponsor_status": "SPONSORED",
        "viewcount": random_int(10),
        "four_sponsors": random_sponsors(),
        "description": random_text(100),
        "project_link": "#",
        "image_link": random_image(),
        "totalOffersPriceUSD": random_float(100),
        "moresponsors": random_int(4),
        "id": COUNT,
        "title": random_text(10),
        "totalPaidPriceUSD": random_float(100),
        "commentcount": random_int(10)
    };
}

function randomProposedIssue(){
    COUNT++;
    return {
        "status": random_status(),
        "sponsor_status": "PROPOSED",
        "viewcount": random_int(10),
        "four_sponsors": [],
        "description": random_text(100),
        "project_link": "#",
        "image_link": random_image(),
        "totalOffersPriceUSD": "0.00",
        "moresponsors": random_int(4),
        "id": COUNT,
        "title": random_text(10),
        "totalPaidPriceUSD": "0.00",
        "commentcount": random_int(10)
    }
}

var fsapi_mod = angular.module('fsapi', []);

fsapi_mod.factory('FSApi', function(){

    function list_issues(sponsoring, offset, count){
        var issues = [];
        for(var i=0; i < count; i++){
            var issue = sponsoring ? randomSponsoredIssue() : randomProposedIssue();
            issues.push(issue);
        }
        var result = {
            count: 15,
            issues: issues
        }
        return fs_timeout_async_result(result);
    }

    return {
        list_issues: list_issues
    }
});