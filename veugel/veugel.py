import logging
from operator import attrgetter
import statistics
import numpy

from veugel import cache
from veugel import relational

log = logging.getLogger(__name__)

class Day(object):
    """
    Represents a day worth of data. I.e., the merged sheets of an ODS file.
    """
    def __init__(self, daynr, rows):
        """
        :type daynr: int
        :type rows: numpy.ndarray
        """
        self.daynr = daynr
        self.rows = rows

    def get_das_median(self):
        return self.rows["duration_of_state"].median()

    def get_das_mean(self):
        return self.rows["duration_of_state"].mean()

    def get_gap_length_mean(self):
        return statistics.mean(self.get_gap_lengths())

    def get_gap_length_median(self):
        return statistics.median(self.get_gap_lengths())

    def get_gap_lengths(self):
        gap_length = 0
        for ct in self.rows["continuity_time"]:
            if -0.01 < ct < 0.01:
                gap_length += 1
            elif gap_length:
                yield gap_length
                gap_length = 0

    @classmethod
    def from_numpy_file(cls, daynr, path):
        return Day(daynr, numpy.load(open(path, "rb")))


class Veugel(object):
    def __init__(self, id, days):
        self.id = id
        self.days = sorted(days, key=attrgetter("daynr"))
        self._days = {d.daynr: d for d in days}

    @property
    def name(self):
        category = "ISO" if id in relational.BROTHERS else "SELF"
        return "{}{}".format(category, self.id)

    def get_day(self, daynr):
        return self._days[daynr]

    @classmethod
    def from_id(cls, id):
        days = cache.get_index_files()[id]
        days = [Day.from_numpy_file(day, path) for day, path in days.items()]
        return Veugel(id, days)


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
