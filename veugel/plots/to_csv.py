import csv
import os
import sys

from collections import OrderedDict
from itertools import chain

from veugel import relational
from veugel.analyse import analyse
from veugel.cache import HOME_DIR

DAS = "duration_of_state"
GAP = "gap_length"
CTIME = "continuity_time"

CSV_DIR = os.path.join(HOME_DIR, "csv")

if not os.path.exists(CSV_DIR):
    os.mkdir(CSV_DIR)


def get_datapoint_type():
    if len(sys.argv) == 1:
        raise ValueError("You must pass a property to export as an argument to this script")

    if sys.argv[1] not in (DAS, GAP, CTIME):
        raise ValueError("Choose one of: {}, {}, {}".format(DAS, GAP, CTIME))

    return sys.argv[1]

def aggregate_das(veugel):
    return veugel.name, OrderedDict((day.daynr, day.rows[DAS]) for day in veugel.days)

def aggregate_gap(veugel):
    return veugel.name, OrderedDict((day.daynr, day.get_gap_lengths()) for day in veugel.days)

def aggregate_ctime(veugel):
    return veugel.name, OrderedDict((day.daynr, day.rows[CTIME]) for day in veugel.days)

def get_datapoint(points, daynr, rownr):
    if len(points[daynr]) <= rownr:
        return ""
    return points[daynr][rownr]


def plot(name, data):
    filename = os.path.join(CSV_DIR, "{name}_{type}.csv".format(name=name, type=get_datapoint_type()))

    headers = list(data.keys())
    amount_of_rows = max(map(len, data.values()))

    rows = [None] * amount_of_rows
    for rownr in range(amount_of_rows):
        rows[rownr] = {daynr: get_datapoint(data, daynr, rownr) for daynr in headers}

    csvfp = csv.DictWriter(open(filename, "w"), fieldnames=headers)
    csvfp.writeheader()
    csvfp.writerows(rows)



if __name__ == '__main__':
    type = get_datapoint_type()

    if type == DAS:
        aggregator = aggregate_das
    elif type == GAP:
        aggregator = aggregate_gap
    elif type == CTIME:
        aggregator = aggregate_ctime
    else:
        assert False, "Not possible :)"

    analyse(chain(*relational.BROTHERS.items()), aggregator=aggregator, plotter=plot, plot_threaded=True)