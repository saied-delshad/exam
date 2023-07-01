import requests
import json

URL = 'https://new.payamsms.com/services/rest/index.php'


def send_sms(applicant_cell, applicant_fullname, exam_name, exam_date):

    
    raw_message= "Dear Applicant {0}, You have successfully registered in exam: {1}, Exam Date: {2}".format(applicant_fullname, exam_name, str(exam_date))

    print(raw_message)
    
    js = {
            "organization": "SHK",
            "username": "exam",
            "password": "753951",
            "method": "send",
            "message":[
                {
                    "sender": "98200097109",
                    "recipient": str(applicant_cell),
                    "body": raw_message,
                    "customerId": 2 
                }
            ]
          }
    response = requests.post(URL, json=js, verify=False)
    print(response.json())
    return response
