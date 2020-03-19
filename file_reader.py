from log_entity import LogEntity
from helpers import get_node_id,get_timedelta

def get_metric_logs_from_file(file_name):
    metric_logs = []
    with open(file_name) as fp:
        line = fp.readline()
        while line:
            splitLine = line.split('\t')
            delta = get_timedelta(splitLine[0])
            node_id = get_node_id(splitLine[1])
            data = splitLine[2].rstrip()
            if (data.startswith("LOG")):
                try:
                    metric_logs.append(LogEntity(node_id, delta, data))
                except Exception as e: print(e)
            line = fp.readline()
    return metric_logs