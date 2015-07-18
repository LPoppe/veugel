import csv
import os
import itertools
import numpy

from veugel import relational
from veugel.analyse import analyse
from veugel.plots.to_csv import CSV_DIR


def bootstrap_day(data):
    sample = numpy.random.choice(data, size=len(data), replace=True)
    median = numpy.median(sample)
    stderr = numpy.std(sample)
    return median, stderr

def bootstrap_veugel(veugel):
    for day in veugel.days:
        das_values = day.rows["duration_of_state"]
        yield (day.daynr, bootstrap_day(das_values))

def aggregate(iso, self):
    return [
        (iso.name, dict(bootstrap_veugel(iso))),
        (self.name, dict(bootstrap_veugel(self)))
    ]

def get_row(bootstrapped, days):
    for day in days:
        try:
            median, stderr = bootstrapped[day]
        except KeyError:
            # This bird didn't have this day
            yield ""
        else:
            yield "{median}±{stderr}".format(**locals())

def plot(*veugel_tuples):
    all_veugels = list(itertools.chain(*veugel_tuples))

    # Determine all available days
    all_days = set()
    for (name, bootstrapped) in all_veugels:
        for daynr in bootstrapped.keys():
            all_days.add(daynr)
    all_days = list(sorted(all_days))

    # Open CSV file
    filename = os.path.join(CSV_DIR, "bootstrapped.csv")
    file = open(filename, "w")

    csvfp = csv.writer(file)
    csvfp.writerow(["name"] + all_days)

    for name, bootstrapped in all_veugels:
        csvfp.writerow([name] + list(get_row(bootstrapped, all_days)))


if __name__ == '__main__':
    analyse(relational.BROTHERS.items(), aggregator=aggregate, plotter=plot, plot_threaded=False)