# -*- coding: utf-8 -*-
from common import make_req, beautify
__author__ = 'ege'

base_url = "http://www.hurriyet.com.tr/index/"


def find_news_peek_url(url):
    bs = get_bs_html(url)
    if bs:
        news_by_date_parent = bs.find("div", {"class": "list scrollable"})
        if news_by_date_parent:
            entities = news_by_date_parent.findAll("a")
            top = 0
            date = None
            for entity in entities:
                try:
                    current_val = int(entity.small.text)
                except Exception:
                    continue
                if current_val > top:
                    top = current_val
                    date = entity.attrs[1][1]
            if date:
                return "%s{title}?d=%s" % (base_url, date)
    return None


def get_bs_html(page):
    r = make_req(page)
    if r:
        bs = beautify(r.text)
        return bs
    return None


def return_news_url(date, title):
    news_url = "%s%s?d=%s" % (base_url, title, date, )
    result_url = find_news_peek_url(news_url)
    if result_url:
        return result_url.format(title=title)
