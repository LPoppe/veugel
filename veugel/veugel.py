import logging
import statistics

log = logging.getLogger(__name__)

class Day(object):
    """
    Represents a day worth of data. I.e., the merged sheets of an ODS file.
    """
    def __init__(self, daynr, rows=()):
        """
        :type daynr: int
        :type rows: numpy.ndarray
        """
        self.daynr = daynr
        self.rows = rows

    def get_das_median(self):
        return self.rows.median("duration_of_state")

    def get_das_mean(self):
        return self.rows.mean("duration_of_state")

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


class Veugel(object):
    def __init__(self, name, days):
        self.name = name
        self.days = days

    def get_day(self, day):
        """
        :type day: int
        """
        # O(N), fugly :-)
        for d in self.days:
            if d.day == day:
                return d
        raise IndexError("Day {day} does not exist for {self.name!r}".format(**locals()))


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
    Veugels.from_cache()
