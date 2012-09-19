from decimal import Decimal
from core.frespomail import *
from core.frespomail import notifyProgrammers_offerrevoked, notifySponsors_workdone, notifyProgrammers_workdone
from core.frespoutils import dictOrEmpty, validateURL, validateIssueURL, get_or_none
from core.models import Issue, Project, Offer, Solution, IssueComment, OfferComment

__author__ = 'tony'

def search_issues(project_id, project_name, search_terms):
    issues = Issue.objects.all()
    if project_id:
        issues = issues.filter(project__id=project_id)
    elif project_name:
        issues = issues.filter(project__name__icontains=project_name)
    if search_terms:
        issues = issues.filter(title__icontains=search_terms)
    issues = issues.order_by('-creationDate')
    return issues


def add_new_issue_and_offer(dict, user):
    offer = _buildOfferFromDictionary(dict, user)
    if(offer.issue.project):
        offer.issue.project.save()
        offer.issue.project = offer.issue.project
    if(not offer.issue.id):
        offer.issue.save()
        offer.issue = offer.issue
    offer.save()
    msg = "offer: " + str(offer.price) + "\n<br>" +\
          "issue key: " + offer.issue.key + "\n<br>" +\
          "issue title: " + offer.issue.title + "\n<br>"
    if(offer.issue.project):
        msg += "project : " + offer.issue.project.name + "\n<br>" +\
               "project.trackerURL: " + offer.issue.project.trackerURL + "\n<br>"
    notify_admin("INFO: New issue sponsored", msg)
    return offer


def sponsor_existing_issue(issue_id, dict, user):
    issue = Issue.objects.get(pk=issue_id)
    _throwIfAlreadySponsoring(issue, user)
    offer = _buildOfferFromRequest_and_issue(dict, user, issue);
    offer.save()
    notifyProgrammers_offeradded(offer)
    notifySponsors_offeradded(offer)
    msg = "offer: " + str(offer.price) + "\n<br>" +\
          "issue key: " + offer.issue.key + "\n<br>" +\
          "issue title: " + offer.issue.title + "\n<br>"
    if(offer.issue.project):
        msg += "project : " + offer.issue.project.name + "\n<br>" +\
               "project.trackerURL: " + offer.issue.project.trackerURL + "\n<br>"
    notify_admin("INFO: Existing issue sponsored", msg)
    return offer


def change_existing_offer(offer_id, offerdict, user):
    offer = Offer.objects.get(pk=offer_id)
    _throwIfNotOfferOwner(offer, user)
    old_offer = offer.clone()
    offer.changeOffer(offerdict)
    notifyProgrammers_offerchanged(old_offer, offer)
    return offer


def add_solution_to_existing_issue(issue_id, comment_content, user):
    issue = Issue.objects.get(pk=issue_id)
    solution = get_or_none(Solution, issue=issue, programmer=user)
    if(solution):
        _throwIfSolutionInProgress(solution, user, 'add solution')
        solution.reopen()
    else:
        solution = Solution.newSolution(issue, user)
    solution.save()
    comment = None
    if(comment_content):
        comment = IssueComment.newComment(issue, user, comment_content)
        comment.save()
    notifySponsors_workbegun(solution, comment)
    return issue


def abort_existing_solution(solution_id, comment_content, user):
    solution = Solution.objects.get(pk=solution_id)
    _throwIfNotSolutionOwner(solution, user)
    _throwIfSolutionNotInProgress(solution, user, 'abort solution')
    solution.abort()
    comment = None
    if(comment_content):
        comment = IssueComment.newComment(solution.issue, user, comment_content)
        comment.save()
    notifySponsors_workstopped(solution, comment)

    return solution


def revoke_existing_offer(offer_id, comment_content, user):
    offer = Offer.objects.get(pk=offer_id)
    _throwIfNotOfferOwner(offer, user)
    _throwIfOfferNotOpen(offer, user, 'revoke offer')
    offer.revoke()
    comment = None
    if(comment_content):
        comment = OfferComment.newComment(offer, user, comment_content)
        comment.save()
    notifyProgrammers_offerrevoked(offer, comment)
    return offer


def resolve_existing_solution(solution_id, comment_content, user):
    solution = Solution.objects.get(pk=solution_id)
    _throwIfNotSolutionOwner(solution, user)
    _throwIfSolutionNotInProgress(solution, user, 'resolve solution')
    solution.resolve()
    comment = None
    if(comment_content):
        comment = IssueComment.newComment(solution.issue, user, comment_content)
        comment.save()
    notifySponsors_workdone(solution, comment)
    notifyProgrammers_workdone(solution, comment)
    return solution


def _buildOfferFromDictionary(dict, user):
    check_noProject = dict.has_key('noProject')
    issue_trackerURL = dict['trackerURL']
    issue_projectId = dict['project_id']
    issue_projectName = dictOrEmpty(dict, 'project_name')
    check_createProject = dict.has_key('createProject')
    newProject_name = dictOrEmpty(dict, 'newProjectName')
    newProject_homeURL = dictOrEmpty(dict, 'newProjectHomeURL')
    newProject_trackerURL = dictOrEmpty(dict, 'newProjectTrackerURL')
    issue_key = dictOrEmpty(dict, 'key');
    issue_title = dictOrEmpty(dict, 'title');
    issue_description = dictOrEmpty(dict, 'description');

    _throwIfIssueExists(issue_trackerURL, user)

    issue = None
    if(check_noProject):
        if(not issue_title or not issue_description):
            raise BaseException('title and description are required')

        issue = Issue.newIssueOrphan(issue_title, issue_description, user)
    else:
        project = None
        if(check_createProject):
            if(not newProject_name or not newProject_homeURL or not newProject_trackerURL):
                raise BaseException('all parameters for new project are required')

            projectHomeURLValidationError = validateURL(newProject_homeURL)
            if(projectHomeURLValidationError):
                raise BaseException('invalid project URL ('+newProject_homeURL+') - '+projectHomeURLValidationError)

            projectTrackerURLValidationError = validateURL(newProject_trackerURL)
            if(projectTrackerURLValidationError):
                raise BaseException('invalid project tracker URL ('+newProject_trackerURL+') - '+projectTrackerURLValidationError)

            project = Project.newProject(newProject_name, user, newProject_homeURL, newProject_trackerURL)
        else:
            project = Project.objects.get(pk=int(issue_projectId))
            if(newProject_homeURL != project.homeURL):
                project.homeURL = newProject_homeURL

        if(not issue_key or not issue_title):
            raise BaseException('key and title are required')

        issueURLValidationError = validateIssueURL(issue_trackerURL)
        if(issueURLValidationError):
            raise BaseException('invalid issue URL ('+issue_trackerURL+') - '+issueURLValidationError)

        issue = Issue.newIssue(project, issue_key, issue_title, user, issue_trackerURL)

    return _buildOfferFromRequest_and_issue(dict, user, issue);


def _throwIfIssueExists(trackerURL, user):
    if(trackerURL):
        issues = Issue.objects.filter(trackerURL__iexact=trackerURL)
        if(issues.count() >= 1):
            raise BaseException('Already exists: '+trackerURL+". User %s"%user.id)


def _buildOfferFromRequest_and_issue(dict, user, issue):
    offer = Offer.newOffer(issue, user, Decimal(0), '', False, False, None)
    _setOfferAttributesFromRequest(offer, dict)
    return offer


def _setOfferAttributesFromRequest(offer, dict):
    offer.price = Decimal(dict['price'])
    offer.no_forking = dict.has_key('no_forking')
    offer.require_release = dict.has_key('require_release')
    offer_check_expires = dict.has_key('expires')
    if(offer_check_expires):
        offer.set_expiration_days(int(dict['expiration_time']))
    offer.acceptanceCriteria = dict['acceptanceCriteria']

    if(not offer.acceptanceCriteria):
        raise BaseException('acceptanceCriteria is required')

    if(offer.price <= 0):
        raise BaseException('offer price must be a positive number')



def _throwIfAlreadySponsoring(issue, user):
    offer = get_or_none(Offer, issue=issue, sponsor=user)
    if(offer):
        raise BaseException('Already sponsoring: '+str(issue.id)+','+str(user.id))

def _throwIfNotOfferOwner(offer, user):
    if(not offer.sponsor.id == user.id):
        raise BaseException('Security error. '+str(user.id)+' is not offer ('+str(offer.id)+') owner. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')


def _throwIfSolutionInProgress(solution, user, operation=None):
    if(solution.status == Solution.IN_PROGRESS):
        raise BaseException('Error: found solution in progress '+str(solution.id)+', '+str(user.id)+'. operation: '+operation)




def _throwIfSolutionNotInProgress(solution, user, operation=None):
    if(not solution.status == Solution.IN_PROGRESS):
        raise BaseException('Error. Expected solution in IN_PROGRESS state. Found ('+solution.status+'). User '+str(user.id)+'/ solution '+str(solution.id)+'. operation: '+operation)


def _throwIfOfferNotOpen(offer, user, operation=None):
    if(not offer.status == Offer.OPEN):
        raise BaseException('Error. Expected offer in OPEN state. Found ('+offer.status+'). User '+str(user.id)+'/ offer '+str(offer.id)+'. operation: '+operation)


def _throwIfNotSolutionOwner(solution, user):
    if(not solution.programmer.id == user.id):
        raise BaseException('Security error. '+str(user.id)+' is not solution ('+str(solution.id)+') owner. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')


