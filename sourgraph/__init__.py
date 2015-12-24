import argparse
import logging
import sys
from sourgraph.web.eksi import make_req, beautify, find_page_count, generate_urls, walk_page

__author__ = 'ege'


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('-> %(message)s')
ch.setFormatter(formatter)
LOGGER.addHandler(ch)
LOGGER.propagate = False

BASE_URL = 'http://eksisozluk.com/'

crawl_results = []


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="eksisozluk.com title",
                        type=lambda s: unicode(s, 'utf8'))
    parser.add_argument("-pr", "--page-range",
                        help="page range (e.g. 3-11)",
                        type=lambda s: unicode(s, 'utf8'))
    parser.add_argument("-sy", "--start-year",
                        help="0 point for x-axis (e.g. 2002)",
                        type=int, default=1999)
    parser.add_argument('--trim', dest='trim',
                        help="trim lower points in graph",
                        action='store_true')
    parser.set_defaults(trim=False)
    parser.add_argument('--with-news', dest='with_news',
                        help="include news from hurriyet.com",
                        action='store_true')
    parser.set_defaults(with_news=False)
    return parser.parse_args()


def squash_results(res):
    crawl_results.extend(res)


def run():
    start_year = args().start_year

    LOGGER.info("checking total page count")
    url = '%s%s' % (BASE_URL, args().title, )
    r = make_req(url)
    r = make_req("%s?searchform.when.from=%s-01-01&a=search" % (r.url, start_year))
    bs = beautify(r.text)
    if args().page_range:
        start, end = args().page_range.split('-')
        start, end = int(start), int(end)
    else:
        start, end = find_page_count(bs)

    if all([start, end]):
        import multiprocessing
        from time import sleep
        from progressbar import ProgressBar, Bar, FormatLabel, RotatingMarker

        LOGGER.info("generating urls between pages %d & %d for [%d - present]" %
                    (start, end, start_year))

        urls = generate_urls(r.url, start, end)

        LOGGER.info("scraping dates from entries...")

        pool = multiprocessing.Pool(processes=8)
        results = pool.map_async(walk_page, urls, callback=squash_results)
        pool.close()

        remaining = results._number_left
        progress_bar = ProgressBar(widgets=[FormatLabel('-> '), RotatingMarker(),
                                            FormatLabel(' '), Bar()],
                                   maxval=remaining).start()

        while True:
            if results.ready():
                break
            progress_bar.update(remaining - results._number_left)
            sleep(.05)

        progress_bar.finish()
        if results.ready():
            import itertools
            from sourgraph.graphs import make_graph

            title = args().title.lower()

            sorted_result_list = sorted(list(itertools.chain(*crawl_results)))
            LOGGER.info("generating graph...")
            top_date = make_graph(sorted_result_list, title=title,
                                  start_year=args().start_year, trim=args().trim)
            LOGGER.info("graph saved")
            if top_date and args().with_news:
                from sourgraph.web.hurriyet import return_news_url
                LOGGER.info("checking news...")
                news_url = return_news_url(top_date, title)
                if news_url:
                    LOGGER.info("news url: %s" % news_url)

                    import webbrowser
                    LOGGER.info("opening url...")
                    webbrowser.open(news_url, new=2)
                else:
                    LOGGER.info("couldn't find any news for '%s'" % title)
    LOGGER.info("bye!")


def main():
    try:
        run()
    except KeyboardInterrupt:
        LOGGER.info("bye!")
        sys.exit(0)
