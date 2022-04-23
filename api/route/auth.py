from flask import Blueprint, render_template,request, jsonify
from api.constants import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from api.service.maillingService import mailSendGrid
from api.service.userService import check_user, hash_password, register_user, verify_auth, verify_user
from api.utils.encryption import  decrypt_message, encrypt_message,generate_key
from api.utils.manage import create_table, insert_test_data
from api.utils.timercount import duration_time
from api.utils.validators import verify_email, verify_password

from urllib.parse import urlparse

from flask_httpauth import HTTPBasicAuth
from flasgger import swag_from

authBasic = HTTPBasicAuth()
auth_api = Blueprint('auth', __name__,url_prefix="/api/v1/auth")



@auth_api.post("/register")
@swag_from('../docs/register.yaml')
def register():

    #Credentials and input verification 
    try:   
        email = request.json['email']
        password = request.json['password']
        respEmail,messageFlashEmail = verify_email(email)
        if not respEmail:
            return jsonify(status="error", message=messageFlashEmail), HTTP_400_BAD_REQUEST
        respPass,messagePass = verify_password(password)
        if not respPass:
            return jsonify(status="error", message=messagePass), HTTP_400_BAD_REQUEST

    except KeyError:
        return jsonify(status="error", message="Must supply 'email' and 'password'"), HTTP_400_BAD_REQUEST
    except:
        return jsonify(status="error", message="Invalid json'"), HTTP_400_BAD_REQUEST


    #check if user already registred 
    checkuser = check_user(email)   

    if not checkuser :
        user = register_user(email,password)   
        if  user :
            #generate link verifification with crypted id and send email
            byte_msg = encrypt_message(email)
            if mailSendGrid(user.code,user.email):
                return jsonify({
                    'message': "User created",
                    'link': "http://127.0.0.1:5000/api/v1/auth/users/"+byte_msg[2:-1]+"/email-verification",
                    'user': user.serialize()

                }), HTTP_201_CREATED
        else :
            return jsonify(status="error", message="An error has occured"), HTTP_400_BAD_REQUEST

    else :
        return jsonify(status="error", message="Email already in use"), HTTP_400_BAD_REQUEST


#Verification user web version
#userIdToken = crypted and encoded Email  
@auth_api.get('/users/<userIdToken>/email-verification')
def verify(userIdToken):
    
    alertClass = "info"

    #decrypt userIdToken to get email  
    email = decrypt_message(userIdToken)

    #verify_email   
    respEmail,messageFlashEmail = verify_email(email)
    if not respEmail:
        return jsonify(status="error", message=messageFlashEmail), HTTP_400_BAD_REQUEST
    
    #get user to check if already verfied 
    user = check_user(email)
    return render_template('index.html',email=email,alertClass=alertClass,verified=user[4])



@auth_api.post('/verify-code')
@swag_from('../docs/verify.yaml')
def verifyCode():
    #get email from json rest
    email = request.json['email']
    #verify email input
    respEmail,messageFlashEmail = verify_email(email.strip())
    if not respEmail:
        return jsonify(status="error", message=messageFlashEmail), HTTP_400_BAD_REQUEST

    code = request.json['code']


    #get user data(code and datetime created) from database 
    user = check_user(email)
    userValidation = user[4]
    dateCode = str(user[6].strip())
    count5min = duration_time(dateCode)

    if userValidation :
        return {"message" :"User already verified","alert":"success"}
  
    else :
        if count5min > 5:
            return {"message" :"The pin code has expired. Please re-send the verification","alert":"warning"}, HTTP_200_OK
        
        else:
            if user[5].strip() == code:
                if verify_user(email):
                    return {"message" :"✔️ Email verified successfully. time to have fun!","alert":"success"}, HTTP_200_OK
                else : 
                    return {"message" :"Email not verified. please try again later!","alert":"warning"}, HTTP_200_OK

            else:
                return {"message" :"Incorrect pin code . Please try again","alert":"warning"}, HTTP_200_OK



@auth_api.post('/verify-code-auth')
def verifyCode_afterLogin(email,code):
    user = check_user(email)
    userValidation = user[4]

    dateCode = str(user[6].strip())
    count5min = duration_time(dateCode)
    if userValidation :
        return {"message" :"User already verified","alert":"success"}
  
    else :
        if count5min > 1:
            return {"message" :"The pin code has expired. Please re-send the verification","alert":"warning"}
        
        else:
            if user[5].strip() == code:
                if verify_user(email):
                    return {"message" :"✔️ Email verified successfully. time to have fun!","alert":"success"}
                else : 
                    return {"message" :"Email not verified. please try again later!","alert":"warning"}

            else:
                return {"message" :"Incorrect pin code . Please try again","alert":"warning"}





@authBasic.verify_password
def verify(username, password):
    if not (username and password):
        return False
    email = username
    hashed_password = hash_password(password)
    user = verify_auth(email,hashed_password)
    if user:
        return True

#Verification user rest version
@auth_api.post("/verify")
@authBasic.login_required
def check():
    try :
        email = request.authorization.username
        code = request.json['code']
        print("code",code)
        messageRes = verifyCode_afterLogin(email,code)
        return jsonify(status=messageRes["alert"], message=messageRes['message']), HTTP_200_OK
    except KeyError:
        return jsonify(status="error", message="Must supply 'code' "), HTTP_400_BAD_REQUEST
    except:
        return jsonify(status="error", message="Invalid json'"), HTTP_400_BAD_REQUEST

