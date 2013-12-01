from gh_frespo_integration.utils import github_adapter
from gh_frespo_integration.models import *
from django.conf import settings
import logging
from datetime import timedelta

__author__ = 'tony'

logger = logging.getLogger(__name__)

def get_repos_and_configs(user):
    repos = []
    github_username = user.github_username()
    if github_username:
        repos = github_adapter.fetch_repos(github_username)
    for repo_dict in repos:
        gh_id = repo_dict['id']
        repodb = get_repodb_by_githubid(gh_id)
        if repodb:
            user_repo_config = get_repo_config_by_repo_and_user(repodb, user)
            if user_repo_config:
                repo_dict['add_links'] = user_repo_config.add_links
                repo_dict['new_only'] = user_repo_config.new_only
    return repos

def get_repodb_by_githubid(gh_id):
    repos = Repo.objects.filter(gh_id = gh_id)
    if repos.count() > 1:
        logger.error('Database inconsistency: multiple repos found with gh_id:%s'%gh_id)
    elif repos.count() == 1:
        return repos[0]
    else:
        return None

def get_repo_config_by_repo_and_user(repo, user):
    configs = UserRepoConfig.objects.filter(repo__id = repo.id, user__id = user.id)
    if configs.count() > 1:
        logger.error('Database inconsistency: multiple configs found for repo:%s / user:%s'%(repo.id, user.id))
    elif configs.count() == 1:
        return configs[0]
    else:
        return None

def update_user_configs(user, dict):
    github_username = user.github_username()
    if github_username:
        repos = github_adapter.fetch_repos(github_username)
        my_repo_ids = []
    for repo_dict in repos:
        gh_id = repo_dict['id']
        repodb = get_repodb_by_githubid(gh_id)
        if not repodb:
            owner = repo_dict['owner']['login']
            owner_type = repo_dict['owner']['type']
            name = repo_dict['name']
            repodb = Repo.newRepo(owner, owner_type, name, gh_id, user)
            repodb.save()
        config = get_repo_config_by_repo_and_user(repodb, user)
        if not config:
            config = UserRepoConfig.newConfig(user, repodb)
        config.add_links = dict.has_key('check_addlink_%s' % gh_id)
#        config.new_only = dict.has_key('check_newonly_%s' % gh_id)
        config.new_only = True
        config.save()
        my_repo_ids.append(gh_id)
    UserRepoConfig.objects.filter(user__id = user.id).exclude(repo__gh_id__in = my_repo_ids).delete()

def add_sponsorthis_comments():
    configs = UserRepoConfig.objects.filter(add_links = True)
    logger.debug('starting sponsor_this routine...')
    for config in configs:
        repo_owner = config.repo.owner
        repo_name = config.repo.name
        last_ran = None
        logger.debug('processing repo_config %s (%s/%s)' % (config.id, config.repo.owner, config.repo.name))
        if config.new_only or config.already_did_old:
            last_ran = config.last_ran - timedelta(hours=1)
            logger.debug('will list issues after %s' % last_ran)
        else:
            logger.debug('will list all issues')
        config.update_last_ran()
        try:
            issues = github_adapter.fetch_issues(repo_owner, repo_name, last_ran)
            logger.debug('issues are fetched')
            for issue in issues:
                _add_comment_if_not_already(config, int(issue['number']), repo_owner, repo_name)
            if not config.new_only:
                config.set_already_did_old()
        except BaseException as e:
            logger.error("Error adding comments repository %s/%s: %s" % (repo_owner, repo_name, e))
    logger.debug('sponsor_this ended successfully')

def _add_comment_if_not_already(repo_config, issue_number, repo_owner, repo_name):
    issue_already_commented = get_issue_already_commented(repo_config.repo, issue_number)
    if not issue_already_commented:
        body = u"""Do you care about this issue? To get it fixed quickly, [offer a cash incentive to developers on FreedomSponsors.org](%s/core/issue/sponsor?trackerURL=https://github.com/%s/%s/issues/%s).
If you can only give US$5, offering just that will invite other people to do the same. Sharing the cost will soon add up!""" % (settings.SITE_HOME, repo_owner, repo_name, issue_number)
        github_adapter.bot_comment(repo_owner, repo_name, issue_number, body)
        issue_already_commented = IssueAlreadyCommented.newIssueAlreadyCommented(repo_config.repo, issue_number)
        issue_already_commented.save()
        logger.info('commented on issue %s of %s/%s' % (issue_number, repo_owner, repo_name))
    else:
        logger.debug('NOT commenting on issue %s of %s/%s because it was already commented on' % (issue_number, repo_owner, repo_name))

def get_issue_already_commented(repo, number):
    iacs = IssueAlreadyCommented.objects.filter(repo__id = repo.id, number = number)
    if iacs.count() > 1:
        logger.error('Database inconsistency: multiple issue_already_commented found for repo:%s / number:%s'%(repo.id, number))
    elif iacs.count() == 1:
        return iacs[0]
    else:
        return None

