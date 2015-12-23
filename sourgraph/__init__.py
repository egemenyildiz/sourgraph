import argparse
import logging
import sys
from web.eksi import make_req, beautify, find_page_count, generate_urls, walk_page

__author__ = 'ege'


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('-> %(message)s')
ch.setFormatter(formatter)
LOGGER.addHandler(ch)

BASE_URL = 'http://eksisozluk.com/'

crawl_results = []


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="ek$i title",
                        type=lambda s: unicode(s, 'utf8'))
    parser.add_argument("-pr", "--page-range",
                        help="page range like \"3-11\"",
                        type=lambda s: unicode(s, 'utf8'))
    parser.add_argument("-sy", "--start-year",
                        help="start year (e.g. 2002)",
                        type=int, default=1999)
    parser.add_argument('--trim', dest='trim',
                        help="Trim lower points in graph",
                        action='store_true')
    parser.set_defaults(trim=False)
    parser.add_argument('--with-news', dest='with_news',
                        help="Include news from hurriyet.com",
                        action='store_true')
    parser.set_defaults(with_news=False)
    return parser.parse_args()


def squash_results(res):
    crawl_results.extend(res)


def run():
    start_year = args().start_year

    LOGGER.info("Requesting page counts...")
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

        LOGGER.info("Generating URLs between pages [%d - %d] 'till %d..." %
                    (start, end, start_year))
        urls = generate_urls(r.url, start, end)
        LOGGER.info("Crawling entries...")
        pool = multiprocessing.Pool(processes=8)
        results = pool.map_async(walk_page, urls, callback=squash_results)
        pool.close()

        remaining = results._number_left
        pbar = ProgressBar(widgets=[FormatLabel('-> '), RotatingMarker(), Bar()],
                           maxval=remaining).start()

        while True:
            if results.ready():
                break
            pbar.update(remaining - results._number_left)
            sleep(.05)

        pbar.finish()
        if results.ready():
            import itertools
            from graphs import make_graph

            sorted_result_list = sorted(list(itertools.chain(*crawl_results)))
            LOGGER.info("Generating graph...")
            top_date = make_graph(sorted_result_list, title=args().title,
                                  start_year=args().start_year, trim=args().trim)
            LOGGER.info("Graph saved...")
            if top_date and args().with_news:
                from web.hurriyet import return_news_url
                LOGGER.info("Checking news...")
                news_url = return_news_url(top_date, args().title)
                if news_url:
                    LOGGER.info("News url: %s" % news_url)
                else:
                    LOGGER.info("Couldn't find any news for '%s'" % args().title)
        LOGGER.info("Finished!")


def main():
    try:
        run()
    except KeyboardInterrupt:
        LOGGER.info("Exiting...")
        sys.exit(0)
