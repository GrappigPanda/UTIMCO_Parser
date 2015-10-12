from UtimcoBase import UtimcoBase
from UtimcoMVA import UtimcoHandlerMVA
from UtimcoBVA import UtimcoHandlerBVA

def lookup_utimco_profile(profile):
    profile = profile.lower()
    profiles = {"mva":UtimcoHandlerMVA,"bva":UtimcoHandlerBVA}
    
    try:
        profiles[profile]
    except KeyError:
        exit("Failed to lookup key: {}".format(profile))
        
    return profiles[profile]