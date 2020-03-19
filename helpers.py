from datetime import timedelta

def get_node_id(str):
    splitData = str.split(':')
    return int(splitData[1])

def get_timedelta(deltaStr):

    if not ":" in deltaStr:
        d = timedelta(milliseconds=int(deltaStr))
        return d

    splitDeltaStr = deltaStr.split('.')
    milliSeconds = int(splitDeltaStr[1])

    timeSplit = splitDeltaStr[0].split(':')

    count = len(timeSplit)

    seconds = 0
    minutes = 0
    hours = 0
    days = 0

    if(count>0):
        seconds = int(timeSplit[count-1])
        count = count -1

    if (count > 0):
        minutes = int(timeSplit[count - 1])
        count = count - 1

    if (count > 0):
        hours = int(timeSplit[count - 1])
        count = count - 1

    if (count > 0):
        days = int(timeSplit[count - 1])
        count = count - 1


    return timedelta(milliseconds=milliSeconds,seconds = seconds,minutes=minutes,days=days,hours=hours)


def get_max_node_id(metric_logs):
    return max(metric_logs,key=lambda x:x.node_id).node_id