import os

from utimco.UtimcoBase import UtimcoLinks
from utimco.UtimcoHandler import lookup_utimco_profile
from utimco.Errors import *
from sys import argv

if len(argv) != 4:
    exit("Usage: \n\n\t python test.py <USER> <PASS> <profile>")

profile = argv[3].lower()

for i in xrange(57350001, 57350436):
    url = UtimcoLinks(profile).get_link(profile)
    
    if not url:
        exit("Failed to retrieve URL") 
        
    utimco_session = lookup_utimco_profile(profile)(argv[1], argv[2], profile)
    resp = utimco_session.login_to_utimco()
    
    if not os.path.isdir("./data/{}".format(profile)):
        os.mkdir("./data/{}".format(profile))
        
    with open("./data/{}/{}.html".format(profile.lower(), i), 'w') as f:
        utimco_session.open_report(url + str(i))
        
        try:
            utimco_session.profile_view("9/1/2014", "8/31/2015")
        except PROFILE_VIEW_ERROR as e:
            print "Failed due to {}".format(e)
            f.write("ERROR FAILED TO SAVE FILE")
        else:
            f.write(utimco_session.browser.response().read())