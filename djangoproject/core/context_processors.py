from django.conf import settings
from frespo_currencies import currency_service


def addAFewFrespoSettings(request):
    return {
        'SITE_HOME': settings.SITE_HOME,
        'FS_FEE': settings.FS_FEE,
        'BITCOIN_ENABLED': settings.BITCOIN_ENABLED,
        'ENABLE_PIWIK': settings.ENABLE_PIWIK,
        'BTC2USD': currency_service.get_rate('BTC', 'USD', False)
    }
