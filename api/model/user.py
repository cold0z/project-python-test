import json
from flask import jsonify


class User():
    
     def __init__(self, email, password, registration_date,active, code,code_date):


        self.email = email
        self._password = None
        self.registration_date = registration_date
        self.active = active
        self.code = code
        self.code_date = code_date
        self.password = password

        


     def password(self):
        # The getter just returns it.
        return self._password

     def password(self, new_password):
        # The setter does the needed calculation.
        self._password = new_password

    
     def serialize(self):
        return {"email": self.email,
                "active": self.active,
                "code": self.code,
                "registration_date": self.registration_date,
                } 
            
     def __str__(self):
        return jsonify("")
     
