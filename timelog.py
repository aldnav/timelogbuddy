"""
timelog
"""
__author__ = 'Aldrin Navarro'

import datetime
import logging
import os

import dataset
import hiplogging

# Set up a standard logger
logger = logging.getLogger('hipchat')
logger.setLevel(logging.DEBUG)
# Add the standard logging to stderr
logger.addHandler(logging.StreamHandler())

handler = hiplogging.HipChatHandler(os.environ['HIPCHAT_ACCESS_TOKEN'],
                                    os.environ['HIPCHAT_ROOM'])
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
# set up db
db = dataset.connect('sqlite:///test.db')
table = db['timelog']
# send to hipchat?
LOG_TO_CHAT = True
extra = {'color': 'purple', 'from': 'me'}


def log_time_in():
    now = datetime.datetime.now()
    log_time = now.strftime("%H:%M")
    log_date = now.strftime("%Y-%m-%d")
    log_type = 'time in'
    table.insert(dict(
        time=log_time, date=log_date, timestamp=now, type=log_type))
    if LOG_TO_CHAT:
        logger.log(20, "{}: {}".format(log_type, log_time), extra=extra)
    # print 'logged in: ', log_date, log_time


def log_time_out():
    now = datetime.datetime.now()
    log_time = now.strftime("%H:%M")
    log_date = now.strftime("%Y-%m-%d")
    log_type = 'time out'
    table.insert(dict(
        time=log_time, date=log_date, timestamp=now, type=log_type))
    if LOG_TO_CHAT:
        logger.log(20, "{}: {}".format(log_type, log_time), extra=extra)
    # print 'logged out: ', log_date, log_time


def log():
    """ Automatically toggles in/out based on the last logged record """
    last_log = get_last_log()  # if False or type='time out', do time in
    if last_log and last_log['type'] == 'time out':
        log_time_in()
    else:
        log_time_out()


def get_last_log():
    last_log = False
    try:
        result = db.query(
            'SELECT * FROM timelog ORDER BY timestamp DESC LIMIT 1')
    except Exception, e:
        print 'Aborting ...'
        print e
    else:
        last_log = list(result)[-1]
    return last_log


if __name__ == '__main__':
    log()

    for record in table.all():
        print record['type'], record['time']
    print
