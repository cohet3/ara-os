# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'db.wd3.myworkdayjobs.com'

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
"externalPath":"
",'''

stp = '/job/'
page_ads =20 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://db.wd3.myworkdayjobs.com/wday/cxs/db/DBWebsite/jobs',
        )
    }
     ),
)


# def renew():
# torproxy.renew(controller)
# torproxy.connect()
# print "mi ip: ",torproxy.show_my_ip()

def crawl(web): 
    # renew()
    # sl.inputEncoding = 'latin1' # 'iso-8859-1'
    # sl.outputEncoding = 'utf-8'
    # sl.headers['Host'] = ""
    # sl.headers['User-Agent'] = ""
    # sl.headers['Accept'] = ""
    # sl.headers['Accept-Language'] = ""
    # sl.headers['Accept-Encoding'] = ""
    # sl.headers['Cookie'] = ""
    # sl.headers['Referer'] = ""
    # sl.headers['Content-Type'] = ""
    # sl.headers['Content-Length'] = ""
    # sl.start('')
    # -------------
    # response = urllib2.urlopen(web)
    # html = response.read()
    # sl = slavy.slavy()
    # sl.start(web)
    # sl.metaExtract = True
    # sl.WR = ["virtual:{0}".format(html)]
    # sl.extract(xtr)
    # -------------
    # req = urllib2.Request(url=url, headers=sl.headers, data=data)
    # response= urllib2.urlopen(req)
    # html = response.read()
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    # ~ buf = StringIO(response.read())
    # ~ f = gzip.GzipFile(fileobj=buf)
    # ~ html = f.read()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    # sl = slavy.slavy()
    # sl.start(web)
    # sl.metaExtract = True
    # sl.WR = ["virtual:{0}".format(html)]
    # sl.extract(xtr)
    # -------------
    # sl.WR = [web]
    # sl.polite(0,1)

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    
    headers = {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US',
        'Connection':'keep-alive',
        'Content-Length':'104',
        'Content-Type':'application/json',
        # 'Cookie':'wday_vps_cookie=2602997258.53810.0000; TS014c1515=01f62963044138aaa7a6d7be7c2c9e0a362d62fdb2b5456dfa65092cee05e776da1903e3f50824c023b6c9eaad8b7f21a6d9da4871; wd-browser-id=acbdc33a-df15-4392-b849-286dc8fcf052; PLAY_SESSION=3ce44b88e4c923de6791b3cc029decea73dbbe34-db_pSessionId=h2g03fon373epeoor8dn9alrmf&instance=wd3prvps0001a; timezoneOffset=-120',
        'Host':'db.wd3.myworkdayjobs.com',
        'Origin':'https://db.wd3.myworkdayjobs.com',
        'Referer':'https://db.wd3.myworkdayjobs.com/DBWebsite/?Country=8cd04a563fd94da7b06857a79faaf815',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    }

    data = '''{"appliedFacets":{"Country":["8cd04a563fd94da7b06857a79faaf815"]},"limit":20,"offset":0,"searchText":""}'''
    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://db.wd3.myworkdayjobs.com/en-US/DBWebsite{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls

    # Para pruebas
    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    # exit(0)

    #if not len(sl.WR):
    #    raise Exception('[WARN] Empty web region')

    #sl.extract(xtr)

    #if not len(sl.M):
    #    raise Exception('[WARN] Empty Model')

    for url in urls:
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            # 'Cookie':'wday_vps_cookie=2602997258.53810.0000; TS014c1515=01f62963044138aaa7a6d7be7c2c9e0a362d62fdb2b5456dfa65092cee05e776da1903e3f50824c023b6c9eaad8b7f21a6d9da4871; PLAY_SESSION=3ce44b88e4c923de6791b3cc029decea73dbbe34-db_pSessionId=h2g03fon373epeoor8dn9alrmf&instance=wd3prvps0001a; timezoneOffset=-120; wd-browser-id=305a6284-490f-42fd-a35e-7004b739aea2',
            'Host':'db.wd3.myworkdayjobs.com',
            'Referer':'https://db.wd3.myworkdayjobs.com/DBWebsite/?Country=8cd04a563fd94da7b06857a79faaf815',
            'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        }
        req = requests.get(url, headers = headers)
        datos = req.text
        #print datos
        #exit(0)
        sl.WR = ["virtual:{0}".format(datos.encode("iso-8859-1"))]
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


# saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_pt, pagination_generator, debug=False)
# saltcellar.crawl = crawl
# saltcellar.exterminate()

# new code for test auto debug script
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


    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_it, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
