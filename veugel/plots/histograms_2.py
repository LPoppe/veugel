from itertools import count
from matplotlib import pyplot
from collections import defaultdict
from veugel import relational
from veugel.veugel import Veugel


__author__ = 'Linda Poppe'

VEUGEL_DIR = "/home/linda/Sounddata/{label}/{num}/"

def to_vijfvoud(day):
    for bucket in count(0, 5):
        if bucket - 2.5 < day <= bucket + 2.5:
            return bucket

def foo(veugel):
    return {to_vijfvoud(day.day): [dp.duration_of_state for dp in day.datapoints] for day in veugel.days}

def merge_foos(foos):
    uberfoo = defaultdict(list)

    for foo in foos:
        for bucket, dasses in foo.items():
            for das in dasses:
                uberfoo[bucket].append(das)

    return uberfoo

def get_hist_data(veugels):
    """

    :rtype : object
    :type veugel: Veugel
    :param min: int
    :param max: int
    """
    uberfoo = merge_foos(map(foo, veugels))

    for n in [50, 60, 70, 90, 120]:
        yield uberfoo[n]

def to_veugel(veugel_number, label):
    return Veugel.from_folder(VEUGEL_DIR.format(label=label,  num=veugel_number))


if __name__ == '__main__':
    veugels, brothers = zip(*relational.BROTHERS.items())

    # Create a figure instance
    fig, axes = pyplot.subplots(nrows=5, ncols=2, figsize=(10, 14))
    ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9 = axes.flat
    n_bins = 30

    veugels = [to_veugel(veugelnr, label="ISO") for veugelnr in veugels]
    brothers = [to_veugel(veugelnr, label="SELF") for veugelnr in brothers]

    data_50, data_60, data_70, data_90, data_120 = get_hist_data(veugels)

    ax0.hist(data_50, n_bins, histtype='step', fill=True)
    ax0.set_title('ISO, DAS at 50DPH'.format(**locals()))

    ax2.hist(data_60, n_bins, histtype='step', fill=True)
    ax2.set_title('ISO, DAS at 60DPH'.format(**locals()))

    ax4.hist(data_70, n_bins, histtype='step', fill=True)
    ax4.set_title('ISO, DAS at 70DPH'.format(**locals()))

    ax6.hist(data_90, n_bins, histtype='step', fill=True)
    ax6.set_title('ISO, DAS at 90DPH'.format(**locals()))

    ax8.hist(data_120, n_bins, histtype='step', fill=True)
    ax8.set_title('ISO, DAS at 120DPH'.format(**locals()))

    data_50, data_60, data_70, data_90, data_120 = get_hist_data(brothers)


    ax1.hist(data_50, n_bins, histtype='step', fill=True)
    ax1.set_title('SELF, DAS at 50DPH'.format(**locals()))

    ax3.hist(data_60, n_bins, histtype='step', fill=True)
    ax3.set_title('SELF, DAS at 60DPH'.format(**locals()))

    ax5.hist(data_70, n_bins, histtype='step', fill=True)
    ax5.set_title('SELF, DAS at 70DPH'.format(**locals()))

    ax7.hist(data_90, n_bins, histtype='step', fill=True)
    ax7.set_title('SELF, DAS at 90DPH'.format(**locals()))

    ax9.hist(data_120, n_bins, histtype='step', fill=True)
    ax9.set_title('SELF, DAS at 120DPH'.format(**locals()))

    fig.savefig("DAS_hist_per_day.png".format(**locals()))