from django.core.management.base import NoArgsCommand
from optparse import make_option
from core.models import *
from django.contrib.auth.models import User

def newIssue(project, key, title, createdByUser, trackerURLPrefix):
    return Issue.newIssue(project, key, title, createdByUser, trackerURLPrefix+key)

def newUser(username, email):
    user = User()
    user.username = username
    user.email = email
    return user

class Command(NoArgsCommand):

    help = "Popula dados de teste"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )
    

    def handle_noargs(self, **options):
        print('noop')
        # sponsor1 = newUser("Mr Sponsor", "sponsor1@gmail.com")#, "sponsor1@gmail.com", OpenIdAccount.GMAIL)
        # sponsor1.save()
        # prog1 = newUser("Mr Programmer", "prog1@gmail.com")#, "prog1@gmail.com", OpenIdAccount.FACEBOOK)
        # prog1.save()
        
        # maven = Project.newProject("Maven", sponsor1, "http://maven.apache.org/", "http://jira.codehaus.org/browse/MNG")
        # maven.save()
        # jenkins = Project.newProject("Jenkins", sponsor1, "http://jenkins-ci.org/", "https://issues.jenkins-ci.org/")
        # jenkins.save()
        
        # prefix = "https://issues.jenkins-ci.org/browse/"

        # for i in range(0,50):
        #     counter = 8*i
        #     newIssue(jenkins, "JENKINS-%s"%(counter+1), "Multiple-SCM-Plugin does not see that nothing changed in Git-Repo and keeps building", sponsor1, prefix).save()
        #     newIssue(jenkins, "JENKINS-%s"%(counter+2), "Major issue when Klocwork reporting is enabled", sponsor1, prefix).save()
        #     newIssue(jenkins, "JENKINS-%s"%(counter+3), "NPE on Jenkins start", sponsor1, prefix).save()
        #     newIssue(jenkins, "JENKINS-%s"%(counter+4), "I'm trying to authenticate the Jenkins command line (CLI) and the system returns an error message (user authentication with AD), but the GUI works.", sponsor1, prefix).save()
        #     newIssue(jenkins, "JENKINS-%s"%(counter+5), "Subverson Release Manager bombardes SVN server with requests", sponsor1, prefix).save()
        #     newIssue(jenkins, "JENKINS-%s"%(counter+6), "Safe Restart plungin is throwing HTTP Status 500 on Jenkins 1.424.1.", sponsor1, prefix).save()
        #     newIssue(jenkins, "JENKINS-%s"%(counter+7), "Race Condition in stable version 1.447.1|Critical Blocker", sponsor1, prefix).save()
        #     newIssue(jenkins, "JENKINS-%s"%(counter+8), "JDK auto installer installs to a different path than JAVA_HOME for a build uses", sponsor1, prefix).save()
        