# auto
Easy use python cron tasks template based on celery

## Usage


1. Git clone

```bash
git clone https://github.com/shidenggui/auto
```

2. Create settings.py

```bash
cp settings.example.py settings.py
```

3. Edit settings.py

Edit settings in settings.py, options based on [celery configuration](http://docs.celeryproject.org/en/latest/userguide/configuration.html)

You can set `sentry_dsn` value to enable sentry's celery integration


4. Create your cron tasks python file under tasks folder

examples in `tasks/tests.py`
```python
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
    print('run every 5 seconds, call by args: ', name)


@add_cron_task(5)
@shared_task(bind=True)
def cron_by_bind(self):
    print('run ervery 5 seconds, bind celery self: ', self)
```

4. Run

```bash
celery worker -A auto.cron -B
```
