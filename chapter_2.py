# -*- coding:utf-8 -*-


import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
from bs4 import BeautifulSoup
import lxml.html
import lxml.cssselect


def download(url,  num_retries, data=None):
    print 'Downloading:', url
    request = urllib2.Request(url, data)
    opener = urllib2.build_opener()
    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries-1, data)
        else:
            code = None
    return html


'''
用正则表达式匹配指定内容
url='http://example.webscraping.com/view/United-Kingdom-239'
html=download(url,5)
html_re=re.findall('[\'<"]td class="w2p_fw">(.*?)<[/]td>',html)
for i in html_re:
    print i
print "The data we want get is " ,html_re[1]

print findall('<tr id="places_area__row"><td class="w2p_fl"><label id="places_area__label" for="places_area">Area: </label></td><td class="w2p_fw">(.*?)</td>')
print findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>,html)
'''

'''
用BeautifulSoup来匹配内容
url='http://example.webscraping.com/view/United-Kingdom-239'
html=download(url,5)
soup=BeautifulSoup(html,'html.parser')
#locate the area row
tr=soup.find(attrs={'id':'places_area__row'})
#等于是一层一层的缩小范围，可以直接搜索attrs={'class':'w2p_fw'}，但是会出现多个结果
td=tr.find(attrs={'class':'w2p_fw'})
print td.text
'''

'''
#parse the HTML
tree = lxml.html.fromstring(html)
td =  tree.cssselect('tr#places_population__row > td.w2p_fw')[0]
area=td.text_content()
print area
'''

url='http://example.webscraping.com/view/United-Kingdom-239'
html=download(url,5)

fields=re.findall('<tr id="places_(.*?)__row">',html)[1:]
print fields
print
print
#print re.search('<tr id="places_area__row">.*?<td class="w2p_fw">(.*?)</td>', html).groups()
#print re.search('<tr id="places_area__row">.*?<td class="w2p_fw">(.*?)</td>', html).group(1) ---> ('244,820 square kilometres',)
##print re.search('<tr id="places_area__row">.*?<td class="w2p_fw">(.*?)</td>', html).group(0)--->输出整个字符串的内容

def re_scraper(html):
    results={}
    for field in fields:
        results[field] = re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' %field , html).groups()[0]
    return results

def bs_scraper(html):
    soup=BeautifulSoup(html,'html.parser')
    results={}
    for field in fields:
        results[field] = soup.find(attrs={'id': 'places_%s__row' %field}).find(attrs={'class':'w2p_fw'}).text
    return results

def lxml_scraper(html):
    tree=lxml.html.fromstring(html)
    results={}
    for field in fields:
        results[field]=tree.cssselect('table > tr#places_%s__row > td.w2p_fw' %field)[0].text_content()
    return results

#number of times to test each scraper
NUM_ITERATIONS=1000

for name,scraper in  [('Regular expressions',re_scraper),('BeautifulSoup',bs_scraper),('Lxml',lxml_scraper)]:
    #record start time of scrape
    start=time.time()
    for i in range(NUM_ITERATIONS):
        if scraper == "re_scraper":
            re.purge()
        result=scraper(html)
        #check scraped result is as expected
        assert(result['area'] == '244,820 square kilometres')
    #record end time of scrape and output the total
    end=time.time()
    print '%s:  %.2f seconds' %(name,end-start)












