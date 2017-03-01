import sys
import os
from datetime import datetime
import time
from itertools import zip_longest


def get_task_ls(inp_file, keys=['event_name', 'time_to_expire', 'priority']):
    '''
    return a list of dict according to provided keys
   '''
    output_ls = []
    with open(inp_file, "r") as f:
        for line in f:
            ls = line.split(',')
            ls = list(map(lambda x: x.strip(), ls))
            n = len(ls)
            if (n < 2 or n > 3):
                raise TypeError("input file not well formatted")
            temp_dict = dict(zip_longest(keys, ls, fillvalue=sys.maxsize))
            temp_dict['time_to_expire'] = datetime.strptime(
                temp_dict.get('time_to_expire'), "%Y/%m/%d %H:%M")
            temp_dict['priority'] = int(temp_dict.get('priority'))
            output_ls.append(temp_dict)
    return output_ls


if __name__ == "__main__":
    try:
        inp_file, start_time = sys.argv[1], sys.argv[2]
    except IndexError:
        print("Usage : python <prog_name> <inp_file> <start_time>")
        sys.exit()

    inp_file = os.path.abspath(inp_file)
    task_ls = get_task_ls(inp_file)
    start_time = datetime.strptime(start_time.strip(), "%Y/%m/%d %H:%M")

    task_ls.sort(key=lambda x: (x.get('time_to_expire'), x.get('priority')))
    if task_ls:
        if (start_time > task_ls[0]['time_to_expire']):
            raise TypeError("start_time invalid")

    sleep_sec_ls = []
    prev = start_time
    for cur in task_ls:
        sleep_sec_ls.append(cur['time_to_expire'] - prev)
        prev = cur['time_to_expire']

    for each, dtime in zip(task_ls, sleep_sec_ls):
        # print(dtime.seconds, "---------------------")
        time.sleep(dtime.seconds)
        print(
            "Current time[ {time_to_expire} ] , Event '{event_name}' Processed ".
            format(**each))
