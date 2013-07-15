import httplib2
from urlparse import urlparse, parse_qs
import re
from xml.dom.minidom import parseString
import json
from core.services.mail_services import notify_admin

class IssueInfo(object):

    def __init__(self):
        self.error = ''
        self.project_name = ''
        self.issue_title = ''
        self.key = ''
        self.tracker = ''
        self.project_trackerURL = ''


def fetchIssueInfo(issueURL):
    if looks_like_github(issueURL):
        info = retriveGithubInfo(issueURL)
    elif looks_like_jira(issueURL):
        info = retriveJIRAInfo(issueURL)
    elif looks_like_bugzilla(issueURL):
        info = retriveBugzillaInfo(issueURL)
    elif looks_like_bitbucket(issueURL):
        info = retrieveBitBucketInfo(issueURL)
    elif looks_like_google_code(issueURL):
        info = retrieveGoogleCodeInfo(issueURL)
    else:
        info = IssueInfo()
    if info.error:
        print 'Error fetching info for: '+issueURL+' - '+info.error
        notify_admin('Error fetching info for: '+issueURL, info.error)
    return info


######## JIRA ##########

def retriveJIRAInfo(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    last_after_slash = parsedURL.path.split('/')[-1]
    jira_key = last_after_slash
    path_before_jira_key = parsedURL.path.split('/'+jira_key)[0]
    project_abbrev = get_jira_project_abbrev(jira_key)
    xmlviewURL = parsedURL.scheme+'://'+parsedURL.netloc+get_jira_xml_view(parsedURL.path)
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    try: 
        resp, content = h.request(xmlviewURL)
        info.key = jira_key
        info.tracker = 'JIRA'
        info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+path_before_jira_key+'/'+project_abbrev
        if(resp.status == 200):
            try:
                dom = parseString(content)
                info.project_name = dom.getElementsByTagName('project')[0].childNodes[0].wholeText
                info.issue_title = dom.getElementsByTagName('summary')[0].childNodes[0].wholeText
                info.description = dom.getElementsByTagName('item')[0].getElementsByTagName('description')[0].childNodes[0].wholeText
            except:
                info.error = 'Could not parse XML view from: '+xmlviewURL
        else:
            info.error = ('status %s: '%resp.status)+xmlviewURL
    except httplib2.HttpLib2Error as e:
        info.error = e.message
    return info
            
    
def looks_like_jira(url):
    parsedURL = urlparse(url)
    path = parsedURL.path
    jira_key = path.split('/')[-1]
    if(path.endswith('/browse/'+jira_key)):
        match = re.match(r'[A-Z]+-\d+', jira_key)
        if(match):
            return match.group(0) == jira_key

def get_jira_project_abbrev(jira_key):
    match = re.match(r'[A-Z]+', jira_key)
    return match.group(0)

def get_jira_xml_view(path):
    jira_key = path.split('/')[-1]
    before_browse = path.split('browse/'+jira_key)[0]
    return before_browse+'/si/jira.issueviews%3aissue-xml/'+jira_key+'/'+jira_key+'.xml'

######## GITHUB ##########


def looks_like_github(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'github.com'


def retriveGithubInfo(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    pathTokens = parsedURL.path.split('/')
    if len(pathTokens) < 5 or pathTokens[3].lower() != 'issues':
        info.error = "URL doesn't look like a Github issue link"
        return info
    info.key = pathTokens[4]
    info.tracker = 'GITHUB'
    info.project_name = pathTokens[2]
    info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+'/'+pathTokens[1]+'/'+pathTokens[2]+'/'+pathTokens[3]
    issueJsonURL = 'https://api.github.com/repos'+parsedURL.path
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    try: 
        resp, content = h.request(issueJsonURL)
        if resp.status == 200:
            try:
                issueJson = json.loads(content)
                info.issue_title = issueJson['title']
                info.description = issueJson['body']
            except:
                info.error = 'Could not parse JSON view from: '+issueJsonURL
        else:
            info.error = ('status %s: '%resp.status)+issueJsonURL
    except httplib2.HttpLib2Error as e:
        info.error = e.message
    return info


######### Bugzilla ########


def looks_like_bugzilla(url):
    parsedURL = urlparse(url)
    if parsedURL.path.lower().endswith('show_bug.cgi'):
        query = parsedURL.query.lower()
        match = re.match(r'id=\d+', query)
        if match:
            return match.group(0) == query
    return False


def retriveBugzillaInfo(url):
    parsedURL = urlparse(url)
    info = IssueInfo()
    info.error = ''
    info.key = parsedURL.query.split('id=')[1]
    info.tracker = 'BUGZILLA'
    pathBeforeShowBug=parsedURL.path.split('show_bug.cgi')[0]
    bugJsonURL = parsedURL.scheme+'://'+parsedURL.netloc+pathBeforeShowBug+'jsonrpc.cgi?method=Bug.get&params=[{"ids":['+info.key+']}]'
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    try: 
        resp, content = h.request(bugJsonURL)
        if resp.status == 200:
            try:
                bugJson = json.loads(content)
                info.project_name = bugJson['result']['bugs'][0]['product']
                info.issue_title = bugJson['result']['bugs'][0]['summary']
                info.description = info.issue_title
                info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+pathBeforeShowBug+'buglist.cgi?product='+info.project_name
            except:
                info.error = 'Could not parse JSon view from: '+bugJsonURL
        elif resp.status == 404:
            pass
        return info
    except httplib2.HttpLib2Error as e:
        info.error = e.message
        return info


########## BitBucket ########


def looks_like_bitbucket(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'bitbucket.org'


def retrieveBitBucketInfo(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    pathTokens = parsedURL.path.split('/')
    if len(pathTokens) < 5 or pathTokens[3].lower() != 'issue':
        info.error = "URL doesn't look like a BitBucket issue link"
        return info
    _username, _project_name, info.key = pathTokens[1], pathTokens[2], pathTokens[4]
    info.tracker = 'BITBUCKET'
    info.project_name = _project_name
    info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+'/'+_username+'/'+_project_name + '/issues'
    issueJsonURL = 'https://api.bitbucket.org/1.0/repositories/' + _username + '/' + _project_name + '/issues/' + pathTokens[4]
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    try: 
        resp, content = h.request(issueJsonURL)
        if resp.status == 200:
            try:
                issueJson = json.loads(content)
                info.issue_title = issueJson['title']
                info.description = issueJson['content']
            except:
                info.error = 'Could not parse JSon view from: '+issueJsonURL
        else:
            info.error = ('status %s: '%resp.status)+issueJsonURL
    except httplib2.HttpLib2Error as e:
        info.error = e.message
    return info


######## Google Code ##########


def retrieveGoogleCodeInfo(url):
    info = IssueInfo()
    parsedURL = urlparse(url)
    pathTokens = parsedURL.path.split('/')
    if len(pathTokens) < 5 or pathTokens[1] != 'p' or pathTokens[3] != 'issues' or pathTokens[4] != 'detail':
        info.error = "URL doesn't look like a Google Code issue link"
        return info
    info.key = parse_qs(parsedURL.query)['id'][0]
    info.tracker = 'GOOGLECODE'
    info.project_name = pathTokens[2]
    info.project_trackerURL = info.project_trackerURL = parsedURL.scheme+'://'+parsedURL.netloc+'/p/'+info.project_name+'/issues/list'
    issueUrl = 'https://code.google.com/feeds/issues/p/' + info.project_name + '/issues/full?id=' + info.key

    h = httplib2.Http(disable_ssl_certificate_validation=True)
    try: 
        resp, content = h.request(issueUrl)
        if resp.status == 200:
            try:
                dom = parseString(content)
                entry = dom.getElementsByTagName('entry')[0]
                info.issue_title = entry.getElementsByTagName('title')[0].childNodes[0].wholeText
                info.description = entry.getElementsByTagName('content')[0].childNodes[0].wholeText
            except:
                info.error = 'Could not parse XML from: '+issueUrl
        else:
            info.error = ('status %s: '%resp.status)+issueUrl
    except httplib2.HttpLib2Error as e:
        info.error = e.message
    return info
            
    
def looks_like_google_code(url):
    parsedURL = urlparse(url)
    return parsedURL.netloc.lower() == 'code.google.com'
