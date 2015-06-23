import sys

from collections import OrderedDict
from matplotlib import pyplot

from veugel import relational
from veugel.veugel import Veugel

__author__ = 'Linda Poppe'

VEUGEL_DIR = "/home/linda/Sounddata/{label}/{num}/"

def foo(veugel):
    for day in veugel.days:
        for dp in day.datapoints:
            yield (day.day, dp.duration_of_state)


def plot_violin_das(fig, veugel, color='red'):
    """
    :type veugel: Veugel
    :param min: int
    :param max: int
    """
    days, means = zip(*foo(veugel))
    fig.violinplot(x=list(days), y=list(means), color=color)


if __name__ == '__main__':
    for veugel_number in list(relational.BROTHERS):
        #pyplot.figure()
        # Create a figure instance
        fig = pyplot.figure()

        # Create an axes instance
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        ax1.set_ylabel('DAS')
        ax1.set_xlabel('DPH')
        ax2.set_ylabel('DAS')
        ax1.set_xlabel('DPH')
        brother_number = relational.BROTHERS[veugel_number]

        print(brother_number)

        try:
            veugel  = Veugel.from_folder(VEUGEL_DIR.format(label="ISO",  num=veugel_number))
            brother = Veugel.from_folder(VEUGEL_DIR.format(label="SELF", num=brother_number))
        except:
            continue

        plot_violin_das(ax1, veugel, color='red')
        plot_violin_das(ax2, brother, color='blue')

        fig.suptitle("{veugel.name} / {brother.name}".format(**locals()))
        fig.savefig("dasviolin_{veugel.name}_{brother.name}.png".format(**locals()),bbox_inches='tight')
