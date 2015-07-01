from collections import OrderedDict
from matplotlib import pyplot

from veugel import relational
from veugel.analyse import analyse

def plot_avg_das(means):
    pyplot.plot(list(means.keys()), list(means.values()), marker='x')

def plot(iso_name, iso_avgs, self_name, self_avgs):
    pyplot.figure()
    pyplot.gca().set_color_cycle(['red', 'blue'])

    plot_avg_das(iso_avgs)
    plot_avg_das(self_avgs)

    pyplot.ylabel('Mean DAS')
    pyplot.xlabel('DPH')
    pyplot.ylim(0, 150)
    pyplot.legend([iso_name, self_name], loc=0)

    pyplot.savefig("das_{iso_name}_{self_name}.png".format(**locals()), bbox_inches='tight')

def get_das_mapping(veugel):
    return OrderedDict((day.daynr, day.get_das_mean()) for day in veugel.days)

def aggregate(iso, self):
    return [iso.name, get_das_mapping(iso), self.name, get_das_mapping(self)]

if __name__ == '__main__':
    analyse(relational.BROTHERS.items(), plot, aggregate, plot_threaded=True)

