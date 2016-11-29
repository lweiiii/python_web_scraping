# -*- coding:utf-8 -*-

import urllib2
import urlparse
import re
import itertools
import urlparse
import datetime

example_url='http://example.webscraping.com/sitemap.xml'

def download(url,user_agent='wswp',proxy=None,num_retries=2):
    print 'Downloading:',url
    header={'User-Agent':user_agent}
    request=urllib2.Request(url,headers=header)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
            html=opener.open(request).read()
    except urllib2.URLError as e:
            print 'Downloading error:', e.reason
            html=None
            if num_retries>0:
                if hasattr(e,'code') and 500<=e.code<600:
                    #recurively retry 5xx HTTP errors
                    return download3(url,num_retries-1)
    return html

def crawl_sitemap(url):
    #download the sitemap file
    sitemap=download(url)
    #extract the sitemap links
    links=re.findall('<loc>(.*?)</loc>',sitemap)
    #download each link
    for link in links:
        html=download(link)

# maximum number of consecutive download errors allowed
max_errors = 5
# current number of consecutive download errors
num_errors = 0 

for page in itertools.count(1):
    url='http://example.webscraping.com/view/-%d' %page
    html=download(url)
    if html is None:
        # received an error trying to download this webpage
        num_errors += 1
        if num_errors == max_errors:
        # reached maximum number of consecutive errors so exits
            break
        else:
            # sucess - can scrape the result
            num_errors = 0 

def get_links(html):
    '''
    Return a list of links from html
    '''
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

def link_crawler(seed_url,link_regex):
    '''
    Crawl from the given seed URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robot.txt restrictions
        if rp.can_fetch(user_agent,url):
            pass
        else:
            print 'Block By robots.txt' ,url
        html = download(url)
        # filter for links matching out regular expression
        for link in get_links(html):
            # check if link matches expected regex
            if re.match(link_regex,link):
                # form absolute link
                link=urlparse.urljoin(seed_url,link)
                # check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)
'''
control delay
'''
class Throttle:
    '''
    Add a delay between downloads for each domain
    '''
    def __init__(self,delay):
        # amount of delay between download for each domain
        self.delay=delay
        # timestamp of when a domain was last accessed
        self.domains={}

    def wait(self,url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domain.get(domain)

        if self.delay>0 and last_accessed is not None:
            sleep_secs=self.delay - (datetime.datetime.now()-last_accessed).second
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain]=datetime.datetime.now()  
























