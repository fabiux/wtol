#!/usr/bin/python
import sys, os, uuid, random
from datetime import datetime
from time import mktime

# get log directory path from two decimal indexes
def getLogPath(i, j):
    i = hex(i)
    j = hex(j)
    return 'logs/'+i[2]+j[2]

# check directories and create them if they don't exist
def checkDirs():
    for i in range(0, 16):
        for j in range(0, 16):
            logpath = getLogPath(i, j)
            if not os.path.exists(logpath):
                os.mkdir(logpath)
    return

# remove all logs
def deleteLogs():
    for i in range(0, 16):
        for j in range(0, 16):
            logpath = getLogPath(i, j)
            filelist = [ f for f in os.listdir(logpath) if f.endswith(".log") ]
            for f in filelist:
                os.remove(logpath+'/'+f)
    return

# open a log file for append
def openLog(callsign):
    return open('logs/'+callsign[0]+callsign[1]+'/'+callsign+'.log', 'a')

# convert a timestamp to UNIX time
def toUnixTime(timestamp):
    t = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return mktime(t.timetuple())

# convert a UNIX time to timestamp
def toTimeStamp(unixtime):
    t = datetime.fromtimestamp(unixtime)
    return t.strftime("%Y-%m-%d %H:%M:%S")

# return a single log line
def logLine(callsign, timestamp, frequency, mode):
    return callsign+'|'+timestamp+'|'+str(frequency)+'|'+mode+'\n'

def main():
    # constants
    CALLSIGN_NUM = 10000
    MIN_QSO_NUM = 100
    MAX_QSO_NUM = 500
    MIN_QSO_DATE = '2012-12-01 00:00:00'
    MAX_QSO_DATE = '2013-01-01 00:00:00'
    QSO_TIME_VARIANCE = 5   # minutes FIXME move to library
    MIN_QSO_FREQ = 14000    # kHz
    MAX_QSO_FREQ = 14350    # kHz
    QSO_FREQ_VARIANCE = 3   # kHz FIXME move to library
    QSL_QSO_RATE = 80       # add comment

    modes = ['SSB', 'CW', 'RTTY', 'JT65']

    # number of minutes in the QSO period
    MIN_QSO_UNIXTIME = toUnixTime(MIN_QSO_DATE)
    QSO_MINUTES = (int)(toUnixTime(MAX_QSO_DATE) - MIN_QSO_UNIXTIME) / 60

    # check log directories
    checkDirs()

    # delete old logs
    deleteLogs()

    # init callsigns list
    callsigns = []
    for i in range(0, CALLSIGN_NUM):
        uid = uuid.uuid4()
        callsigns.append(uid.hex)

    # generate log for each callsign
    qsocount = 0
    qslcount = 0
    for callsign in callsigns:
        f = openLog(callsign)
        qso_num = random.randint(MIN_QSO_NUM, MAX_QSO_NUM)
        for i in range(0, qso_num):
            qsocount += 1
            othercallsign = callsigns[random.randint(0, CALLSIGN_NUM - 1)]
            minutes = random.randint(0, QSO_MINUTES)
            timestamp = toTimeStamp(MIN_QSO_UNIXTIME + (minutes * 60))
            frequency = random.randint(MIN_QSO_FREQ + QSO_FREQ_VARIANCE, MAX_QSO_FREQ - QSO_FREQ_VARIANCE)
            mode = modes[random.randint(0, 3)]
            if callsign <> othercallsign:
                f.write(logLine(othercallsign, timestamp, frequency, mode))
                if random.randint(1, 100) <= QSL_QSO_RATE:
                    qslcount += 1
                    t = toUnixTime(timestamp)
                    minutes = random.randint(-QSO_TIME_VARIANCE, QSO_TIME_VARIANCE)
                    t += minutes * 60
                    timestamp2 = toTimeStamp(t)
                    frequency2 = frequency + random.randint(-QSO_FREQ_VARIANCE, QSO_FREQ_VARIANCE)
                    f2 = openLog(othercallsign)
                    f2.write(logLine(callsign, timestamp2, frequency2, mode))
                    f2.close()
        f.close()
    print 'QSO: ' + str(qsocount)
    print 'QSL: ' + str(qslcount)
    return

if __name__ == '__main__':
	main()
