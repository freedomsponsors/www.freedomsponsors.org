import httplib2
import json
import requests
from django.conf import settings
from gh_frespo_integration.models import *
import dateutil.parser

BOT_AUTH = (settings.GITHUB_BOT_USERNAME, settings.GITHUB_BOT_PASSWORD)

def _fetch_json_objects_from_url(url):
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    resp, content = h.request(url)
    if(resp.status == 200):
        try:
            return json.loads(content)
        except:
            raise BaseException("Could not parse JSON view from URL: %s" % url)
    else:
        raise BaseException("status %s: %s" % (resp.status, url))

def fetch_repos(username):
    repos = _fetch_json_objects_from_url("https://api.github.com/users/%s/repos"%username)
    for repo in repos:
        repo['owner']['type'] = Repo.USER
    orgs = _fetch_json_objects_from_url("https://api.github.com/users/%s/orgs"%username)
    for org in orgs:
        org_repos = _fetch_json_objects_from_url("https://api.github.com/orgs/%s/repos"%org['login'])
        for repo in org_repos:
            repo['owner']['type'] = Repo.ORG
        repos.extend(org_repos)
    return repos

def bot_comment(username, repo_name, issue_number, body):
    github_url = "https://api.github.com/repos/%s/%s/issues/%s/comments"%(username, repo_name, issue_number)
    data = json.dumps({"body": body})
    r = requests.post(github_url, data, auth=BOT_AUTH)
    if(r.status_code != 201):
        raise BaseException("status %s: %s" % (r.status_code, github_url))

def bot_comment_on_users_behalf(user, username, repo_name, issue_number, body):
    access_token='' #TODO get user github token (big hex string on the database)
    github_url = "https://api.github.com/repos/%s/%s/issues/%s/comments?access_token=%s"%(username, repo_name, issue_number, access_token)
    data = json.dumps({"body": body})
    r = requests.post(github_url, data, auth=BOT_AUTH)
    if(r.status_code != 201):
        raise BaseException("status %s: %s" % (r.status_code, github_url))

def fetch_issues(repo_owner, repo_name, since):
    url = "https://api.github.com/repos/%s/%s/issues" % (repo_owner, repo_name)
    if since:
        since_date = since.strftime('%Y-%m-%dT%H:%M:%SZ')
        url += "?since=%s" % since_date
    issues = _fetch_json_objects_from_url(url)
    if not since:
        return issues
    issues_result = []
    for issue in issues:
        print 'found issue %s'%issue['number']
        created = dateutil.parser.parse(issue['created_at'])
        if created > since:
            issues_result.append(issue)
        else:
            break
    return issues_result
