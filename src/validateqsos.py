#!/usr/bin/python
import sys, os, _mysql, time
import utils as u
from utils import getLogPath, toTimeStamp, toUnixTime

# get a result from a query
def getQueryResult(db, sql):
    db.query(sql)
    res = db.store_result()
    return res.fetch_row(0);

def main():
    starttime = time.time()
    db = _mysql.connect('localhost', 'wtol', 'wtol', 'wtol')
    db.query('DELETE FROM qso')
    for i in range(0, 16):
        for j in range(0, 16):
            logpath = getLogPath(i, j)
            print 'scanning ' + logpath
            filelist = [ f for f in os.listdir(logpath) if f.endswith(".log") ]
            for filename in filelist:
                callsign = filename.split('.')
                callsign = callsign[0]
                for line in open(logpath + '/' + filename, 'r'):
                    line = line.split('|')
                    callsign_dx = line[0]
                    qso_timestamp = line[1]
                    qso_frequency = line[2]
                    qso_mode = line[3]
                    qso_timestamp_min = toTimeStamp(toUnixTime(qso_timestamp) - (60 * u.QSO_TIME_VARIANCE))
                    qso_timestamp_max = toTimeStamp(toUnixTime(qso_timestamp) + (60 * u.QSO_TIME_VARIANCE))
                    qso_frequency_min = str(int(qso_frequency) - u.QSO_FREQ_VARIANCE)
                    qso_frequency_max = str(int(qso_frequency) + u.QSO_FREQ_VARIANCE)
                    sql = "SELECT COUNT(callsign) AS tot FROM qso WHERE (callsign = '" + callsign_dx + "') AND (callsign_dx = '" + callsign + "') AND (datestart BETWEEN '" + qso_timestamp_min + "' AND '" + qso_timestamp_max + "') AND (frequency BETWEEN '" + qso_frequency_min + "' AND '" + qso_frequency_max + "') AND (mode = '" + qso_mode + "') AND (qsl = 0)"
                    result = getQueryResult(db, sql)
                    if result[0][0] == '0':
                        qsl = '0'
                    else:
                        qsl = '1'
                        sql = "UPDATE qso SET qsl = 1 WHERE (callsign = '" + callsign_dx + "') AND (callsign_dx = '" + callsign + "') AND (datestart BETWEEN '" + qso_timestamp_min + "' AND '" + qso_timestamp_max + "') AND (frequency BETWEEN '" + qso_frequency_min + "' AND '" + qso_frequency_max + "') AND (qsl = 0)"
                        db.query(sql)
                    sql = "INSERT INTO qso VALUES ('" + callsign + "', '" + callsign_dx + "', '" + qso_timestamp + "', '" + qso_frequency + "', '" + qso_mode + "', " + qsl + ")"
                    try:
                        db.query(sql)
                    except:
                        pass
    print 'Elapsed time: ' + str(time.time() - starttime) + ' seconds'
    return

if __name__ == '__main__':
    main()
