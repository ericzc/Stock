from datetime import date
from apscheduler.scheduler import Scheduler
import time

import requests


r = requests.get('http://www.baidu.com')
#print r.headers
print r.status_code
print r.text













