# coding:utf8

from unittest import TestCase, mock

import auto.utils


class TestUtils(TestCase):
    @mock.patch('auto.utils.os.listdir')
    def test_load_tasks(self, mock_listdir):
        test_cases = [
            # listdir return empty files
            ('tasks', [], []),
            # listdir return python files and other files
            ('tasks', ['a.py', 'b'], ['tasks.a']),
        ]
        for folder, listdir_return, expected_include in test_cases:
            mock_listdir.return_value = listdir_return
            result = auto.utils.load_tasks(folder)
            self.assertListEqual(result, expected_include)
