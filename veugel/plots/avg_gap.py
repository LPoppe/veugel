import sys

from collections import OrderedDict
from matplotlib import pyplot
import statistics

from veugel import relational
from veugel.veugel import Veugel

__author__ = 'Linda Poppe'


VEUGEL_DIR = "/home/linda/Sounddata/{label}/{num}/"


def plot_avg_gap(veugel):
    """
    :type veugel: Veugel
    :param min: int
    :param max: int
    """
    print(veugel.name)

    means = OrderedDict((d.day, statistics.mean(d.get_gap_lengths())) for d in veugel.days)
    pyplot.plot(list(means.keys()), list(means.values()), marker='x')
    pyplot.ylabel('Mean gap length (ms)')
    pyplot.xlabel('DPH')
    pyplot.ylim(0,100)
    pyplot.legend(["ISO "+str(veugel_number), "SELF "+str(brother_number)], loc=0)


if __name__ == '__main__':
    for veugel_number in relational.BROTHERS:
        pyplot.figure()
        pyplot.gca().set_color_cycle(['red', 'blue'])
        brother_number = relational.BROTHERS[veugel_number]

        try:
            veugel  = Veugel.from_folder(VEUGEL_DIR.format(label="ISO",  num=veugel_number))
        except ValueError:
            print("ISO/{veugel_number} does not exist".format(**locals()))
            continue

        try:
            brother = Veugel.from_folder(VEUGEL_DIR.format(label="SELF", num=brother_number))
        except ValueError:
            print("SELF/{brother_number} does not exist".format(**locals()))
            continue



        plot_avg_gap(veugel)
        plot_avg_gap(brother)

        pyplot.savefig("GAP_{veugel.name}_{brother.name}.png".format(**locals()), bbox_inches='tight')