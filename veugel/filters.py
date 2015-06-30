"""
Contains all filters (removal of fake gaps, etc), which operates on Row objects.
"""

FAKE_GAP_JUMP_THRESHOLD = 5 # milliseconds
FAKE_GAP_LENGTH_MAX = 250
FAKE_GAP_LENGTH_MIN = 5
DAS_NOISE_THRESHOLD = 400

__all__ = (
    "filter_empty_rows",
    "filter_fake_gaps",
    "filter_illegal_das"
)

# FILTER FUNCTIONS #
def _is_fake_gap(gap_start, rows):
    """
    Determines if a gap is fake
    :return: boolean
    """
    # Beginning of file
    if gap_start == 0:
        return True

    # End of file is implicitly checked in filter_fake_gaps, by omitting to
    # yield the last gap anyway
    pass

    # Length of gap
    if len(rows) > FAKE_GAP_LENGTH_MAX:
        return True

    if len(rows) < FAKE_GAP_LENGTH_MIN:
        return True

    # Does it have a jump?
    for t1, t2 in zip(rows[1:], rows):
        if abs(t1.time - t2.time) > FAKE_GAP_JUMP_THRESHOLD:
            return True

    return False


def filter_fake_gaps(rows):
    gap = []
    gap_start = -1

    for rownr, row in enumerate(rows):
        if -0.01 < row.continuity_time < 0.01:
            # We're in a gap, append current row to 'gap' list
            if gap_start == -1:
                gap_start = rownr
            gap.append(row)
        elif gap:
            # We're at the end of a gap here
            if not _is_fake_gap(gap_start, gap):
                # This is not a fake gap, just yield all the rows
                yield from gap

            # Reset gap state
            del gap[:]
            gap_start = -1
        else:
            # We're not in a gap, nor at the end of one. Just yield the row.
            yield row

def filter_empty_rows(rows):
    return filter(any, rows)

def filter_illegal_das(rows):
    return (row for row in rows if row.duration_of_state <= DAS_NOISE_THRESHOLD)

# UTILITIES #
def get_all_filter_functions():
    return [globals()[fname] for fname in __all__]

def all_filters(rows):
    for filter_func in get_all_filter_functions():
        rows = filter_func(rows)
    return rows
