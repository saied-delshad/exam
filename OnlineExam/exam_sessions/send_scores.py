import requests


URL = 'https://bpms.cao.ir/NetForm/Service/examresult/request'


def send_score(ref_code, nid, score, date, passed=0):

    js = {
            "course": ref_code,
            "nid": nid,
            "score": score,
            "date": date,
            "passed": passed
          }

    response = requests.post(URL, json=js, verify=False)
    print(response.json)
    return response
