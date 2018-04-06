# coding:utf8
import os


def load_tasks(folder='tasks'):
    """
    return python files module name under folder
    :param folder: folder name
    :return: list of python module name
    :rtype: list
    """
    includes = []
    for file in os.listdir(folder):
        if not file.endswith('.py'):
            continue
        basename = os.path.splitext(file)[0]
        includes.append('{}.{}'.format(folder, basename))
    return includes
