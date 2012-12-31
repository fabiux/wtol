from datetime import datetime
from time import mktime

# constants
CALLSIGN_NUM = 100
MIN_QSO_NUM = 100
MAX_QSO_NUM = 500
MIN_QSO_DATE = '2012-12-01 00:00:00'
MAX_QSO_DATE = '2013-01-01 00:00:00'
MIN_QSO_FREQ = 14000    # kHz
MAX_QSO_FREQ = 14350    # kHz
QSO_TIME_VARIANCE = 5   # minutes
QSO_FREQ_VARIANCE = 3   # kHz
QSL_QSO_RATE = 80       # add comment
modes = ['SSB', 'CW', 'RTTY', 'JT65']

LOGS_ROOT_DIR = 'logs'

# get log directory path from two decimal indexes
def getLogPath(i, j):
    i = hex(i)
    j = hex(j)
    return LOGS_ROOT_DIR+'/'+i[2]+j[2]

# convert a timestamp to UNIX time
def toUnixTime(timestamp):
    t = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return mktime(t.timetuple())

# convert a UNIX time to timestamp
def toTimeStamp(unixtime):
    t = datetime.fromtimestamp(unixtime)
    return t.strftime("%Y-%m-%d %H:%M:%S")
