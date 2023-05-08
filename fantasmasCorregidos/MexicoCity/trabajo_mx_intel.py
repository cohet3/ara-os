# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'intel.wd1.myworkdayjobs.com'

xtr_url = '''url
"externalPath":"
"'''

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

stp = 'AAA'
page_ads = 18
#paginas = 0

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs' ,
        )
      }
    ),
)

#def renew():
    #torproxy.renew(controller)
    #torproxy.connect()
    #print "mi ip: ",torproxy.show_my_ip()
def crawl(web):

    for paginas in xrange(0, 120, 20):
        sl = slavy.slavy()
        sl.start(web)
        sl.metaExtract = True
        #sl.step(stp)
        headers= {
            'Accept':'application/json',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US',
            'Connection':'keep-alive',
            'Content-Length':'108',
            'Content-Type':'application/json',
            #'Cookie':'PLAY_SESSION=3a5d691b1822a5f016c5ac9f8e28890f4ac0751e-intel_pSessionId=dqpm2fe62e8iqbi40n4sc3jq3v&instance=wd1prvps0006i; wday_vps_cookie=3307645450.8755.0000; timezoneOffset=-120; TS014c1515=01560d08390489e6b2088e7cdd5387d10c8b71a36a5838d1a557dbf40424a6101f119b5c47afe1488de98dac5c636cd4a0db84454c; wd-browser-id=79a5699c-69c6-4be1-b509-cbdcb41e8cc1',
            'Host':'intel.wd1.myworkdayjobs.com',
            'Origin':'https://intel.wd1.myworkdayjobs.com',
            'Referer':'https://intel.wd1.myworkdayjobs.com/en-US/External?locations=1e4a4eb3adf101717b7c0175bf81decd',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        }
        data ='''{"appliedFacets":{"locations":["1e4a4eb3adf101717b7c0175bf81decd"]},"limit":20,"offset":''' + str(paginas) + ''',"searchText":""}'''
        #print data
        req = requests.post(url = web, headers = headers, data = data)
        datos = req.text
        #print datos
        #exit(0)

        sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

        sl.extract(xtr_url)
        sl.WR = ["https://intel.wd1.myworkdayjobs.com/en-US/External{0}".format(x.get("url", "")) for x in sl.M]

        # Para pruebas
        #sl.printWR()
        # sl.printM()
        # sl.printstatus()
        # sl.WR = sl.WR[0:5]
        #exit(0)

        if not len(sl.WR):
            raise Exception('[WARN] Empty web region')

        #sl.extract(xtr)

        #if not len(sl.M):
            #raise Exception('[WARN] Empty Model')

        for url in sl.WR:
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                #'Cookie':'PLAY_SESSION=3a5d691b1822a5f016c5ac9f8e28890f4ac0751e-intel_pSessionId=dqpm2fe62e8iqbi40n4sc3jq3v&instance=wd1prvps0006i; wday_vps_cookie=3307645450.8755.0000; timezoneOffset=-120; wd-browser-id=0a7d048c-7bad-4ae3-a318-2f9c3e4b0b83; TS014c1515=01560d0839dbf0212991d9c0c44438b0110a36359123ed4c6e7ada2a0eea06076233f18d09a15901222e1cc69e3ffaadcda8784954',
                'Host':'intel.wd1.myworkdayjobs.com',
                'Referer':'https://intel.wd1.myworkdayjobs.com/en-US/External?locations=1e4a4eb3adf101717b7c0175bf81decd',
                'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile':'?0',
                'sec-ch-ua-platform':'"Windows"',
                'Sec-Fetch-Dest':'document',
                'Sec-Fetch-Mode':'navigate',
                'Sec-Fetch-Site':'same-origin',
                'Sec-Fetch-User':'?1',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            }
            req = requests.get(url, headers = headers)
            datos = req.text
            #print datos
            #exit(0)
            sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
            sl.extract(xtr)

            for offer in sl.M:
                ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

                ad['title'] = offer.get("title", "")
                ad['description'] = offer.get("description", "")
                ad['url'] = url
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
