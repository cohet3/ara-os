# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'https://careers.dupont.com/'

xtr = '''extra
<html lang="es"

title
"title":"
",
description
"descriptionTeaser":"
",
city
"cityStateCountry":"
",'''

xtr_url = '''url
"reqId":"
"'''

stp = '/es/es/job/'
page_ads = 6

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://careers.dupont.com/widgets' ,
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
    
    headers = {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'es-ES,es;q=0.9',
        'content-length':'438',
        'content-type':'application/json',
        # 'cookie':'notice_behavior=expressed,eu; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3; VISITED_LANG=es; VISITED_COUNTRY=es; Per_UniqueID=187227b257bb2b-12ba7b-1d8e-187227b257c12ad; in_ref=https%3A%2F%2Fwww.google.com%2F; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiJlYjQ5MjIzMC03ZWFiLTQ3ZTQtOGM5ZS1iNTI0NWViYzc1YjIifSwibmJmIjoxNjc5OTI0NjI5LCJpYXQiOjE2Nzk5MjQ2Mjl9.uM75KjIc63n0BWOJ8Bu7AxHz7WOwdoI2-cvpyBg5g0Q; JSESSIONID=eb492230-7eab-47e4-8c9e-b5245ebc75b2; PHPPPE_GCC=a',
        'origin':'https://careers.dupont.com',
        'referer':'https://careers.dupont.com/es/es/search-results',
        'sec-ch-ua':'"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-csrf-token':'dc1155603a4247d2b7abaad8dc7208cf',
    }

    data='''{"lang":"es_es","deviceType":"desktop","country":"es","pageName":"search-results","ddoKey":"refineSearch","sortBy":"","subsearch":"","from":0,"jobs":true,"counts":true,"all_fields":["category","country","state","city","type","locationType"],"size":10,"clearAll":false,"jdsource":"facets","isSliderEnable":false,"pageId":"page11","siteType":"external","keywords":"","global":true,"selected_fields":{"country":["Mexico"]},"locationData":{}}'''
    req =requests.post(url=web, data=data, headers=headers)
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ['https://careers.dupont.com/es/es/job/{0}'.format(x.get('url', '')) for x in sl.M]

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
