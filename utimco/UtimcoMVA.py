from UtimcoHandler import UtimcoHandler
from Errors import *

class UtimcoHandlerMVA(UtimcoHandler): 
    """
    A class extension for the MVA profile on Utimco's website.
    
    A lot of the reports for UTIMCO will need to be expanded from the base class,
    as each profile has different ways of handling looking up the info.
    """
    
    def profile_view(self, begin, end):
        if not UtimcoHandler.check_for_errors():
            raise PROFILE_VIEW_ERROR
        self.browser.select_form(nr = 0)
        self.browser.form['frmBegPeriod'] = begin
        self.browser.form['frmEndPeriod'] = end
        req = self.browser.click(type = "submit", nr = 0)
        return self.browser.open(req)

    def parse(self):
        pass