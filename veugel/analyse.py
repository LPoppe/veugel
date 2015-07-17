import multiprocessing

from itertools import repeat
from veugel.veugel import Veugel
from veugel.cache import get_index_files

def default_aggregator(*veugels):
    return veugels

def aggregate(aggregator__veugel_ids):
    aggregator, veugel_ids = aggregator__veugel_ids
    veugel_ids = (veugel_ids,) if isinstance(veugel_ids, int) else veugel_ids
    veugels = map(Veugel.from_id, veugel_ids)
    return aggregator(*veugels)

def plot(plotter__args):
    plotter, args = plotter__args
    return plotter(*args)

def analyse(veugel_ids, plotter, aggregator=default_aggregator, plot_threaded=False):
    get_index_files()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    aggregated = pool.imap(aggregate, zip(repeat(aggregator), veugel_ids))
    plotted = pool.imap(plot, zip(repeat(plotter), aggregated if plot_threaded else [aggregated]))
    return list(plotted)