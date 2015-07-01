import multiprocessing

from itertools import repeat
from veugel.veugel import Veugel


def default_aggregator(*veugels):
    return veugels

def aggregate(aggregator__veugel_ids):
    aggregator, veugel_ids = aggregator__veugel_ids
    veugel_ids = (veugel_ids,) if isinstance(veugel_ids, int) else veugel_ids
    veugels = map(Veugel.from_id, veugel_ids)
    return aggregator(*veugels)

def analyse(veugel_ids, plotter, aggregator=default_aggregator, plot_threaded=False):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    aggregated = pool.imap(aggregate, zip(repeat(aggregator), veugel_ids))
    list(pool.imap_unordered(plotter if plot_threaded else [plotter], aggregated))
