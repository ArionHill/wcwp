import urllib2
import re
import itertools


def download(url, user_agent='wswp', num_retries=2):
    print 'Downloading: ', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error: ', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # 4xx: request fail.
                # 5xx: service error. retry is needed.
                # recursively retry 5xx HTTP errors.
                return download(url, num_retries - 1)
    return html


def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # print sitemap
    # extract the sitemap links.
    # links = re.findall('<loc>(.*?)</loc>', sitemap)
    links = re.findall('<td><div><a href="(.*?)">', sitemap)
    # download each link
    for link in links:
        html = download('/'.join(url.split('/')[0:-1]) + link)


if __name__ == '__main__':
    url = 'http://httpstat.us/500'
    url = 'http://example.webscraping.com/sitemap.xml'
    url = 'http://example.webscraping.com/sitemap.xml'
    crawl_sitemap(url)
    # download(url)
