from django.test import TestCase
from gh_frespo_integration.utils import github_adapter

__author__ = 'tony'

def _assert_repo_contains(test, repos, name):
    repo_names = []
    found = False
    for repo in repos:
        if repo['name'] == name:
            found = True
            break
        repo_names.append(repo['name'])
    err = "repo %s not found in %s"%(name, repo_names)
    test.assertTrue(found, err)


class GithubAdapterTest(TestCase):
    def test_fetch_repos(self):
        repos = github_adapter.fetch_repos("tonylampada")
        self.assertTrue(len(repos) >= 6)
        _assert_repo_contains(self, repos, "PituKontrol")
        _assert_repo_contains(self, repos, "Svn-Hooks-In-Java")
        _assert_repo_contains(self, repos, "www.freedomsponsors.org")
        _assert_repo_contains(self, repos, "freedomsponsors-jira-plugin")
        _assert_repo_contains(self, repos, "freedomsponsors.github.com")
