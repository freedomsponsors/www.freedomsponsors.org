from frespo_currencies import currency_service

__author__ = 'tony'


def mock_currency_service():
    def mocked_get_rate(fron, to):
        if fron == to:
            return 1.0
        ft = fron + to
        map = {
            'USDBRL': 2.0,
            'USDBTC': 0.01,
            'BTCUSD': 100.0,
            'BTCBRL': 200.0
        }
        return map[ft]

    currency_service.get_rate = mocked_get_rate