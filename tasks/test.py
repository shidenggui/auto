from celery import shared_task

from auto.cron import cron_task, add_cron_task


@cron_task('* * * * *')
def cron_by_crontab():
    print('run every minute')


@cron_task(5)
def cron_by_second():
    print('run every 5 seconds')


@cron_task(5, name='sdg')
def cron_by_args(name):
    print('call by args: ', name)


@add_cron_task(5)
@shared_task(bind=True)
def cron_by_bind(self):
    print('bind celery self: ', self)
