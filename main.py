from log_entity import LogEntity
from datetime import timedelta

totalNodeCount = 50

def get_node_id(str):
    splitData = str.split(':')
    return int(splitData[1])

def get_timedelta(deltaStr):
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


def calculate_battery_usage(id1,id2,char_length):
    diff = abs(id1 - id2)

    #maximum number of distance to travel
    m = 4
    remaining = diff%m
    div = int(diff/m)

    total = remaining * remaining * char_length
    for d in range(0,div):
        total += m * m * char_length

    return total


if __name__ == "__main__":

    total_node_count = 10

    filepath = '20NLoglistener.txt'

    metric_logs = []
    with open(filepath) as fp:
       line = fp.readline()
       while line:
           splitLine = line.split('\t')
           delta = get_timedelta(splitLine[0])
           node_id = get_node_id(splitLine[1])
           data = splitLine[2].rstrip()
           if(data.startswith("LOG")):
               metric_logs.append(LogEntity(node_id,delta,data))
           line = fp.readline()


    total_network_request_count_without_data_aggregation = 0
    total_network_request_bandwidth_with_data_aggregation = 0

    total_network_request_count_with_data_aggregation = 0
    total_network_request_bandwidth = 0

    totalMaxBatteryUsage = 0
    totalMinBatteryUsage = 0

    for metric_log in metric_logs:
        if metric_log.log_type == "TEMPARATURE" or metric_log.log_type == "AVAILABILITY":
           network_count_needed = total_node_count-1
           total_network_request_count_without_data_aggregation += network_count_needed
           total_network_request_bandwidth_with_data_aggregation += network_count_needed*5
           totalMaxBatteryUsage += calculate_battery_usage(10-metric_log.node_id,metric_log.node_id,3)
           totalMaxBatteryUsage += calculate_battery_usage(0, metric_log.node_id,3)
        elif metric_log.log_type == "SENT":
            totalMinBatteryUsage+=len(metric_log.network_data)
            total_network_request_count_with_data_aggregation +=1
            total_network_request_bandwidth += len(metric_log.network_data)

    print("Request Count Ratio: \t\t",total_network_request_count_without_data_aggregation,"-",total_network_request_count_with_data_aggregation)
    print("BandwidthRatio: \t\t\t",total_network_request_bandwidth_with_data_aggregation,"-",total_network_request_bandwidth)
    print("Energy consumption ratio: \t",totalMaxBatteryUsage,"-",totalMinBatteryUsage)

    #delay
    totalDelay = timedelta()
    delayCount = 0
    count = len(metric_logs)
    for i in range(count):
        if metric_logs[i].log_type == "TEMPARATURE" or metric_logs[i].log_type == "AVAILABILITY":
            dataGeneratorLog = metric_logs[i]
            startTime = dataGeneratorLog.delta
            delayCount +=1
            if(count != i-1):
                breakFirstNode = False
                for j in range(i+1,count):
                    endCandidateLog = metric_logs[j]
                    if(endCandidateLog.node_id == 1 and endCandidateLog.log_type == "RECEIVED"):
                        network_data = endCandidateLog.network_data

                        split_network_data = network_data.split('|')

                        if(metric_logs[i].log_type == "TEMPARATURE"):
                            temperatureStr = split_network_data[2]
                            temperatureSplit = temperatureStr.split(';')

                            for temperatureItem in temperatureSplit:
                                if(temperatureItem):
                                    temperaturePair = temperatureItem.split(':')
                                    if dataGeneratorLog.temperature == float(temperaturePair[0]):
                                        nodeIds= map(int,temperaturePair[1].split(','))
                                        if(dataGeneratorLog.node_id in nodeIds):
                                            totalDelay += endCandidateLog.delta - dataGeneratorLog.delta
                                            breakFirstNode = True
                                            break
                            if(breakFirstNode):
                                break
    print("Average Delay: \t\t\t\t",totalDelay/delayCount)











