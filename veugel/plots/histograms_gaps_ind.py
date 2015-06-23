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
    a = {to_vijfvoud(day.day): day.get_gap_lengths() for day in veugel.days}
    print(a)
    return a

def get_hist_data(veugel):
    """

    :rtype : object
    :type veugel: Veugel
    :param min: int
    :param max: int
    """
    foodict = foo(veugel)

    print(veugel.name)

    for n in [50, 60, 70, 90, 120]:
        yield foodict[n]

if __name__ == '__main__':
    for veugel_number in list(relational.BROTHERS):
        brother_number = relational.BROTHERS[veugel_number]

        # Create a figure instance
        fig, axes = pyplot.subplots(nrows=5, ncols=2, figsize=(10, 14))
        ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9 = axes.flat
        n_bins = 20

        try:
            veugel  = Veugel.from_folder(VEUGEL_DIR.format(label="ISO",  num=veugel_number))
            brother = Veugel.from_folder(VEUGEL_DIR.format(label="SELF", num=brother_number))
        except:
            continue

        data_50, data_60, data_70, data_90, data_120 = get_hist_data(veugel)

        ax0.hist(data_50, n_bins, histtype='step', fill=True)
        ax0.set_title('{veugel.name} gap length at 50DPH'.format(**locals()))

        ax2.hist(data_60, n_bins, histtype='step', fill=True)
        ax2.set_title('{veugel.name} gap length at 60DPH'.format(**locals()))

        ax4.hist(data_70, n_bins, histtype='step', fill=True)
        ax4.set_title('{veugel.name} gap length at 70DPH'.format(**locals()))

        ax6.hist(data_90, n_bins, histtype='step', fill=True)
        ax6.set_title('{veugel.name} gap length at 90DPH'.format(**locals()))

        ax8.hist(data_120, n_bins, histtype='step', fill=True)
        ax8.set_title('{veugel.name} gap length at 120DPH'.format(**locals()))

        data_50, data_60, data_70, data_90, data_120 = get_hist_data(brother)


        ax1.hist(data_50, n_bins, histtype='step', fill=True)
        ax1.set_title('{brother.name} gap length at 50DPH'.format(**locals()))

        ax3.hist(data_60, n_bins, histtype='step', fill=True)
        ax3.set_title('{brother.name} gap length at 60DPH'.format(**locals()))

        ax5.hist(data_70, n_bins, histtype='step', fill=True)
        ax5.set_title('{brother.name} gap length at 70DPH'.format(**locals()))

        ax7.hist(data_90, n_bins, histtype='step', fill=True)
        ax7.set_title('{brother.name} gap length at 90DPH'.format(**locals()))

        ax9.hist(data_120, n_bins, histtype='step', fill=True)
        ax9.set_title('{brother.name} gap length at 120DPH'.format(**locals()))


        fig.suptitle("{veugel.name} / {brother.name}".format(**locals()))
        fig.savefig("gap_hist_{veugel.name}_{brother.name}.png".format(**locals()))