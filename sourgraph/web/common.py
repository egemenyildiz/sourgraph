# -*- coding: utf-8 -*-
import eventlet
import requests
from BeautifulSoup import BeautifulSoup

__author__ = 'ege'

HEADERS = {
    'User-Agent': 'Data Collector (sourgraph: github.com/egemenyildiz/sourgraph)',

}


def beautify(content):
    return BeautifulSoup(content)


def make_req(url):
    r = None
    try:
        with eventlet.Timeout(60):
            r = requests.get(url, headers=HEADERS)
    except Exception as e:
        print e
    return r
