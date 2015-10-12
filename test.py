from utimco.UtimcoBase import UtimcoLinks
from UtimcoHandler import lookup_utimco_profile
from Errors.py import *
from sys import argv

for i in xrange(57350001, 57350436):
    url = UtimcoLinks(argv[3]).get_link(argv[3])
    
    if not url:
        exit("Failed to retrieve URL") 
        
    utimco_session = lookup_utimco_profile[argv[3]](argv[1], argv[2], argv[3])
    resp = utimco_session.login_to_utimco()
    
    with open("./utimco/{}/{}.html".format(argv[3].lower(), i), 'w') as f:
        utimco_session.open_report(url + str(i))
        
        try:
            utimco_session.profile_view("9/1/2014", "8/31/2015")
        except PROFILE_VIEW_ERROR as e:
            print "Failed due to {}".format(e)
            f.write("ERROR FAILED TO SAVE FILE")
        else:
            f.write(utimco_session.browser.response().read())