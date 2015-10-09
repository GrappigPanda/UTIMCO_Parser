from utimco.UtimcoMVA import UtimcoHandlerMVA
from utimco.UtimcoHandler import UtimcoLinks
from utimco.Errors import *
from sys import argv

for i in xrange(57350001, 57350436):
    utimco_session = UtimcoHandlerMVA(argv[1], argv[2], argv[3])
    resp = utimco_session.login_to_utimco()
   
    url = UtimcoLinks("MVA").get_link()
    
    if url:
        print url
    else:
        exit() 
    
    with open("./utimco/mva/{}.html".format(i), 'w') as f:
        utimco_session.open_report(url + str(i))
        
        try:
            utimco_session.profile_view("9/1/2014", "8/31/2015")
        except PROFILE_VIEW_ERROR as e:
            print "Failed due to {}".format(e)
            f.write("ERROR FAILED TO SAVE FILE")
        else:
            f.write(utimco_session.browser.response().read())