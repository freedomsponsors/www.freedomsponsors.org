from core.utils.trackers_adapter import fetchIssueInfo

issueInfo = fetchIssueInfo("https://issues.apache.org/jira/browse/AXIS-66")
assert(not issueInfo.error)
assert(issueInfo.tracker == 'JIRA')
assert(issueInfo.key == 'AXIS-66')
assert(issueInfo.project_url == 'https://issues.apache.org/jira/browse/AXIS')
assert(issueInfo.project_name == 'Axis')
assert(issueInfo.issue_title == '[xsd:list] WSDL2Java doesn\'t handle schema <list> enumerations')