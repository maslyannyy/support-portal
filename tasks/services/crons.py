import getpass
import os

from crontab import CronTab

_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def write_task(is_active: bool, script: str, sleep: int, param: str, *args, **kwargs):
    """Добавляет или удалят крон с именем script, в зависимоти от state"""
    os_user = getpass.getuser()
    cron_tabs = CronTab(user=os_user)

    if not is_active:
        for cron in cron_tabs.find_command(script):
            if f'sleep {sleep}' in str(cron):
                cron_tabs.remove(cron)
        cron_tabs.write()
        return

    cron = cron_tabs.new(command=f'sleep {sleep}; python3 {os.path.join(_PATH, "manage.py")} {script}')
    cron.setall(param)
    cron_tabs.write()


def clear_all_tasks():
    os_user = getpass.getuser()
    cron_tabs = CronTab(user=os_user)
    cron_tabs.remove_all()
    cron_tabs.write()
