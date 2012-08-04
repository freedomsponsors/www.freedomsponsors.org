from django.core.management.base import NoArgsCommand
from optparse import make_option
from core.models import *
from core.frespoutils import get_or_none
from django.contrib.auth.models import User


def frespoUser():
    user = get_or_none(User, username='freedomsponsors')
    if(user):
        return user
    else:
        user = User()
        user.username = 'freedomsponsors'
        user.email = 'freedomsponsors@freedomsponsors.com'
        user.first_name = 'Freedom'
        user.last_name = 'Sponsors'
        user.save()
    return user

def frespoProject(frespo_user):
    project = get_or_none(Project, name='FreedomSponsors')
    if(project):
        return project
    else:
        project = Project.newProject('FreedomSponsors', frespo_user, 'http://www.freedomsponsors.com', 'http://www.freedomsponsors.com')
        project.save()
    return project

class Command(NoArgsCommand):

    help = "Popula dados estaticos iniciais"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )
    
    def handle_noargs(self, **options):
        frespo_user = frespoUser()
        UserInfo.newUserInfo(frespo_user).save()
        frespo_project = frespoProject(frespo_user)
        print('User freedomsponsors = %s'%frespo_user.id)
        print('Project FreedomSponsors = %s'%frespo_project.id)
