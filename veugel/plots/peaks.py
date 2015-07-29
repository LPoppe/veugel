from collections import defaultdict, OrderedDict
import functools
from itertools import count, chain
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

def to_buckets(values, bucket_size):
    filled_buckets = defaultdict(int)
    for value in values:
        bucket = to_bucket(value, bucket_size)
        filled_buckets[bucket] += 1
    # Convert our normal dictionary to a dictionary ordered by the bucket
    return OrderedDict(sorted(filled_buckets.items()))

def detect_peaks(values, minimum_peak_size):
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

def day_aggregate(das_values):
    """
    Gegeven een reeks getallen, bepaal:

      1. De buckets (dat wil zeggen, aggregeer punten die dicht bij elkaar liggen en tel hoe vaak ze voorkomen)
      2. De pieken van die buckets
    """
    buckets = to_buckets(das_values, bucket_size=3)
    bucket_keys, bucket_values = zip(*buckets.items())

    # Peaks are represented as a list of tuples, with the first element giving
    # the INDEX of the bucket value. So we should convert it to 'real' bucket values
    peaks = list(detect_peaks(bucket_values, minimum_peak_size=50))
    peaks = [(bucket_keys[x_peak], y_peak) for x_peak, y_peak in peaks]
    peaks = OrderedDict(peaks)

    # peaks: een dictionary van bucket (int) -> count (int)
    # buckets: een dictionary van bucket (int) -> count(int)

    # Return an ordered dict of buckets, and their peaks
    return buckets, peaks


def aggregate(veugel):
    # @LINDA: Kies je dagen die je wil berekenen in de onderstaande constructie!
    days = veugel.days # FILTER DUS HIER

    aggregated = [(day.daynr, day_aggregate(day.rows["duration_of_state"])) for day in days]
    aggregated = OrderedDict(aggregated)

    # HACK: als we hier een enkel item teruggeven gaat analyse() over de zeik :<. We geven
    # dus een lijst met een enkel item terug, wat vervolgens weer goed gaat in plot().
    return [aggregated]

def plot(aggregated):
    pyplot.figure()

    for day, (buckets, peaks) in aggregated.items():
        print(day)
        pyplot.plot(list(buckets.keys()), list(buckets.values()))
        pyplot.plot(list(peaks.keys()), list(peaks.values()), 'x')

    pyplot.show()

if __name__ == "__main__":
    analyse([list(BROTHERS.keys())[0]], aggregator=aggregate, plotter=plot, plot_threaded=True)