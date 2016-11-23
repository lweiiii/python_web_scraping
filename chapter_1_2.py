# -*- coding:utf-8 -*-

import urllib2
import re
import itertools
import urlparse

example_url='http://example.webscraping.com/sitemap.xml'

def download(url,user_agent='wswp',num_retries=2):
    print 'Downloading:',url
    header={'User-Agent':user_agent}
    request=urllib2.Request(url,user_agent)
    try:
            html=urllib2.urlopen(request).read()
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

'''
ID遍历爬虫

for page in itertools.count(1):
    url='http://example.webscraping.com/view/-%d' %page
    print  "Current Downloading URL : " ,url
    html=download(url)
    if html is None:
        break
    else:
        pass
    ＃以下为改良的程序，实现连续下载5次错误才终止程序


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
'''

'''
#  此时的URL是相对路径
def link_crawler1(seed_url,link_regex):
    '''
    Crawl from the given seed URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # filter for links matching out regular expression
        for link in get_links(html):
            if re.match(link_regex,link):
                crawl_queue.append(link)
'''

def get_links(html):
    '''
    Return a list of links from html
    '''
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

'''
＃ 此时会循环爬虫，因为不同页面之间有联系的
def link_crawler2(seed_url,link_regex):
    '''
    Crawl from the given seed URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # filter for links matching out regular expression
        for link in get_links(html):
            if re.match(link_regex,link):
                link=urlparse.urljoin(seed_url,link)
                crawl_queue.append(link)
'''

def link_crawler(seed_url,link_regex):
    '''
    Crawl from the given seed URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
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
                    
link_crawler('http://example.webscraping.com','/(view|index)')