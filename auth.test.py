from mimetypes import init
import uuid
import unittest
from api import create_app


class FlaskTest(unittest.TestCase):

    def test_register(self):
        application = create_app()

        uniqueId = "dmt"+str(uuid.uuid1())
        tester = application.test_client(self) 
        response = tester.post("/api/v1/auth/register", json={
            "email":uniqueId+"@gmail.com","password":"11aa113Y12"
        })
        self.assertEqual(response.status_code,201)
        print("Client registration complete")

    def test_register_fileds(self):
        application = create_app()

        tester = application.test_client(self) 
        response = tester.post("/api/v1/auth/register", json={
            "email":"dd@gmail.com"
        })
        self.assertEqual(response.json["message"],"Must supply 'email' and 'password'")
        print("Field required complete")

    
    def test_verify_code(self):
        application = create_app()

        tester = application.test_client(self) 
        response = tester.post("/api/v1/auth/verify-code", json={
            "email":"webenfly@gmail.com","code":'1234'
        })
        self.assertEqual(response.json["message"],"The pin code has expired. Please re-send the verification")
        print("Code verification complete")


if __name__ == "__main__":
    unittest.main() 
    flaskTest = FlaskTest()
    flaskTest.test_register_fileds()
    flaskTest.test_register()
    flaskTest.test_verify_code()
    