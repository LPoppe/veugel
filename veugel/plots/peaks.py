from matplotlib import pyplot
from veugel.analyse import analyse
from veugel.peakdetect import _smooth
from veugel.relational import BROTHERS

def aggregate(veugel):
    return veugel.days[0].rows["duration_of_state"], [3]

def plot(das_values, peaks):
    pyplot.figure()
    pyplot.plot(_smooth(das_values, window_len=100))
    pyplot.plot(_smooth(das_values, window_len=10))
    pyplot.show()

if __name__ == "__main__":
    analyse([next(iter(BROTHERS.keys()))], aggregator=aggregate, plotter=plot, plot_threaded=True)