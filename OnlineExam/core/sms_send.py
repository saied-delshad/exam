import requests
from pytz import timezone
import json

URL = 'https://new.payamsms.com/services/rest/index.php'


def send_sms(applicant_cell, applicant_fullname, exam_name, exam_date_time, custom_message = None):

    exam_date = exam_date_time.date().strftime("%d/%m/%Y")

    exam_time = exam_date_time.astimezone(timezone('Asia/Tehran')).time().strftime('%H:%M')

    
    if custom_message == None:
        raw_message= """Dear Applicant {0}, You have successfully registered in exam: {1}, Exam Date: {2}, Exam Time:{3} Civil Aviation Authority of the Islamic Republic of Iran""".format(applicant_fullname, exam_name, exam_date, exam_time)
    else:
        raw_message = custom_message

    
    js = {
            "organization": "SHK",
            "username": "exam",
            "password": "753951",
            "method": "send",
            "messages":[
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
