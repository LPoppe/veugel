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
    means = OrderedDict((d.day, d.get_das_mean()) for d in veugel.days)
    pyplot.plot(list(means.keys()), list(means.values()), marker='x')


if __name__ == '__main__':
    for veugel_number in relational.BROTHERS:
        pyplot.figure()

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

        pyplot.savefig("{veugel.name}_{brother.name}.png".format(**locals()), bbox_inches='tight')

