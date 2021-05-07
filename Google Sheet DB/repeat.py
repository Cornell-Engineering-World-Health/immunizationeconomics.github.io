from crontab import CronTab
from datetime import datetime

cron = CronTab(user='alisonlandry')
job = cron.new(command='python main.py')
job.minute.every(240)

cron.write()
