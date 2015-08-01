from collections import defaultdict, Counter, OrderedDict

__author__ = 'linda'

from scipy import stats
from veugel import relational
from veugel.analyse import analyse

BUCKETS = [50, 60, 70, 90, 120]
MAX_DAYS = 1000
N_BINS = 20


def choose_day(days, daynr, tries=3):
    days = {day.daynr: day for day in days}
    for day_delta in range(0, tries):
        if daynr + day_delta in days:
            return days[daynr + day_delta]
        elif daynr - day_delta in days:
            return days[daynr - day_delta]
    raise ValueError("No key day found between (%s, %s)" % (daynr - tries, daynr + tries))


def get_hist_data(veugel):
    days = [choose_day(veugel.days, daynr) for daynr in BUCKETS]
    days = [day.rows["duration_of_state"] for day in days]
    days = [Counter(das_values) for das_values in days]
    days = [OrderedDict(sorted(counted.items())) for counted in days]
    return days


def get_ks(iso, self):
    for daynr in BUCKETS:
        #print(sorted(Counter(choose_day(iso.days, daynr).rows["duration_of_state"]).items()))
        #print(sorted(Counter(choose_day(self.days, daynr).rows["duration_of_state"]).items()))
        iso_das = choose_day(iso.days, daynr).rows["duration_of_state"]
        self_das = choose_day(self.days, daynr).rows["duration_of_state"]
        yield stats.ks_2samp(iso_das, self_das)


def _aggregate(iso, self):
    yield iso.name
    yield self.name

    yield get_hist_data(iso)
    yield get_hist_data(self)

    yield list(get_ks(iso, self))


def aggregate(iso, self):
    return list(_aggregate(iso, self))


def plot(iso_name, self_name, iso_hist, self_hist, ks):

    print("{} <-> {}".format(iso_name, self_name))
    for day, res in zip(BUCKETS, ks):
        print("{}: {}".format(day, res))


if __name__ == '__main__':
    analyse(list(relational.BROTHERS.items())[:1], plot, aggregate, plot_threaded=True)
