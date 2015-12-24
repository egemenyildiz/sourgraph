# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import Counter
from datetime import datetime, timedelta
import math
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt

__author__ = 'ege'


def range_check(x, p):
    return x.most_common(1)[0][1] - x.most_common(len(x))[-1][1] < x.most_common(1)[0][1] * p


def create_figure(l, title, start_year):
    start_date = datetime(start_year, 1, 1)
    plt.figure()
    plt.grid(True)
    ax = plt.subplot()
    ax.set_title(u"%s" % title, fontsize=8)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(8)

    date_keys = []
    for date in l.keys():
        date_keys.append(datetime.strptime(date, '%B, %Y').date())

    x, y = zip(*sorted(zip(date_keys, l.values()), key=lambda z: z[0]))

    ax.plot_date(x=x, y=y, fmt="r-")
    ax.set_ylabel(u"entries", fontsize=8)
    ax.set_ylim(bottom=0, top=l.most_common(1)[0][1] * 1.15)
    months_fmt = DateFormatter("%B, %Y")
    ax.xaxis.set_major_formatter(months_fmt)
    for tick in ax.get_xticklabels():
        tick.set_rotation(70)

    bo3 = l.most_common(3)  # todo: get more precise entry dates for these points
    top_date = None
    for top_entry in bo3:
        # todo: check if we already set an annotation to that point
        y_index = y.index(top_entry[1])
        if not top_date:
            top_date = x[y_index].strftime("%Y%m")
        ax.annotate("%s (%s)" % (top_entry[1], x[y_index].strftime('%B, %Y')),
                    (x[y_index], y[y_index] + 1.25),
                    ha="center", va="center",
                    bbox=dict(boxstyle='round,pad=0.3', fc='#F5F5F5', ec='black'),
                    fontsize=8)

    ax.set_xlim([start_date, datetime.now() + timedelta(minutes=360)])
    plt.subplots_adjust(bottom=0.20)
    return plt, top_date


def make_graph(x, title, start_year, trim):
    l = Counter(["%s, %s" % (x.strftime("%B"), x.year) for x in x])

    if trim:
        while True:
            if range_check(l, 0.99) or len(l) < 3:
                break
            l.pop(l.most_common(len(l))[-int(math.ceil(len(l) * 0.1)):][0][0])

    plot, top_date = create_figure(l, title, start_year)
    plot.savefig('%s.png' % (title.replace(' ', '_')))
    return top_date
