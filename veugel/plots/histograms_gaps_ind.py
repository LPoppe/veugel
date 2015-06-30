from itertools import count
from matplotlib import pyplot
from veugel import relational
from veugel.analyse import analyse

BUCKETS = [50, 60, 70, 90, 120]
N_BINS = 20


def to_quintuple(day):
    for bucket in count(0, 5):
        if bucket - 2.5 < day <= bucket + 2.5:
            return bucket

def get_quintuple_map(veugel):
    return {to_quintuple(day.daynr): list(day.get_gap_lengths()) for day in veugel.days}

def get_hist_data(veugel):
    quintuple_map = get_quintuple_map(veugel)

    for n in BUCKETS:
        yield quintuple_map[n]

def aggregate(iso, self):
    return iso.name, list(get_hist_data(iso)), self.name, list(get_hist_data(self))

def plot(bins):
    for iso_name, iso_bins, self_name, self_bins in bins:
        fig, axes = pyplot.subplots(nrows=len(BUCKETS), ncols=2, figsize=(10, 14))

        for bucketnr, axn in enumerate(range(0, len(axes.flat), 2)):
            axes.flat[axn].hist(iso_bins[bucketnr], N_BINS, histtype='step', fill=True)
            axes.flat[axn].set_title('{} gap length at {}DPH'.format(iso_name, BUCKETS[bucketnr]))

        for bucketnr, axn in enumerate(range(1, len(axes.flat), 2)):
            axes.flat[axn].hist(self_bins[bucketnr], N_BINS, histtype='step', fill=True)
            axes.flat[axn].set_title('{} gap length at {}DPH'.format(self_name, BUCKETS[bucketnr]))

        fig.suptitle("{iso_name} / {self_name}".format(**locals()))
        fig.savefig("gap_hist_{iso_name}_{self_name}.png".format(**locals()))

if __name__ == '__main__':
    analyse(relational.BROTHERS.items(), plot, aggregate)
