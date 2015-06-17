from collections import namedtuple
import functools
import glob
from itertools import chain, count
import json
import os
import multiprocessing
import pyexcel_ods3
import sys
import re

FIELDS = ["time", "continuity_time", "duration_of_state"]
FILENAME_RE = re.compile("(?P<name>.+)_(?P<day>[0-9]+)(_.+)?\.ods")
FAKE_GAP_JUMP_THRESHOLD = 5 # milliseconds
FAKE_GAP_LENGTH_THRESHOLD = 250


Datapoint = namedtuple("BaseDatapoint", FIELDS)


def parse_filename(filename):
    """Parse filename of the form "ISO3331_70_gaps" to a tuple of ("ISO3331", 70)"""
    match = FILENAME_RE.match(filename).groupdict()
    return match["name"], int(match["day"])

def to_datapoints(sheets):
    for sheet in map(iter, sheets):
        names = [n.lower() for n in next(sheet)]
        for row in sheet:
            rowdict = dict(zip(names, row))
            values = [rowdict[field] for field in FIELDS]
            yield Datapoint(*values)

def get_json_filename(path):
    _, filename = split_path(path)
    return os.path.join(get_cache_dir(path), "{}.json".format(filename[:-4]))

def get_cache_dir(filename):
    dir, _ = split_path(filename)
    return os.path.join(dir, "cache")

def split_path(path):
    """Returns a tuple with (dir, filename)"""
    return path.rsplit("/", 1)

def create_cache(path):
    json_filename = get_json_filename(path)
    _, day = parse_filename(path)
    sheets = pyexcel_ods3.get_data(path).values()
    day = Day(day=day, datapoints=list(to_datapoints(sheets)))

    cache_dir = get_cache_dir(path)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    open(json_filename, "w").write(day.to_json())


class Day(object):
    """
    Represents a day worth of data. I.e., the merged sheets of an ODS file.
    """
    def __init__(self, day, datapoints=()):
        self.day = day
        self.datapoints = list(filter(any, datapoints))

        self.remove_fake_gaps()

    def get_gaps(self):
        return list(self._get_gaps())

    def get_gaph_lengths(self):
        return [abs(from_ - to) for from_, to in self.get_gaps()]

    def _get_gaps(self):
        # -1 basically means "we're not in a gap"
        gap_start = -1

        for rownr, row in zip(count(), self.datapoints):
            if -0.01 < row.continuity_time < 0.01:
                if gap_start == -1:
                    gap_start = rownr
            elif gap_start != -1:
                yield (gap_start, rownr)
                gap_start = -1

        # If we're still in a gap when file ended, yield the gap
        if gap_start != -1:
            yield (gap_start, len(self.datapoints))

    def _is_fake_gap(self, gap):
        """
        Determines if a gap is fake
        :param gap: (from, to)
        :return: boolean
        """
        from_, to = gap

        # Beginning of file
        if from_ == 0:
            return True

        # End of file
        if to == len(self.datapoints):
            return True

        # Length of gap
        if abs(from_ - to) > FAKE_GAP_LENGTH_THRESHOLD:
            return True

        # Does it have a jump?
        times = self.datapoints[from_:to]
        for t1, t2 in zip([times[0]] + times, times):
            if abs(t1.time - t2.time) > FAKE_GAP_JUMP_THRESHOLD:
                return True

        return False

    def get_fake_gaps(self):
        """
        Fake gaps are gaps:

            1. At the beginning
            2. At the very end
            3. Having a row 'jumping' in time, i.e., more than 'threshold' milliseconds
        """
        return list(filter(self._is_fake_gap, self.get_gaps()))

    def remove_fake_gaps(self):
        self.remove_gaps(self.get_fake_gaps())

    def remove_gaps(self, gaps):
        """
        Remove gaps from datapoints

        :param gaps: [(from, to)]
        """
        offending_rows = set(chain(*[range(from_, to) for from_, to in gaps]))
        datapoints = [row for n, row in enumerate(self.datapoints) if n not in offending_rows]
        self.datapoints = datapoints

    def to_json(self):
        return json.dumps((self.day, FIELDS, self.datapoints), indent=2)

    @classmethod
    def from_json(cls, content):
        day, fields, datapoints = json.loads(content)
        assert fields == FIELDS, "Cache invalid. Remove cache folders?"
        return Day(day=day, datapoints=(Datapoint(*values) for values in datapoints))

    @classmethod
    def from_ods(cls, filename):
        # Can we use the cached version?
        json_filename = get_json_filename(filename)
        if os.path.exists(json_filename):
            return cls.from_json(open(json_filename).read())

        # We can't use the cached version, use external process to create caches (because
        # pyexcel_ods3 files do not get garbage collected..)
        print("Parsing {}".format(os.path.basename(filename)))
        p = multiprocessing.Process(target=create_cache, args=(filename,))
        p.start()
        p.join()

        return cls.from_ods(filename)


class Veugel(object):
    def __init__(self, name, days=()):
        self.name = name
        self.days = sorted(days, key=lambda d: d.day)

    @classmethod
    def from_folder(cls, path):
        pattern = os.path.join(os.path.abspath(path), "*.ods")
        spreadsheets = sorted(glob.glob(pattern))

        if not spreadsheets:
            raise ValueError("No spreadsheets at {pattern}".format(**locals()))

        first_filename = spreadsheets[0].split("/")[-1]
        name, _ = parse_filename(first_filename)
        return Veugel(name, days=map(Day.from_ods, spreadsheets))


if __name__ == "__main__":
    for veugel in map(Veugel.from_folder, sys.argv[1:]):
        for day in veugel.days:
            print(day.get_fake_gaps())
