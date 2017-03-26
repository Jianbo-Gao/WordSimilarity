#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, csv, ssl, math

import urllib2, socket, socks
from bs4 import BeautifulSoup

from setting import *

def getaddrinfo(*args):
    # DNS on Socks
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

def google(search_str):
    print "searching: "+search_str
    # Deal with GFW
    default_socket = socket.socket
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    socket.getaddrinfo = getaddrinfo

    # Ignore HTTPS Certificate
    ssl._create_default_https_context = ssl._create_unverified_context

    # Search by Google
    url ='https://www.google.com/search?q=%s' % search_str
    request =urllib2.Request(url)
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
    request.add_header('User-agent', user_agent)
    response =urllib2.urlopen(request)
    html =response.read().decode("utf-8")
    soup = BeautifulSoup(html,"lxml")
    resultStats=soup.find(id="resultStats").encode("utf-8")
    resultList=str(resultStats).split(" ")
    if len(resultList) > 5:
        temp = resultList[2].split(",")
    else:
        temp = resultList[1][17:].split(",")
    count=""
    for i in xrange(len(temp)):
        count += temp[i]
    return int(count)

def sim_pagecount(wordpairs, filename):
    PAGECOUNT_DIR=os.path.join(RESULT_DIR, "pagecount")

    # Read Search Cache
    cache={}
    try:
        cachefile=file(os.path.join(PAGECOUNT_DIR,"cache.csv"),'rb')
        cachereader=csv.reader(cachefile)
        for line in cachereader:
            cache[line[0]]=line[1]
        cachefile.close()
    except Exception, e:
        print "no cache file."

    webjaccardfile=file(os.path.join(PAGECOUNT_DIR,"webjaccard_"+filename),'wb')
    webjaccardwriter=csv.writer(webjaccardfile)

    weboverlapfile=file(os.path.join(PAGECOUNT_DIR,"weboverlap_"+filename),'wb')
    weboverlapwriter=csv.writer(weboverlapfile)

    webdicefile=file(os.path.join(PAGECOUNT_DIR,"webdice_"+filename),'wb')
    webdicewriter=csv.writer(webdicefile)

    webpmifile=file(os.path.join(PAGECOUNT_DIR,"webpmi_"+filename),'wb')
    webpmiwriter=csv.writer(webpmifile)

    resultfiles=[webjaccardfile, weboverlapfile, webdicefile, webpmifile]
    resultwriters=[webjaccardwriter, weboverlapwriter, webdicewriter, webpmiwriter]


    for wordpair in wordpairs:
        try:
            pstr=wordpair[0]
            qstr=wordpair[1]
            pandqstr="%22"+pstr+"+and+"+qstr+"%22"

            if not cache.has_key(pstr):
                try:
                    cache[pstr]=google(pstr)
                except Exception, e:
                    print e
                    cache[pstr]=0
            if not cache.has_key(qstr):
                try:
                    cache[qstr]=google(qstr)
                except Exception, e:
                    print e
                    cache[qstr]=0
            if not cache.has_key(pandqstr):
                try:
                    cache[pandqstr]=google(pandqstr)
                except Exception, e:
                    print e
                    cache[pandqstr]=0

            p=cache[pstr]
            q=cache[qstr]
            pandq=cache[pandqstr]

            webjaccard_sim = 0
            weboverlap_sim = 0
            webdice_sim = 0
            webpmi_sim = 0

            # Data From http://www.statisticbrain.com/total-number-of-pages-indexed-by-google/
            googlepages = 30000000000000L

            # c=5 is from Paper http://www.ijcsi.org/papers/IJCSI-10-2-1-391-396.pdf
            if pandq > 5:
                try:
                    webjaccard_sim = 1.0*pandq/(p+q-pandq)
                except Exception, e:
                    print p, q, pandq
                    webjaccard_sim = -10000

                try:
                    weboverlap_sim = 1.0*pandq/min(p, q)
                except Exception, e:
                    print p, q, pandq
                    weboverlap_sim = -10000

                try:
                    webdice_sim = 2.0*pandq/(p+q)
                except Exception, e:
                    print p, q, pandq
                    webdice_sim = -10000

                try:
                    webpmi_sim = math.log((1.0*pandq*googlepages)/(p*q),2)
                except Exception, e:
                    print p, q, pandq
                    webpmi_sim = -10000

            webjaccard_result=(wordpair[0], wordpair[1], webjaccard_sim)
            weboverlap_result=(wordpair[0], wordpair[1], weboverlap_sim)
            webdice_result=(wordpair[0], wordpair[1], webdice_sim)
            webpmi_result=(wordpair[0], wordpair[1], webpmi_sim)

            results=[webjaccard_result, weboverlap_result, webdice_result, webpmi_result]

            for i in xrange(len(resultwriters)):
                writer = resultwriters[i]
                writer.writerow(results[i])
        except Exception, e:
            print e
            break

    # Read Search Cache
    cachefile=file(os.path.join(PAGECOUNT_DIR,"cache.csv"),'wb')
    cachewriter=csv.writer(cachefile)
    for key in cache:
        cachewriter.writerow([key, cache[key]])
    cachefile.close()

    for resultfile in resultfiles:
        resultfile.close()
