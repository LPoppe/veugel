import logging

from veugel import relational
from veugel.analyse import analyse


def aggregate(veugel, brother):
    # Aggreagte data over here
    return veugel.name, brother.name

def plot(veugel_and_brothers):
    # Do plotting stuff here
    for veugel, brother in veugel_and_brothers:
        print(veugel, brother)

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)
    analyse(relational.BROTHERS.items(), plot, aggregate)
