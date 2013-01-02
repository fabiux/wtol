#!/usr/bin/python
import sys, os, uuid, random
import utils as u
from utils import getLogPath, toUnixTime, toTimeStamp

# check directories and create them if they don't exist
def checkDirs():
    if not os.path.exists(u.LOGS_ROOT_DIR):
        os.mkdir(u.LOGS_ROOT_DIR)

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
    return open(u.LOGS_ROOT_DIR+'/'+callsign[0]+callsign[1]+'/'+callsign+'.log', 'a')

# return a single log line
def logLine(callsign, timestamp, frequency, mode):
    return callsign+'|'+timestamp+'|'+str(frequency)+'|'+mode+'\n'

def main():
    # number of minutes in the QSO period
    MIN_QSO_UNIXTIME = toUnixTime(u.MIN_QSO_DATE)
    QSO_MINUTES = (int)(toUnixTime(u.MAX_QSO_DATE) - MIN_QSO_UNIXTIME) / 60

    # check log directories
    checkDirs()

    # delete old logs
    deleteLogs()

    # init callsigns list
    callsigns = []
    for i in range(0, u.CALLSIGN_NUM):
        uid = uuid.uuid4()
        callsigns.append(uid.hex)

    # generate log for each callsign
    qsocount = 0
    qslcount = 0
    for callsign in callsigns:
        f = openLog(callsign)
        qso_num = random.randint(u.MIN_QSO_NUM, u.MAX_QSO_NUM)
        for i in range(0, qso_num):
            qsocount += 1
            othercallsign = callsigns[random.randint(0, u.CALLSIGN_NUM - 1)]
            minutes = random.randint(0, QSO_MINUTES)
            timestamp = toTimeStamp(MIN_QSO_UNIXTIME + (minutes * 60))
            frequency = random.randint(u.MIN_QSO_FREQ + u.QSO_FREQ_VARIANCE, u.MAX_QSO_FREQ - u.QSO_FREQ_VARIANCE)
            mode = u.modes[random.randint(0, 3)]
            if callsign <> othercallsign:
                f.write(logLine(othercallsign, timestamp, frequency, mode))
                if random.randint(1, 100) <= u.QSL_QSO_RATE:
                    qslcount += 1
                    t = toUnixTime(timestamp)
                    minutes = random.randint(-u.QSO_TIME_VARIANCE, u.QSO_TIME_VARIANCE)
                    t += minutes * 60
                    timestamp2 = toTimeStamp(t)
                    frequency2 = frequency + random.randint(-u.QSO_FREQ_VARIANCE, u.QSO_FREQ_VARIANCE)
                    f2 = openLog(othercallsign)
                    f2.write(logLine(callsign, timestamp2, frequency2, mode))
                    f2.close()
        f.close()
    print 'QSO: ' + str(qsocount)
    print 'QSL: ' + str(qslcount)
    return

if __name__ == '__main__':
	main()
