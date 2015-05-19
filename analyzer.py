__author__ = 'eric'

# -*- coding: utf-8 -*-



import os
import time
from time import localtime,strftime
import datetime
from apscheduler.scheduler import Scheduler
from manager import Manager


sched = Scheduler()

STOCK_LIST = [

              'sz000725',
              'sh600307',
              'sh600010',
              'sz000825',
              'sh601390'
              ]



def main():

    mgr = Manager()
    mgr.add_stocklist( STOCK_LIST )
    mgr.start_realtime()


    sched.start()
    jobstartmorning = sched.add_cron_job(mgr.start_realtime(),day_of_week='0,1,2,3,4',hour='9',minute='30')
    jobstartnoon = sched.add_cron_job(mgr.start_realtime(),day_of_week='0,1,2,3,4',hour='13',minute='0')
    #jobsummarystart = sched.add_cron_job(mgr.start_realtime(),day_of_week='0,1,2,3,4',hour='20',minute='0')

    while(True):
        print'waiting for the next trace!!'
        time.sleep(100)

if __name__ == "__main__":
    main()

