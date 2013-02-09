from django.conf import settings

def addAFewFrespoSettings(request):
	return {'SITE_HOME' : settings.SITE_HOME,
	'FS_FEE' : settings.FS_FEE,
	'BITCOIN_ENABLED' : settings.BITCOIN_ENABLED,}
