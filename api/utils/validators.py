import re


def verify_password(password):
    flash_message = ""
    if not password:
        flash_message = "Please enter a password"
        process_registration = False

    elif not is_strong_password(password):
        flash_message = "Password must be 8 characters including one uppercase letter and alphanumeric characters"
        process_registration = False 
    else: 
        process_registration = True 

    return process_registration,flash_message



def verify_email(email):
    flash_message = ""
    if not email:
        flash_message = "Please enter a email"
        process_registration = False

    elif not isEmailValid(email):
        flash_message = "Please enter a email expl. john@domaine.com"
        process_registration = False 
    
    else: 
        process_registration = True
    
    return process_registration,flash_message






def isEmailValid(email):
    regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

    if re.fullmatch(regex, email):
        return True
    else:
        return False




def is_strong_password(password):
    is_long = len(password) >= 8
    has_digit = bool(re.search(r"\d", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    if(has_digit and has_upper and is_long):
        return True
    else:
        return False

