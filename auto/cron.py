import functools

from celery import Celery, shared_task
from celery.schedules import crontab

from auto.utils import load_tasks

app = Celery("auto", include=load_tasks())
app.config_from_object("settings")


def register_sentry():
    """register sentry for celery"""
    from raven import Client
    from raven.contrib.celery import register_signal, register_logger_signal

    dsn = app.conf.get("sentry_dsn")
    if dsn is None:
        return
    client = Client(dsn)

    # register a custom filter to filter out duplicate logs
    register_logger_signal(client)

    # hook into the Celery error handler
    register_signal(client)


register_sentry()


def update_cron_task(cron, func, *args, **kwargs):
    """update cron task to app.conf.beat_schedule
    :param cron: cron setting
    :type cron: str or int or schedule format
    :param func: cron task func
    :type func: function
    :param args: args pass to task
    :type args: list
    :param kwargs: kwargs pass to task
    :type kwargs: dict
    """
    if isinstance(cron, str):
        cron = crontab(*cron.split(" "))
    task = "{}.{}".format(func.__module__, func.__name__)
    cron_name = "[{task} | {cron}]".format(task=task, cron=cron)
    app.conf.beat_schedule.update(
        {
            cron_name: {
                "task": task,
                "schedule": cron,
                "args": args,
                "kwargs": kwargs,
            }
        }
    )


def cron_task(cron, *args, **kwargs):
    """add cron task to celery beat_schedule
    :param cron: cron setting
    :type cron: str or int or schedule format
    :param args: args pass to task
    :type args: list
    :param kwargs: kwargs pass to task
    :type kwargs: dict
    """

    def decorator(f):
        update_cron_task(cron=cron, func=f, *args, **kwargs)

        @shared_task
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator


def add_cron_task(cron, *args, **kwargs):
    """add cron task to celery beat_schedule,
    but need manually specific shared task decorator
    :param cron: cron setting
    :type cron: str or int or schedule format
    :param args: args pass to task
    :type args: list
    :param kwargs: kwargs pass to task
    :type kwargs: dict
    """

    def decorator(f):
        update_cron_task(cron=cron, func=f, *args, **kwargs)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator
