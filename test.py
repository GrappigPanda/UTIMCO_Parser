from UtimcoMVA import UtimcoHandlerMVA
from Errors import *
from sys import argv


for i in xrange(57350001, 57350436):
    # Username, then pass
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