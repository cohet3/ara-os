# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek


fetched_from = 'careers.philips.com'

xtr = '''city
"addressLocality" : "
"
extra
"identifier" : {

company
"name" : "
"
title
"title" : "
"
description
"description" : "
",
contract
"employmentType" : "
"'''

xtr_url = '''url
"commandLink":"
",'''

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://philips.wd3.myworkdayjobs.com/jobs-and-careers/5/refreshFacet/318c8bb6f553100021d223d9780d30be',
        )
      }
    ),
)

#def renew():
    #torproxy.renew(controller)
    #torproxy.connect()
    #print "mi ip: ",torproxy.show_my_ip()
def crawl(web):
    
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    #sl.step(stp)

    headers = {
    'Accept':'application/json,application/xml',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'es-ES,es;q=0.9',
    'Connection':'keep-alive',
    'Content-Length':'196',
    'Content-Type':'application/x-www-form-urlencoded',
    #'Cookie':'PLAY_SESSION=d37f226432ebaf9e5d14deeb19ea4cf8c1ff88ac-philips_pSessionId=gcportnnl9bb7b2vbbpagm3qvr&instance=wd3prvps0002g; wday_vps_cookie=2737214986.3635.0000; PLAY_LANG=es; timezoneOffset=-120',
    'Host':'philips.wd3.myworkdayjobs.com',
    'Origin':'https://philips.wd3.myworkdayjobs.com',
    'Referer':'https://philips.wd3.myworkdayjobs.com/jobs-and-careers/3/refreshFacet/318c8bb6f553100021d223d9780d30be',
    'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile':'?0',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    #'sessionSecureToken':'k3qjsfp7d96drt47o4u30eele4',
    'stats-perf':'db520db1c64a4806bd2d04f7b7fa9b6b,56,0,',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'workday-client-manifest-id':'mvp',
    'X-Workday-Client':'2021.22.015',
    }

    data = '''facets=locationHierarchy1&locationHierarchy1=locationHierarchy1%3A%3A6e1b2a934716103c2ade08475dff0100&sessionSecureToken=k3qjsfp7d96drt47o4u30eele4&clientRequestID=cb3885565e5a4d899a672fe40c368923'''

    req = requests.post(url = 'https://philips.wd3.myworkdayjobs.com/jobs-and-careers/3/replaceFacet/318c8bb6f553100021d223d9780d30be', headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://philips.wd3.myworkdayjobs.com{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls
    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

   
    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("&#43;", "+", re.sub("&nbsp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", "")))))))))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

        yield ad

#saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_pt, pagination_generator, debug=False)
#saltcellar.crawl = crawl
#saltcellar.exterminate()

#new code for test auto debug script
if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "test":
        debug_mode = True
    elif len(sys.argv) < 2:
        debug_mode = False
    else:
        print "usage: python filename.py (test)"
        print "example for test: python <filename.py> test "
        print "example for run: python <filename.py>"
        exit(1)

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
