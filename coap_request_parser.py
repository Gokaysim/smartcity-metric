

def get_node_ids_from_str(str):
    split_str = str.split(",")

    node_ids =[]
    for item in split_str:
        if(item):
            node_ids.append(int(item))

    return node_ids

class CoapRequestParser:
    def __init__(self,network_data):

        target_id_and_rest = network_data.split("|")
        self.target_id = int(target_id_and_rest[0])

        avalibality_str =target_id_and_rest[1]

        avalibality_str_parts = avalibality_str.split(";");



        for part in avalibality_str_parts:
            if(part):
                avalibality_value = part.split(":")[0]
                node_ids_str = part.split(":")[1]
                if(node_ids_str):
                    node_ids = get_node_ids_from_str(node_ids_str)

                    if(avalibality_value == "1"):
                        self.available_node_ids = node_ids
                    elif(avalibality_value == "0"):
                        self.not_available_node_ids = node_ids