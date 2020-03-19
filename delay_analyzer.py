from helpers import get_max_node_id
from datetime import timedelta

def analyze_delay(metric_logs):
    max_node_id = get_max_node_id(metric_logs)

    availability_logs = filter(lambda x: x.log_type == "AVAILABILITY", metric_logs)


    total_time = timedelta()
    count = 0
    for availability_log in availability_logs:
        [temp_count2,temp_total_time2] = part(availability_log, metric_logs, max_node_id)

        count +=  temp_count2
        total_time +=   temp_total_time2

    if count == 0:
        count = 1

    return {
        "total_delay":total_time,
        "delay_count":count,
        "average_delay":total_time/count
    }

def part(availability_log,metric_logs,edge_node):
    total_time = timedelta()
    count = 0
    if (availability_log.empty == 1):
        filtered_nodes = filter(lambda x: x.node_id == edge_node
                                          and x.log_type == "RECEIVED"
                                          and x.delta > availability_log.delta
                                          # and hasattr(x, "parsed_data")
                                          and hasattr(x.parsed_data, "available_node_ids")
                                          and availability_log.node_id in x.parsed_data.available_node_ids
                                ,
                                metric_logs)

        last_node = next(filtered_nodes, None)
        if (last_node):
            total_time += last_node.delta - availability_log.delta
            count += 1


        filtered_nodes = filter(lambda x: x.node_id == 1
                                               and x.log_type == "RECEIVED"
                                               and availability_log.delta > availability_log.delta
                                               and x.parsed_data.available_node_ids
                                               and availability_log.node_id in x.parsed_data.available_node_ids
                                     , metric_logs)

        last_node = next(filtered_nodes, None)
        if (last_node):
            total_time += last_node.delta - availability_log.delta
            count += 1
    else:
        filtered_nodes = filter(lambda x: x.node_id == edge_node
                                          and x.log_type == "RECEIVED"
                                          and x.delta > availability_log.delta
                                          # and hasattr(x, "parsed_data")
                                          and hasattr(x.parsed_data, "not_available_node_ids")
                                          and availability_log.node_id in x.parsed_data.not_available_node_ids
                                ,
                                metric_logs)

        last_node = next(filtered_nodes, None)
        if (last_node):
            total_time += last_node.delta - availability_log.delta
            count += 1

        filtered_nodes = filter(lambda x: x.node_id == 1
                                               and x.log_type == "RECEIVED"
                                               and availability_log.delta > availability_log.delta
                                               and x.parsed_data.not_available_node_ids
                                               and availability_log.node_id in x.parsed_data.not_available_node_ids
                                     , metric_logs)

        last_node = next(filtered_nodes, None)
        if (last_node):
            total_time += last_node.delta - availability_log.delta
            count += 1

    return [count,total_time]