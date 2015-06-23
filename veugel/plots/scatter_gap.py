import sys

from collections import OrderedDict
from matplotlib import pyplot

from veugel import relational
from veugel.veugel import Veugel

__author__ = 'Linda Poppe'

VEUGEL_DIR = "/home/linda/Sounddata/{label}/{num}/"

def foo(veugel):
    for day in veugel.days:
        for gap_length in day.get_gap_lengths():
            yield (day.day, gap_length)


def plot_scatter_gap(fig, veugel, color='red'):
    """
    :type veugel: Veugel
    :param min: int
    :param max: int
    """
    days, means = zip(*list(foo(veugel)))

    fig.scatter(x=list(days), y= list(means), color=color)

if __name__ == '__main__':
    for veugel_number in list(relational.BROTHERS):
        #pyplot.figure()1
        # Create a figure instance
        fig = pyplot.figure()
        pyplot.ylabel('Gap length')
        pyplot.xlabel('DPH')
        pyplot.ylim(0,250)
        # Create an axes instance
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        brother_number = relational.BROTHERS[veugel_number]

        print(brother_number)

        try:
            veugel  = Veugel.from_folder(VEUGEL_DIR.format(label="ISO",  num=veugel_number))
            brother = Veugel.from_folder(VEUGEL_DIR.format(label="SELF", num=brother_number))
        except:
            continue

        plot_scatter_gap(ax1, veugel, color='red')
        plot_scatter_gap(ax2, brother, color='blue')

        fig.suptitle("{veugel.name} / {brother.name}".format(**locals()))
        fig.savefig("gapscatter_{veugel.name}_{brother.name}.png".format(**locals()), bbox_inches='tight')
