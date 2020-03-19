from log_entity import LogEntity
from datetime import timedelta
from file_reader import get_metric_logs_from_file
from helpers import get_max_node_id
from coap_request_parser import CoapRequestParser
totalNodeCount = 50

if __name__ == "__main__":
    metric_logs = get_metric_logs_from_file("loglistener.txt")
    print("Max node id",get_max_node_id(metric_logs))
    print("Total",len(metric_logs))
    r = filter(lambda x:x.log_type == "AVAILABILITY",metric_logs)

    print("AVAILABILITY count",len(list(r)))


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

def calculate_delay(metric_logs):
    max_node_id = max(metric_logs,key= lambda x:x.node_id).node_id
    min_node_id = min(metric_logs, key=lambda x: x.node_id).node_id

    filtered_availability_array = filter(lambda x: x.log_type == "AVAILABILITY", metric_logs)
    for element in filtered_availability_array:
        empty = element.empty
        sent_to_max_edge = filter(lambda x:x.node_id == max_node_id and x.delta>element.delta and x.log_type == "RECEIVED",metric_logs)
        for edge_receive in sent_to_max_edge:
            # print(edge_receive.network_data)
            emptinessVal = edge_receive.network_data.split("|")[1]
            if(emptinessVal):
                emptinessValSeperate = emptinessVal.split(";")
                v = emptinessValSeperate[0].split(":");
                if int(v[0])==1 and empty:
                    # print(get_node_ids(v[1]))
                    pass
                elif len(emptinessValSeperate)>1 and emptinessValSeperate[1]:
                    # print(emptinessValSeperate[1])
                    pass



def get_last_and_first(var):
    return var.node_id ==1 or var.node_id == 20

def get_node_ids(node_ids):
    split_node_ids = node_ids.split(",");

    ni = []
    for node_id in split_node_ids:
        ni.append(int(node_id))
    return ni

def get_as_object(data):
    first_split = data.split("|")
    availability = first_split[1]
    temperature = first_split[2]
    objs = []

    if(availability is not None):
        empty_not_empty_array = availability.split(";")

        for empty_not_empty in empty_not_empty_array:

            if empty_not_empty != "":
                vv = empty_not_empty.split(":")
                value = vv[0]

                node_ids= get_node_ids(vv[1])
                for node_id in node_ids:
                    objs.append({
                        "type":"AVAILABILITY",
                        "node_id":node_id,
                        "empty":int(value)
                    })

    if(temperature is not None):
        temperaturesArray = temperature.split(";")
        for temperatureItem in temperaturesArray:
            if temperatureItem != "":
                vv = temperatureItem.split(":")
                value = vv[0]

                node_ids = get_node_ids(vv[1])

                for node_id in node_ids:
                    objs.append({
                        "type":"TEMPARATURE",
                        "node_id":node_id,
                        "temperature":float(value)
                    })
    return objs;







def f():
    total_node_count = 10

    filepath = 'loglistener.txt'

    metric_logs = []
    with open(filepath) as fp:
       line = fp.readline()
       while line:
           splitLine = line.split('\t')
           delta = get_timedelta(splitLine[0])
           node_id = get_node_id(splitLine[1])
           data = splitLine[2].rstrip()
           if(data.startswith("LOG")):
               try:
                metric_logs.append(LogEntity(node_id,delta,data))
               except :
                pass
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

    print("Request Count Ratio: \t\t",total_network_request_count_without_data_aggregation/total_network_request_count_with_data_aggregation)
    print("BandwidthRatio: \t\t\t",total_network_request_bandwidth_with_data_aggregation/total_network_request_bandwidth)
    print('sadasd:',total_network_request_bandwidth_with_data_aggregation)
    print("Energy consumption ratio: \t",totalMaxBatteryUsage/totalMinBatteryUsage)

    #delay


    print("ssssss",len(list(filter(lambda x:x.log_type == "AVAILABILITY",metric_logs))))


    calculate_delay(metric_logs)
    vardd =filter(lambda x:x.log_type == "RECEIVED",metric_logs);
    l = 0
    for vardditem in vardd:
        l +=len(vardditem.network_data)

    filteredNodes = filter(get_last_and_first,metric_logs)

    totalDelay =timedelta()
    delayCount = 0

    for s in filteredNodes:
        if s.log_type == "RECEIVED":
            netword_data = s.network_data
            object_array = get_as_object(netword_data)
            for object in object_array:
                if(object["type"] == "AVAILABILITY"):
                    b = bool(object["empty"])
                    # print(object["node_id"],object["type"])
                    resource = next(filter(lambda x: x.node_id == object["node_id"] and x.log_type == object["type"] and x.empty == b, metric_logs), None)
                    if(resource is not None):
                        metric_logs.remove(resource)
                        # print(s.delta - resource.delta,resource.delta,s.delta)
                        if resource.delta != 0 and s.delta!=0:
                            totalDelay += s.delta - resource.delta
                            delayCount +=1

    if(delayCount !=0):
        print("avg delay\t",(totalDelay/delayCount))
        print("Delay Count",delayCount)
    else:
        print("avg delay]t", 0)
    # totalDelay = timedelta()
    # delayCount = 0
    # count = len(metric_logs)
    # for i in range(count):
    #     if metric_logs[i].log_type == "TEMPARATURE" or metric_logs[i].log_type == "AVAILABILITY":
    #         dataGeneratorLog = metric_logs[i]
    #         startTime = dataGeneratorLog.delta
    #         delayCount +=1
    #         if(count != i-1):
    #             breakFirstNode = False
    #             for j in range(i+1,count):
    #                 endCandidateLog = metric_logs[j]
    #                 if(endCandidateLog.node_id == 1 and endCandidateLog.log_type == "RECEIVED"):
    #                     network_data = endCandidateLog.network_data
    #
    #                     split_network_data = network_data.split('|')
    #
    #                     if(metric_logs[i].log_type == "TEMPARATURE"):
    #                         temperatureStr = split_network_data[2]
    #                         temperatureSplit = temperatureStr.split(';')
    #
    #                         for temperatureItem in temperatureSplit:
    #                             if(temperatureItem):
    #                                 temperaturePair = temperatureItem.split(':')
    #                                 if dataGeneratorLog.temperature == float(temperaturePair[0]):
    #                                     nodeIds= map(int,temperaturePair[1].split(','))
    #                                     if(dataGeneratorLog.node_id in nodeIds):
    #                                         totalDelay += endCandidateLog.delta - dataGeneratorLog.delta
    #                                         breakFirstNode = True
    #                                         break
    #                         if(breakFirstNode):
    #                             break
    # print("Average Delay: \t\t\t\t",totalDelay/delayCount)











