class LogEntity:
    def __init__(self,node_id,delta,line):
        split = line.split(" ")

        self.delta = delta
        self.log_type = split[1]
        self.node_id = node_id

        if self.log_type == "RECEIVED":
            self.network_data = split[2]
        elif self.log_type == "SENT":
            self.from_node_id = split[2]
            self.network_data = split[3]
        elif self.log_type == "TEMPARATURE":
            self.temperature = float(split[2])
        elif self.log_type == "AVAILABILITY":
            self.empty = bool(split[2])
        else:
            self.other_node_id