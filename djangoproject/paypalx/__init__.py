# -*- coding: utf-8 -*-
import datetime
import socket
import simplejson as json
from httplib2 import Http
from urlparse import urljoin

X_PAYPAL_ERROR_RESPONSE = {
    'TRUE': True,
    'FALSE': False
}

__all__ = ['PaypalError', 'DecodeError', 'AdaptivePayments', 'AdaptiveAccounts']


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
    

class PaypalError(Exception):
    def __init__(self, code, msg, headers):
        self.code = code
        self.msg = msg
        self.headers = headers
    
    def __getitem__(self, key):
        if key == 'code':
            return self.code
        try:
            return self.headers[key]
        except KeyError:
            raise AttributeError(key)
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        if self.code:
            return "#%s %s" % (self.code, self.msg)
        else:
            return self.msg
    

class DecodeError(PaypalError):
    def __init__(self, headers, body):
        super(DecodeError, self).__init__(None, "Could not decode JSON", headers)
        self.body = body
    
    def __repr__(self):
        return "headers: %s, content: <%s>" % (self.headers, self.body)
    

class AdaptiveAPI(object):
    debug = False
    production_host = 'https://svcs.paypal.com/'
    sandbox_host = 'https://svcs.sandbox.paypal.com/'
    
    def __init__(self, username, password, signature, application_id, email, api_operation, sandbox=False):
        self.username = username
        self.password = password
        self.signature = signature
        self.application_id = application_id
        self.email = email
        self.api_operation = api_operation
        if sandbox:
            self.host = self.sandbox_host
        else:
            self.host = self.production_host
        self.http = Http()
    
    def _check_required(self, required, **kwargs):
        for requirement in required:
            if requirement not in kwargs:
                raise PaypalError(None, "Missing required args : %s" % requirement, kwargs)
    
    def _endpoint(self, name):
        return urljoin(urljoin(self.host, self.api_operation + '/'), name)
    
    def _request(self, endpoint, data=None):
        body = None
        if data:
            body = json.dumps(data, cls=JSONEncoder)
        
        if self.debug:
            print endpoint
        
        def device_ip():
            return socket.gethostbyname(socket.gethostname())
        
        headers = {
            'X-PAYPAL-SECURITY-USERID': self.username,
            'X-PAYPAL-SECURITY-PASSWORD': self.password,
            'X-PAYPAL-SECURITY-SIGNATURE': self.signature,
            'X-PAYPAL-APPLICATION-ID': self.application_id,
            'X-PAYPAL-SANDBOX-EMAIL-ADDRESS': self.email,
            'X-PAYPAL-DEVICE-IPADDRESS': device_ip(),
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON'
        }
        
        if self.debug:
            print headers
            print body
        
        response, content = self.http.request(endpoint, "POST", body=body, headers=headers)
        if self.debug:
            print response
            print content
        
        if response['status'][0] != '2':
            code = response['status']
            message = content
            raise PaypalError(code, message, response)
        
        if content:
            try:
                content = json.loads(content)
            except ValueError:
                raise DecodeError(response, content)
        
        if X_PAYPAL_ERROR_RESPONSE[response.get('x-paypal-error-response', 'FALSE')]:
            code = response['status']
            message = content
            if isinstance(content, dict):
                code = content['error'][0]['errorId']
                message = content['error'][0]['message']
            raise PaypalError(code, message, response)
        
        return content
    

class AdaptivePayments(AdaptiveAPI):
    def __init__(self, username, password, signature, application_id, email, sandbox=False):
        super(AdaptivePayments, self).__init__(username, password, signature, application_id, email, 'AdaptivePayments', sandbox)
    
    def pay(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('actionType', 'cancelUrl', 'currencyCode',
            'receiverList', 'returnUrl')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('Pay')
        return self._request(endpoint, data=kwargs)
    
    def set_payments_options(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('payKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('SetPaymentOptions')
        return self._request(endpoint, data=kwargs)
    
    def execute_payment(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('payKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('ExecutePayment')
        return self._request(endpoint, data=kwargs)
    
    def payment_details(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        endpoint = self._endpoint('PaymentDetails')
        return self._request(endpoint, data=kwargs)
    
    def get_payment_options(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('payKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('GetPaymentOptions')
        return self._request(endpoint, data=kwargs)
    
    def preapproval(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('endingDate', 'startingDate', 'currencyCode',
            'maxTotalAmountOfAllPayments', 'cancelUrl', 'returnUrl')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('Preapproval')
        return self._request(endpoint, data=kwargs)
    
    def preapproval_details(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('preapprovalKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('PreapprovalDetails')
        return self._request(endpoint, data=kwargs)
    
    def cancel_preapproval(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('preapprovalKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('CancelPreapproval')
        return self._request(endpoint, data=kwargs)
    
    def refund(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        endpoint = self._endpoint('Refund')
        return self._request(endpoint, data=kwargs)
    
    def convert_currency(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('baseAmountList', 'convertToCurrencyList')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('ConvertCurrency')
        return self._request(endpoint, data=kwargs)
    

class AdaptiveAccounts(AdaptiveAPI):
    def __init__(self, username, password, signature, application_id, email, sandbox=False):
        super(AdaptiveAccounts, self).__init__(username, password, signature, application_id, email, 'AdaptiveAccounts', sandbox)
    
    def create_account(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        if 'sandboxEmailAddress' not in kwargs:
            kwargs['sandboxEmailAddress'] = self.email
        required_values = ('accountType', 'address', 'citizenshipCountryCode',
            'contactPhoneNumber', 'createAccountWebOptions', 'currencyCode',
            'name', 'preferredLanguageCode', 'requestEnvelope')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('CreateAccount')
        return self._request(endpoint, data=kwargs)
    
    def add_bank_account(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('confirmationType', 'bankCountryCode', 'requestEnvelope')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('AddBankingAccount')
        return self._request(endpoint, data=kwargs)
    
    def add_payment_card(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('billingAddress', 'cardType', 'cardNumber',
            'confirmationType', 'nameOnCard', 'expirationDate')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('AddPaymentCard')
        return self._request(endpoint, data=kwargs)
    
    def set_funding_source_confirmed(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('fundingSourceKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('SetFundingSourceConfirmed')
        return self._request(endpoint, data=kwargs)
    
    def get_verified_status(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        required_values = ('emailAddress', 'firstName', 'lastName', 'matchCriteria')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('GetVerifiedStatus')
        return self._request(endpoint, data=kwargs)
    
    def get_user_agreement(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = {}
        endpoint = self._endpoint('GetUserAgreement')
        return self._request(endpoint, data=kwargs)
    
