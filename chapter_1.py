import urllib2
import re


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
crawl_sitemap(example_url)