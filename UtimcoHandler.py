import mechanize
import os.path
from sys import argv

class INVALID_DATE(Exception):
    def __str__(self):
        return "Invalid date"
        
class UNKNOWN_ERROR(Exception): 
    def __str__(self):
        return "Unknown Error, be afraid!"

class PROFILE_VIEW_ERROR(Exception): 
    def __str__(self):
        return "Failed to retrieve profile info"

class UtimcoHandler:
    """
    A class to manage the login and cookie storage for the UTIMCO Wrapper
    """
    
    def __init__(self, username, userpass):
        self.username = username
        self.password = userpass

        self.browser = mechanize.Browser()
        self.set_browser_variable()
        self.user_agent = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
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
            login_url = "https://www.utimco.org/scripts/wcs/extranet_Login.asp?refer=/scripts/cris/login.asp"
            self.browser.open(login_url)
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
        #return self.browser.submit(name="submit", label="Submit Report Basis and Period Changes")
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
            
class UtimcoHandlerMVA(UtimcoHandler): 
    """
    A class extension for the MVA profile on Utimco's website.
    
    A lot of the reports for UTIMCO will need to be expanded from the base class,
    as each profile has different ways of handling looking up the info.
    """
    
    def profile_view(self, begin, end):
        if not self.check_for_errors():
            raise PROFILE_VIEW_ERROR
        self.browser.select_form(nr = 0)
        self.browser.form['frmBegPeriod'] = begin
        self.browser.form['frmEndPeriod'] = end
        req = self.browser.click(type = "submit", nr = 0)
        return self.browser.open(req)

for i in xrange(57350001, 57350436):
    utimco_session = UtimcoHandlerMVA(argv[1], argv[2])
    resp = utimco_session.login_to_utimco()
    with open("./utimco/mva/{}.html".format(i), 'w') as f:
        utimco_session.open_report("https://www.utimco.org/scripts/cris/rptMVA.asp?accountNumber={}".format(i))
        try:
            utimco_session.profile_view("9/1/2014", "8/31/2015")
        except PROFILE_VIEW_ERROR as e:
            print "Failed due to: {}".format(e)
            f.write("ERROR FAILED TO SAVE FILE")
        else:
            f.write(utimco_session.browser.response().read())
        finally:
            f.close()