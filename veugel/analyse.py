import multiprocessing

from itertools import repeat
from veugel.veugel import Veugel


def default_aggregator(*veugels):
    return veugels

def aggregate(aggregator, veugel_ids):
    veugel_ids = (veugel_ids,) if isinstance(veugel_ids, int) else veugel_ids
    veugels = map(Veugel.from_id, veugel_ids)
    return aggregator(*veugels)

def analyse(veugel_ids, plotter, aggregator=default_aggregator):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    aggregated = pool.starmap(aggregate, zip(repeat(aggregator), veugel_ids))
    plotter(aggregated)
