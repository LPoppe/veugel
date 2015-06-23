import sys

from collections import OrderedDict
from matplotlib import pyplot

from veugel import relational
from veugel.veugel import Veugel

__author__ = 'Linda Poppe'


VEUGEL_DIR = "/home/linda/Sounddata/{label}/{num}/"


def plot_avg_das(veugel):
    """
    :type veugel: Veugel
    :param min: int
    :param max: int
    """
    print(veugel.name)
    #means_and_errors = ((d.day, d.get_das_mean(), d.get_das_error()) for d in veugel.days)
    #days, means, errors = zip(*means_and_errors)
    #pyplot.errorbar(x=list(days), y=list(means), yerr=errors, fmt='x')

    means = OrderedDict((d.day, d.get_das_mean()) for d in veugel.days)
    pyplot.plot(list(means.keys()), list(means.values()), marker='x')
    pyplot.ylabel('Mean DAS')
    pyplot.xlabel('DPH')
    pyplot.ylim(0,150)
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



        plot_avg_das(veugel)
        plot_avg_das(brother)

        pyplot.savefig("das_{veugel.name}_{brother.name}.png".format(**locals()), bbox_inches='tight')

