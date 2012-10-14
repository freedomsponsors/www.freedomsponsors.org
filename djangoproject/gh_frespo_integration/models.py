from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Repo(models.Model):
    owner = models.CharField(max_length=256)
    owner_type = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    gh_id = models.CharField(max_length=32)
    createdByUser = models.ForeignKey(User)
    creationDate = models.DateTimeField()

    USER = "USER"
    ORG = "ORG"

    @classmethod
    def newRepo(cls, owner, owner_type, name, gh_id, createdByUser):
        repo = cls()
        repo.owner = owner
        repo.owner_type = owner_type
        repo.name = name
        repo.gh_id = gh_id
        repo.createdByUser = createdByUser
        repo.creationDate = timezone.now()
        return repo

class UserRepoConfig(models.Model):
    user = models.ForeignKey(User)
    repo = models.ForeignKey(Repo)
    add_links = models.BooleanField()
    new_only = models.BooleanField()
    creationDate = models.DateTimeField()

    @classmethod
    def newConfig(cls, user, repo):
        config = cls()
        config.user = user
        config.repo = repo
        config.add_links = False
        config.new_only = False
        config.creationDate = timezone.now()
        return config

class IssueAlreadyCommented(models.Model):
    repo = models.ForeignKey(Repo)
    number = models.IntegerField()