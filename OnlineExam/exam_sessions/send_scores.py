import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
import ssl


class TlsAdapter(HTTPAdapter):

  def __init__(self, ssl_options=0, **kwargs):
    self.ssl_options = ssl_options
    super(TlsAdapter, self).__init__(**kwargs)

  def init_poolmanager(self, *pool_args, **pool_kwargs):
    ctx = ssl_.create_urllib3_context(cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
    self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

URL = 'https://bpms.cao.ir/NetForm/Service/irexamresult/request'


def send_score(ref_code, nid, score, date, passed=0):

    js = {
            "course": ref_code,
            "nid": nid,
            "score": score,
            "date": date,
            "passed": passed
          }
    sess = requests.session()
    adp = TlsAdapter(ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1_3)
    sess.mount(URL, adp)
    response=sess.post(URL, json=js)

    return response.json()
