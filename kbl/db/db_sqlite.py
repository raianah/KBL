from sqlite3 import connect
from os.path import isfile
from apscheduler.triggers.cron import CronTrigger

BUILD_PATH = "./data/db/build.sql"
DB_PATH = "./data/db/database.db"

"""

    Using this file requires 'apscheduler', which is not included in requirements.txt. You must exclusively include the package if you wish to use this.

"""

conn = connect(DB_PATH, check_same_thread=False)

cxn = conn.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner

@with_commit
def build():
    if isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

def commit():
    conn.commit()

def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))

def close():
    cxn.close()

def field(command, *values):
    cxn.execute(command, tuple(values))

    if (fetch := cxn.fetchone()) is not None:
        return fetch[0]

def record(command, *values):
    cxn.execute(command, tuple(values))

    return cxn.fetchone()

def records(command, *values):
    cxn.execute(command, tuple(values))

    return cxn.fetchall()

def column(command, *values):
    cxn.execute(command, tuple(values))
    
    return [item[0] for item in cxn.fetchall()]

def execute(command, *values):
    cxn.execute(command, tuple(values))

def multiexec(command, valueset):
    cxn.executemany(command, valueset)

def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cxn.executescript(script.read())