# coding:utf8

from unittest import TestCase

from celery.beat import crontab

import auto.cron


def test_func(name='no', job='no'):
    return '{}.{}'.format(name, job)


class TestCron(TestCase):
    def test_update_cron_task(self):
        test_cases = [
            # crontab str
            ('* 10 * * *', test_func, ('sdg', ), {
                'job': 'programmer'
            }, 'tests.test_cron.test_func',
             '[tests.test_cron.test_func | {}]'.format(crontab(hour=10)),
             crontab(hour=10)),
            # run by seconds
            (5, test_func, tuple(), {}, 'tests.test_cron.test_func',
             '[tests.test_cron.test_func | 5]', 5),
        ]
        for cron_settings, func, args, kwargs, \
            expected_task_name, expected_cron_name, expected_schedule \
                in test_cases:
            auto.cron.update_cron_task(cron_settings, func, *args, **kwargs)
            self.assertIn(expected_cron_name, auto.cron.app.conf.beat_schedule)
            self.assertDictEqual({
                'task': expected_task_name,
                'schedule': expected_schedule,
                'args': args,
                'kwargs': kwargs
            }, auto.cron.app.conf.beat_schedule[expected_cron_name])
