from gh_frespo_integration.utils import github_adapter
from gh_frespo_integration.models import *
import logging

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
        config.new_only = dict.has_key('check_newonly_%s' % gh_id)
        config.save()
        my_repo_ids.append(gh_id)
    UserRepoConfig.objects.filter(user__id = user.id).exclude(repo__gh_id__in = my_repo_ids).delete()