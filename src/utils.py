# get log directory path from two decimal indexes
def getLogPath(i, j):
    i = hex(i)
    j = hex(j)
    return 'logs/'+i[2]+j[2]

# convert a timestamp to UNIX time
def toUnixTime(timestamp):
    t = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return mktime(t.timetuple())

# convert a UNIX time to timestamp
def toTimeStamp(unixtime):
    t = datetime.fromtimestamp(unixtime)
    return t.strftime("%Y-%m-%d %H:%M:%S")
