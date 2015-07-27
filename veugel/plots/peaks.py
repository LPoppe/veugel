from collections import defaultdict, OrderedDict
import functools
from itertools import count
from matplotlib import pyplot
from veugel import peakdetect
from veugel.analyse import analyse
from veugel.relational import BROTHERS

@functools.lru_cache()
def to_bucket(value, bucket_size):
    if value < 0:
        raise ValueError("Given value less than zero.")

    for bucket in count(0, bucket_size):
        if bucket <= value < bucket + bucket_size:
            return bucket

def to_buckets(values, bucket_size=3):
    filled_buckets = defaultdict(int)
    for value in values:
        bucket = to_bucket(value, bucket_size)
        filled_buckets[bucket] += 1
    # Convert our normal dictionary to a dictionary ordered by the bucket
    return OrderedDict(sorted(filled_buckets.items()))

def detect_peaks(values, minimum_peak_size=50):
    UP, DOWN = 1, 2
    direction = UP

    previous_value = previous_valley = min(values) - 1
    for i, value in enumerate(values):
        if direction == UP:
            if value < previous_value:
                if abs(previous_value - previous_valley) >= minimum_peak_size:
                    yield i-1, previous_value
                direction = DOWN
        else:
            if value > previous_value:
                previous_valley = previous_value
                direction = UP
        previous_value = value


def aggregate(veugel):
    das_values = veugel.days[0].rows["duration_of_state"]

    buckets = to_buckets(das_values)
    bucket_keys, bucket_values = zip(*buckets.items())

    # Peaks are represented as a list of tuples, with the first element giving
    # the INDEX of the bucket value. So we should convert it to 'real' bucket values
    peaks = list(detect_peaks(bucket_values, minimum_peak_size=50))
    peaks = [(bucket_keys[x_peak], y_peak) for x_peak, y_peak in peaks]
    peaks = OrderedDict(peaks)

    # Return an ordered dict of buckets, and their peaks
    return buckets, peaks

def plot(das_values, peaks):
    pyplot.figure()

    keys = list(das_values.keys())

    pyplot.plot(keys, [das_values[x] for x in keys])
    pyplot.plot(list(peaks.keys()), list(peaks.values()), 'x')

    pyplot.show()

if __name__ == "__main__":
    analyse([next(iter(BROTHERS.keys()))], aggregator=aggregate, plotter=plot, plot_threaded=True)