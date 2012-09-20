from splinter.browser import Browser 
from time import sleep
from core.utils.frespo_utils import Struct
import logging

logger = logging.getLogger(__name__)

TIMEOUT=5

def paradinha(time=0.4):
    sleep(time)
    # sleep(2)

class AppDriver:
    @classmethod
    def build(cls):
        driver = cls()
        driver.browser = Browser('chrome')
        # driver.browser = Browser()
        return driver

    def reset(self, home_url):
        logger.info ('>>>>>>>>>>>> reset '+home_url)
        self.home_url = home_url
        # self.browser.cookies.delete()

    def go_to_projects(self):
        self.browser.visit(self.home_url+"/core/project")

    def logout(self):
        userMenu = self.browser.find_by_id('a_userMenu')
        if(len(userMenu) > 0):
            userMenu[0].click()
            self.browser.click_link_by_partial_text('Sign Out')

    def createGoogleSession(self, user):
        logger.info ('>>>>>>>>>>>> create google session')
        browser = self.browser
        browser.visit('https://gmail.google.com') 
        paradinha(2)
        browser.fill('Email', user['username'])
        browser.fill('Passwd', user['password'])
        paradinha()
        browser.find_by_value('Sign in').click()

    def create_account_google(self, user):
        browser = self.browser
        browser.visit(self.home_url) 
        browser.click_link_by_partial_text('Log in / Register')
        browser.click_link_by_href('/login/google')
        browser.fill('Email', user['username'])
        browser.fill('Passwd', user['password'])
        # browser.find_by_value('Login').click()
        browser.find_by_id('signIn').click()
        assert(browser.is_text_present(user['first_name']+' '+user['last_name']+' - edit profile'))
        browser.find_by_id('btnSubmit').click()
        assert(browser.is_text_present(user['first_name']+user['last_name']))
        browser.find_by_id('upper_left_brand').click()
        assert(browser.is_text_present(user['first_name']+user['last_name']))
        assert(browser.is_text_present('Crowdfunding Free Software, one issue at a time'))

    def login_google(self, user=None):
        browser = self.browser

        browser.visit(self.home_url) 
        browser.click_link_by_partial_text('Log in / Register')
        browser.click_link_by_href('/login/google')
        if(user):
            browser.fill('Email', user['username'])
            browser.fill('Passwd', user['password'])
            browser.find_by_value('Login').click()
            browser.click_link_by_partial_text('FreedomSponsors.org')
            assert(browser.is_text_present(user['first_name']+user['last_name']))
        logger.info ('>>>>>>>>>>>> login_google, url: '+browser.url)
        assert(browser.is_text_present('Crowdfunding Free Software, one issue at a time'))

    def sponsor_issue(self, trackerURL, offer_dict):
        browser = self.browser
        browser.visit(self.home_url+'/core/issue/sponsor?trackerURL='+trackerURL)
        offer = Struct(**offer_dict)
        if(offer_dict.has_key('step2')):
            _waitUntilVisible_id(browser, 'div_step2_w')
            self._fillStep2(offer.step2)
        if(offer_dict.has_key('step3')):
            _waitUntilVisible_id(browser, 'div_step3_w')
            self._fillStep3(offer.step3)
        if(offer_dict.has_key('step4')):
            _waitUntilVisible_id(browser, 'div_step4_w')
            self._fillOfferForm(offer.step4)
        alert = None
        try:
            alert = browser.get_alert()
        except:
            pass
        if(alert):
            assert('congratulations' in alert.text)
            alert.accept()

    def addOffer(self, offer_dict):
        browser = self.browser
        offer = Struct(**offer_dict)
        
        browser.click_link_by_href('/core/issue/add')
        if(offer_dict.has_key('step1')):
            step1 = Struct(**offer.step1)
            if(offer.step1.has_key('trackerURL')):
                browser.fill('trackerURL', step1.trackerURL)
            if(offer.step1.has_key('noProject')):
                _check(browser, 'noProject', step1.noProject)
            browser.find_by_id('btnNext1').click()
            paradinha()
        if(offer_dict.has_key('step2')):
            _waitUntilVisible_id(browser, 'div_step2_w')
            self._fillStep2(offer.step2)
        if(offer_dict.has_key('step3')):
            _waitUntilVisible_id(browser, 'div_step3_w')
            self._fillStep3(offer.step3)
        if(offer_dict.has_key('step4')):
            _waitUntilVisible_id(browser, 'div_step4_w')
            self._fillOfferForm(offer.step4)
        if(offer.step1.has_key('trackerURL')):
            assert(browser.is_text_present("You're almost done"))
            browser.click_link_by_text('OK')

    def _fillStep2(self, step2dict):
        browser = self.browser
        step2 = Struct(**step2dict)
        if(step2dict.has_key('key')):
            browser.fill('key', step2.key)
        if(step2dict.has_key('title')):
            browser.fill('title', step2.title)
        if(step2dict.has_key('description')):
            browser.find_by_id('description')[0].fill('step2.description')
        browser.find_by_id('btnNext2').click()
        paradinha()

    def _fillStep3(self, step3dict):
        browser = self.browser
        step3 = Struct(**step3dict)
        if(step3dict.has_key('createProject')):
            _check(browser, 'createProject', step3.createProject)
        if(step3dict.has_key('newProjectName')):
            browser.fill('newProjectName', step3.newProjectName)
        if(step3dict.has_key('newProjectHomeURL')):
            browser.fill('newProjectHomeURL', step3.newProjectHomeURL)
        if(step3dict.has_key('newProjectTrackerURL')):
            browser.fill('newProjectTrackerURL', step3.newProjectTrackerURL)
        browser.find_by_id('btnNext3').click()
        paradinha()

    
    def followIssueLinkOnHomeByTitle(self, title):
        browser = self.browser
        
        browser.visit(self.home_url) 
        # browser.click_link_by_partial_text(": "+title)
        browser.click_link_by_partial_text(title)

    def followOfferLinkByValue(self, value):
        browser = self.browser
        
        browser.click_link_by_partial_text(str(value))

    def logoff(self):
        browser = self.browser
        browser.click_link_by_partial_text('FreedomTesting')
        browser.click_link_by_partial_text('Sign Out')

    def sponsorCurrentIssue(self, offerdatadict, assertAlmostDone=True):
        browser = self.browser
        browser.click_link_by_partial_text('Sponsor this issue')
        paradinha()
        self._fillOfferForm(offerdatadict)
        if(assertAlmostDone):
            self._assertAlmostDone()

    def commentOnCurrentIssueOrOffer(self, content, verifyContent=None):
        browser = self.browser
        browser.find_by_id('content').type(content)
        browser.find_by_id('btnSubmitNewComment').click()
        if not verifyContent:
            verifyContent = content
        _waitUntilTextPresent(browser, verifyContent)

    def editCommentOnCurrentIssueOrOffer(self, index, newcontent, verifyContent=None):
        browser = self.browser
        browser.find_by_name('selector-edit-comment')[index].click()
        for textarea in browser.find_by_name('content'):
            if textarea.visible:
                textarea.fill(newcontent)
                element = browser.find_by_name('selector-btnSubmitEditComment')[index]
                _waitUntilVisible_element(element)
                element.click()
                if not verifyContent:
                    verifyContent = newcontent
                _waitUntilTextPresent(browser, verifyContent)
                return
        raise


    def _assertAlmostDone(self):
        assert(self.browser.is_text_present("You're almost done"))
        self.browser.click_link_by_text('OK')

    def _fillOfferForm(self, offerdatadict):
        offerdata=Struct(**offerdatadict)
        browser = self.browser
        browser.fill('price', str(offerdata.price))
        browser.fill('acceptanceCriteria', offerdata.acceptanceCriteria)
        if(offerdatadict.has_key('no_forking')):
            _check(browser, 'no_forking', offerdata.no_forking)
        if(offerdatadict.has_key('require_release')):
            _check(browser, 'require_release', offerdata.require_release)
        browser.find_by_id('btnSubmitOffer').click()
        paradinha()
        

    def editCurrentOffer(self, price=None, acceptanceCriteria=None, no_forking=None, 
            require_release=None, expires=None, expiration_days=None):
        browser = self.browser
        browser.click_link_by_partial_text('Change offer')
        paradinha()
        if(price):
            browser.fill('price', str(price))
        if(acceptanceCriteria):
            browser.fill('acceptanceCriteria', acceptanceCriteria)
        if(not no_forking is None):
            _check(browser, 'no_forking', no_forking)
        if(not require_release is None):
            _check(browser, 'require_release', require_release)
        if(not expires is None):
            _check(browser, 'expires', expires)
            if(expires):
                browser.fill('expiration_time', str(expiration_days))
        browser.find_by_id('btnSubmitOffer').click()
        paradinha()

    def is_text_present(self, text):
        return self.browser.is_text_present(text)



    def quit(self):
        self.browser.quit()

def _check(browser, id, yes):
    if(yes):
        browser.check(id)
    else:
        browser.uncheck(id)

def _waitUntilVisible_id(browser, id):
    t=0
    i = 0.2
    while(not browser.find_by_id(id).visible and t < TIMEOUT):
        sleep(i)
        t = t+i
    if(not browser.find_by_id(id).visible):
        raise BaseException('Timeout waiting for element to become visible: '+id)

def _waitUntilVisible_element(element):
    t=0
    i = 0.2
    while(not element.visible and t < TIMEOUT):
        sleep(i)
        t = t+i
    if(not element.visible):
        raise BaseException('Timeout waiting for element to become visible: '+element)

def _waitUntilTextPresent(browser, text):
    t=0
    i = 0.2
    while(not browser.is_text_present(text) and t < TIMEOUT):
        sleep(i)
        t = t+i
    if(not browser.is_text_present(text)):
        raise BaseException('Timeout waiting for text to be present: '+text)