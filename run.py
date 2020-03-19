from file_reader import get_metric_logs_from_file
from helpers import get_max_node_id

from energy_analyzer import analyzer_energy_consuption
from delay_analyzer import analyze_delay
import numpy as np
from datetime import timedelta

def calculate_metrics(node_count,count):
    line_file_name = "./"+ str(node_count) +"/line/"+str(count)+".txt"
    star_file_name = "./" + str(node_count) + "/star/" + str(count) + ".txt"
    circular_file_name = "./" + str(node_count) + "/circular/" + str(count) + ".txt"

    return [calculate_with_file_name(line_file_name),calculate_with_file_name(star_file_name),calculate_with_file_name(circular_file_name)]

def calculate_with_file_name(file_name):
    print(file_name)
    metric_logs = get_metric_logs_from_file(file_name)


    energy = analyzer_energy_consuption(metric_logs)
    delay =analyze_delay(metric_logs)

    energy.update(delay)

    received_metric_logs = filter(lambda x: x.log_type == "RECEIVED",metric_logs)
    # print(file_name,len(list(received_metric_logs)))

    total_message_length = 0

    for received_metric_log in received_metric_logs:
        total_message_length += len(received_metric_log.network_data)

    energy["total_message_length"] = total_message_length

    return energy

def get_whisker_stats(arr):
    data = np.array(arr)
    median = np.median(data)
    sum = np.sum(data)
    mean = np.mean(data)
    upper_quartile = np.percentile(data, 75)
    lower_quartile = np.percentile(data, 25)

    iqr = upper_quartile - lower_quartile
    upper_whisker = data[data <= upper_quartile + 1.5 * iqr].max()
    lower_whisker = data[data >= lower_quartile - 1.5 * iqr].min()

    return {"sum":sum,"mean":mean ,"median":median,"upper_quartile":upper_quartile,"lower_quartile":lower_quartile,"upper_whisker":upper_whisker,"lower_whisker":lower_whisker}


def calculate_throughput_goodput():
    arr5a = [74719,80733,83237,79742,79144,78585,79658,77333,86261]

    arr5b = [40592,46440,50306,46666,47681,45842,46521,45075,50605]

    arr10a = [221312,219131,228760,211844,209076,230053,247259,215565,215361,232979]
    arr10b = [148669,144689,153352,140939,136572,146812,171771,144180,141297,161529]

    arr15a = [396709,419850,382952,408269,416493,388916,404553,418091,433213,407216]
    arr15b = [280725,298039,268932,292156,294664,274332,286841,301176,306261,281870]

    arr20a = [599711,626579,646581,622256,651377,608872,644296,664918,646292,642963]
    arr20b = [433687,463285,478035,456873,651377,442863,476518,486690,474172,470020]

    print("throughput")
    print(get_whisker_stats(arr5a))
    print(get_whisker_stats(arr10a))
    print(get_whisker_stats(arr15a))
    print(get_whisker_stats(arr20a))

    print("goodput")
    print(get_whisker_stats(arr5b))
    print(get_whisker_stats(arr10b))
    print(get_whisker_stats(arr15b))
    print(get_whisker_stats(arr20b))


def other():
    node_counts = [5,10,15,20l]

    line_whisker_stats = []
    star_whisker_stats = [
    ]
    circular_whisker_stats = [
    ]
    for node_count in node_counts:
        line_stats = {
            "total_energy_consumption":[],
            "total_energy_consumption2":[],
            "bandthwidth":[],
            "request_count":[],
            "average_delay":[],
            "total_message_length":[]
        }
        star_stats = {
            "total_energy_consumption":[],
            "total_energy_consumption2": [],
            "bandthwidth":[],
            "request_count":[],
            "average_delay":[],
            "total_message_length":[]
        }
        circular_stats = {
            "total_energy_consumption": [],
            "total_energy_consumption2": [],
            "bandthwidth": [],
            "request_count": [],
            "average_delay": [],
            "total_message_length": []
        }
        for i in range(0,10):
            results =calculate_metrics(node_count,i)

            line = results[0]
            star = results[1]
            circular = results[2]

            line_stats["total_energy_consumption"].append(line["total_energy_consumption"])
            line_stats["total_energy_consumption2"].append(line["total_energy_consumption2"])
            line_stats["bandthwidth"].append(line["bandthwidth"])
            line_stats["request_count"].append(line["request_count"])
            line_stats["average_delay"].append(line["average_delay"])
            line_stats["total_message_length"].append(line["total_message_length"])

            star_stats["total_energy_consumption"].append(star["total_energy_consumption"])
            star_stats["total_energy_consumption2"].append(star["total_energy_consumption2"])
            star_stats["bandthwidth"].append(star["bandthwidth"])
            star_stats["request_count"].append(star["request_count"])
            star_stats["average_delay"].append(star["average_delay"])
            star_stats["total_message_length"].append(star["total_message_length"])

            circular_stats["total_energy_consumption"].append(circular["total_energy_consumption"])
            circular_stats["total_energy_consumption2"].append(circular["total_energy_consumption2"])
            circular_stats["bandthwidth"].append(circular["bandthwidth"])
            circular_stats["request_count"].append(circular["request_count"])
            circular_stats["average_delay"].append(circular["average_delay"])
            circular_stats["total_message_length"].append(circular["total_message_length"])

        line_whisker_stats.append(line_stats)
        star_whisker_stats.append(star_stats)
        circular_whisker_stats.append(circular_stats)

    if(len(line_whisker_stats)>0):
        line_whisker_stats[0]["throughput"] = [140826, 140323, 144237, 139231, 143254, 142711, 139081, 140651, 138625, 140940]
        star_whisker_stats[0]["throughput"] = [97250,97119,106839,100815,104829,106951,96878,101765,102215,162917]
        circular_whisker_stats[0]["throughput"] = [157055,155171,159452,158019,159908,156982,157026,155387,162917]

    if(len(line_whisker_stats)>1):
        line_whisker_stats[1]["throughput"] = [426525, 430308, 423649, 422030, 421334, 430656, 420620, 430007, 429523, 429523]
        star_whisker_stats[1]["throughput"] = [248597,251060,249428,248162,250256,248597,222041,250940,234401,250404]
        circular_whisker_stats[1]["throughput"] = [426525,427398,423649,432030,421634,430646,420620,430507,429523,429523]

    if (len(line_whisker_stats) > 2):
        line_whisker_stats[2]["throughput"] = [723837, 723837, 712684, 725877, 726465, 723195, 729648, 719193, 729302, 716625]
        star_whisker_stats[2]["throughput"] = [408756,384005,409069,407963,367353,357145,396580,371334,392828,703371]
        circular_whisker_stats[2]["throughput"] = [649984,645378,641073,653835,634277,636091,649361,649977,641115,641173]

    if (len(line_whisker_stats) > 3):
        line_whisker_stats[3]["throughput"] = [1015864, 1037792, 1040785, 1024875, 1045608, 1040309, 1031774, 1026828, 1046306, 1017030]
        star_whisker_stats[3]["throughput"] = [520079,564303,503501,486246,526848,509357,528630,523737,517948,517132]
        circular_whisker_stats[3]["throughput"] = [1040511,1041791,1056873,1029268,1041894,1045257,1025054,1030052,1040732,1041501]



    print("total_energy_consumption")
    for i in range(len(line_whisker_stats)):
        print(get_whisker_stats(line_whisker_stats[i]["total_energy_consumption"]))
        print(get_whisker_stats(star_whisker_stats[i]["total_energy_consumption"]))
        print(get_whisker_stats(circular_whisker_stats[i]["total_energy_consumption"]))
        print("**********************")
    print("total_energy_consumption2")
    for i in range(len(line_whisker_stats)):
        print(get_whisker_stats(line_whisker_stats[i]["total_energy_consumption2"]))
        print(get_whisker_stats(star_whisker_stats[i]["total_energy_consumption2"]))
        print(get_whisker_stats(circular_whisker_stats[i]["total_energy_consumption2"]))
        print("**********************")
    print("bandthwidth")
    for i in range(len(line_whisker_stats)):
        print(get_whisker_stats(line_whisker_stats[i]["bandthwidth"]))
        print(get_whisker_stats(star_whisker_stats[i]["bandthwidth"]))
        print(get_whisker_stats(circular_whisker_stats[i]["bandthwidth"]))
        print("**********************")
    print("request_count")
    for i in range(len(line_whisker_stats)):
        print(get_whisker_stats(line_whisker_stats[i]["request_count"]))
        print(get_whisker_stats(star_whisker_stats[i]["request_count"]))
        print(get_whisker_stats(circular_whisker_stats[i]["request_count"]))
        print("**********************")

    print("average_delay")
    for i in range(len(line_whisker_stats)):
        print(get_whisker_stats(line_whisker_stats[i]["average_delay"]))
        print(get_whisker_stats(star_whisker_stats[i]["average_delay"]))
        print(get_whisker_stats(circular_whisker_stats[i]["average_delay"]))
        print("**********************")

    print("total_message_length")
    for i in range(len(line_whisker_stats)):
        print(get_whisker_stats(line_whisker_stats[i]["total_message_length"]))
        print(get_whisker_stats(star_whisker_stats[i]["total_message_length"]))
        print(get_whisker_stats(circular_whisker_stats[i]["total_message_length"]))
        print("**********************")

    print("throughput")
    for i in range(len(line_whisker_stats)):
        print(get_whisker_stats(line_whisker_stats[i]["throughput"]))
        print(get_whisker_stats(star_whisker_stats[i]["throughput"]))
        print(get_whisker_stats(circular_whisker_stats[i]["throughput"]))
        print("**********************")

        


if __name__ == "__main__":
    other()
