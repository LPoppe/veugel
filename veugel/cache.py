"""
Complete rewrite of original veugel files. Spreadsheets are now converted to numpy arrays
to support fast analysing and plotting; these arrays are stored as serialised numpy files
in HOME_DIR/cache.

Note that the numpy dumps
"""
import glob
import os
import multiprocessing
import pickle
import collections
import re

import numpy
import pyexcel_ods3

from veugel.filters import all_filters

THREADS = int(os.environ.get("THREADS", multiprocessing.cpu_count()))

# Directories / paths
HOME_DIR = os.path.expanduser("~/Sounddata")
CACHE_DIR = os.path.join(HOME_DIR, "cache")
CACHE_INDEX = os.path.join(CACHE_DIR, "index.pickle")
FILENAME_RE = re.compile("(?P<type>SELF|ISO)(?P<id>[0-9]+)_(?P<day>[0-9]+)(_.+)?\.ods$")

# Filter constants
FIELDS = collections.OrderedDict((
    ("time", "f4"),
    ("continuity_time", "f4"),
    ("duration_of_state", "i2")
))

def to_rows(sheets):
    Row = collections.namedtuple("Row", list(FIELDS))
    for sheet in map(iter, sheets):
        names = [n.lower() for n in next(sheet)]
        for row in sheet:
            row = dict(zip(names, row))
            row = tuple(row[fname] for fname in FIELDS)
            yield Row(*row)

def create_cache(path):
    """Converts an ODS file to a single numpy array"""
    # Parse filename / path
    match = FILENAME_RE.search(path).groupdict()
    veugel_id = int(match["id"])
    day = int(match["day"])

    cache_file = os.path.join(CACHE_DIR, "{veugel_id}_{day}.npy".format(**locals()))
    if not os.path.exists(cache_file):
        # Parse ods files
        print("Parsing {path}..".format(path=path))
        sheets = pyexcel_ods3.get_data(path).values()

        # FILTERING HERE...
        rows = all_filters(to_rows(sheets))

        # Create cache dir if it not exists
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)

        # Save numpy array in cache file
        array = numpy.array(list(rows), dtype=list(FIELDS.items()))
        numpy.save(open(cache_file, "wb"), array)

    return veugel_id, day, cache_file


def get_index_files():
    if os.path.exists(CACHE_INDEX):
        return pickle.load(open(CACHE_INDEX, "rb"))

    # We need to create the indices first
    ods_files = glob.glob(os.path.join(HOME_DIR, "*/*/*.ods"))
    cache_files = collections.defaultdict(dict)
    pool = multiprocessing.Pool(THREADS, maxtasksperchild=1)

    for veugel_id, day, path in pool.imap_unordered(create_cache, ods_files):
        cache_files[veugel_id][day] = path

    pickle.dump(cache_files, open(CACHE_INDEX, "wb"))

    return cache_files
