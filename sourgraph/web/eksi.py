from datetime import datetime
import re
import logging
from common import make_req, beautify

LOGGER = logging.getLogger(__name__)

__author__ = 'ege'


DATE_TIME_PATTERN = r'(?P<date>(\d+.\d+.\d+))\s(?P<time>(\d+:\d+))'
DATE_PATTERN = r'(?P<date>(\d+.\d+.\d+))'


def find_page_count(bs):
    entity = bs.find("div", {"class": "pager"})
    try:
        return int(entity.attrs[1][1]), int(entity.attrs[2][1])
    except TypeError as te:
        return None, None


def find_entries(bs):
    entries = bs.find("ul", {"id": "entry-list"})
    entities = entries.findAll("div", {"class": "info"})
    dates = []
    if entities:
        for entity in entities:
            date_object = None
            try:
                x = re.search(DATE_TIME_PATTERN, entity.a.text)
                date_object = datetime.strptime('%s %s' % (x.group('date'), x.group('time')), '%d.%m.%Y %H:%M')
            except AttributeError as ae:
                try:
                    x = re.search(DATE_PATTERN, entity.a.text)
                    date_object = datetime.strptime('%s' % x.group('date'), '%d.%m.%Y')
                except Exception as e:
                    LOGGER.exception(e)

            if date_object:
                dates.append(date_object)


    return dates


def walk_page(page):
    r = make_req(page)
    if r:
        bs = beautify(r.text)
        return find_entries(bs)
    return []


def generate_urls(redirected_url, start=1, end=1):
    return ["%s&p=%d" % (redirected_url, x) for x in xrange(start, end + 1)]