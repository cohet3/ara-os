# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'https://careers.wtwco.com/'

xtr = '''title
"title":"
"
city
"primary_city":"
"
description
<div data-field="description" class="jd-description">
</div>'''

xtr_url = '''url
"id":
,'''


stp = '/job-es/'
page_ads = 12

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 3))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://jobsapi-internal.m-cloud.io/api/job?callback=jobsCallback&facet%5B%5D=primary_country%3AMX&sortfield=open_date&sortorder=descending&Limit=12&Organization=2045&offset=1' ,
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
    # sl.step(stp)
    # headers = {
    #     'Accept':'*/*',
    #     'Accept-Encoding':'gzip, deflate, br',
    #     'Accept-Language':'es-ES,es;q=0.9',
    #     'Connection':'keep-alive',
    #     'Content-Length':'139',
    #     'Content-Type':'text/plain;charset=UTF-8',
    #     'Host':'bam.nr-data.net',
    #     'Origin':'https://careers.wtwco.com',
    #     'Referer':'https://careers.wtwco.com/es/job-search-results/?primary_country=MX',
    #     'sec-ch-ua':'"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    #     'sec-ch-ua-mobile':'?0',
    #     'sec-ch-ua-platform':'"Windows"',
    #     'Sec-Fetch-Dest':'empty',
    #     'Sec-Fetch-Mode':'no-cors',
    #     'Sec-Fetch-Site':'cross-site',
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    # }
    data = '''a=121917868&v=1228.PROD&to=Z1NWNkIED0cDABAIWF4ZdQFEDA5aTRcBDEdcV0AHHQcUXQ4HARM%3D&rst=278112&ck=0&s=3f52cff960f2a860&ref=https://careers.wtwco.com/es/job-search-results/'''
    req =requests.get(url=web) # data=data, headers=headers
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ["https://careers.wtwco.com/es/job-es/{0}".format(x.get('url', '')) for x in sl.M]

    # Para pruebas
    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    # exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
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
