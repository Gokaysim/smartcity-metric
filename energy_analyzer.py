from helpers import get_max_node_id


def calculate_battery_usage(id1,id2,char_length):
    diff = abs(id1 - id2)

    # maximum number of distance to travel
    m = 4
    remaining = diff % m
    div = int(diff / m)

    total = remaining * remaining * char_length
    for d in range(0, div):
        total += m * m * char_length

    return total

def analyzer_energy_consuption(metric_logs):
    total_energy_consumption = 0
    total_energy_consumption2 = 0
    bandthwidth = 0
    request_count = 0

    for metric_log in metric_logs:
        if metric_log.log_type == "SENT":
            total_energy_consumption2 += len(metric_log.network_data)+ len(metric_log.network_data) * (abs(metric_log.node_id-metric_log.from_node_id)**2)
            total_energy_consumption +=  + len(metric_log.network_data) * (
                        abs(metric_log.node_id - metric_log.from_node_id) ** 2)
            bandthwidth += len(metric_log.network_data)
            request_count +=1

    # print("Request Count Ratio: \t\t",
    #       total_network_request_count_without_data_aggregation / total_network_request_count_with_data_aggregation)
    # print("BandwidthRatio: \t\t\t",
    #       total_network_request_bandwidth_with_data_aggregation / total_network_request_bandwidth)
    # print("Energy consumption ratio: \t",total_max_battery_usage/total_min_battery_usage)


    return {
        "total_energy_consumption":total_energy_consumption,
        "total_energy_consumption2":total_energy_consumption2,
        "bandthwidth":bandthwidth,
        "request_count":request_count
    }
    # return {
    #     "request_count_ratio": total_network_request_count_without_data_aggregation/total_network_request_count_with_data_aggregation,
    #     "bandwidth_ratio" :total_network_request_bandwidth_with_data_aggregation / total_network_request_bandwidth,
    #     "energy_consumption_ratio":total_max_battery_usage/total_min_battery_usage
    # }
