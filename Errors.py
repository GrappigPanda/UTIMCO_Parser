class INVALID_DATE(Exception):
    def __str__(self):
        return "Invalid date"
        
class UNKNOWN_ERROR(Exception): 
    def __str__(self):
        return "Unknown Error, be afraid!"

class PROFILE_VIEW_ERROR(Exception): 
    def __str__(self):
        return "Failed to retrieve profile info"
 