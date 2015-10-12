import mechanize
import os.path
from sys import argv

class UtimcoLinks:
    """ 
    A container class that acts as a lookup device for different report's
    links so that I don't have to hard-code links
    """
    
    def __init__(self, link):
        self.links = {
            'mva': "https://www.utimco.org/scripts/cris/rptMVA.asp?accountNumber=",
            'bva': "https://www.utimco.org/scripts/cris/rptBVA.asp?accountNumber=",
            'login': "https://utimco.org//scripts/wcs/extranet_Login.asp?refer=/scripts/cris/login.asp"
            }
            
        if link in self.links:
            self.target = link.lower()
        else:
            self.target = None
    
    def get_link(self, link_name=None):
        if self.target:
            return self.links[self.target.lower()]
            
        try:
            if link_name:
                return self.links[link_name.lower()]
        except KeyError as e:
            print "Failed to find key {}: {}".format(link_name, e)
            return None
            
        
class UtimcoBase:
    """
    A class to manage the login and cookie storage for the UTIMCO Wrapper
    """
    
    def __init__(self, username, userpass, report):
        self.username = username
        self.password = userpass

        self.browser = mechanize.Browser()
        self.set_browser_variable()
        self.user_agent = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        #TODO(ian): Ensure cookies properly save.
        self.cookie_jar = mechanize.LWPCookieJar()
        self.cookie_file = "utimco_cookies.txt"
        
        
        
    def __initialize_cookie_jar(self):
        self.browser.set_cookiejar(self.cookie_jar)
       
    def set_browser_variable(self, *args):
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)
        
    def __save_cookies_to_file(self):
        self.cookie_jar.save(self.cookie_file)

    def __load_cookies(self):
        self.cookie_jar.revert(self.cookie_file)
        
    def login_to_utimco(self):
        #TODO(ian): Verify if cookies are still good and load old cookies
        if os.path.isfile("test"):
            self.cookie_jar.revert(self.cookie_file)    
        else:
            self.browser.open(UtimcoLinks("login").get_link())
            self.browser.select_form(nr = 1)
            self.browser.form['frmUserID'] = self.username
            self.browser.form['frmPassword'] = self.password
        
            resp = self.browser.submit()
            self.__save_cookies_to_file()
        return "test"

    def open_report(self, report_link):
        self.browser.open(report_link)
        return self.browser.response().read()

    def simulate_click_button(self, button_number):
        self.browser.select_form(nr = 0)
        req = self.browser.click(type = "submit", nr = 0)
        return self.browser.open(req)

    def check_for_errors(self):
        resp = self.browser.response().read()
        if " error " in resp: 
            return False
        elif " Invalid " in resp:
            return False
        else:
            return True
