from datetime import date
from apscheduler.scheduler import Scheduler
import time




def my_job():
   print int(time.time())
# Start the scheduler
sched = Scheduler()
sched.start()

#start the morning
job = sched.add_cron_job(my_job,day_of_week='0,1,2,3,4',hour='9',minute='30')
#stop the morning


while(True):
    print 'my sleep'+str(int(time.time()))
    time.sleep(1000000)
    pass
