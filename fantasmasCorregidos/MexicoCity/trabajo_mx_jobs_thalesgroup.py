# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'jobs.thalesgroup.com'

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
"'''

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://thales.wd3.myworkdayjobs.com/wday/cxs/thales/Careers/jobs' ,
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
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US',
        'Connection':'keep-alive',
        'Content-Length':'112',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=c3ca6803dc285cf8a26054672cc525c1cd9cda99-thales_pSessionId=k7khqcnoo7dvuhqf0gafh9q6n1&instance=wd3prvps0005c; wday_vps_cookie=2586220042.58930.0000; timezoneOffset=-60; wd-browser-id=07496556-e9a0-48e4-9221-cbae8f73d73d; TS014c1515=01f6296304b38a5a2130ae04b6c93d02d306fe818a171b4ecbe0216213cb9a4357a8f50344e23b2b13253f8c68f0063db27b63a860',
        'Host':'thales.wd3.myworkdayjobs.com',
        'Origin':'https://thales.wd3.myworkdayjobs.com',
        'Referer':'https://thales.wd3.myworkdayjobs.com/en-US/Careers/jobs?ActiveFacetID=3996063&CurrentPage=1&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&FacetFilters%5B0%5D.ID=3996063&FacetFilters%5B0%5D.FacetType=2&FacetFilters%5B0%5D.Count=10&FacetFilters%5B0%5D.Display=Mexico&FacetFilters%5B0%5D.IsApplied=true&FacetFilters%5B0%5D.FieldName=&SearchResultsModuleName=Search%20Results&SearchFiltersModuleName=Search%20Filters&SortCriteria=0&SortDirection=1&SearchType=5&PostalCode=&fc=&fl=&fcf=&afc=&afl=&afcf=&locationCountry=e2adff9272454660ac4fdb56fc70bb51',
        'sec-ch-ua':'"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    data = '''{"appliedFacets":{"locationCountry":["e2adff9272454660ac4fdb56fc70bb51"]},"limit":20,"offset":0,"searchText":""}'''

    req = requests.post(url = web, headers = headers, data = data, verify = False)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://thales.wd3.myworkdayjobs.com/en-US/Careers{0}".format(x.get("url", "")) for x in sl.M]

    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]
    # exit(0)

    if not len(sl.WR):
       raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
       raise Exception('[WARN] Empty Model')
   

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("Â", "", re.sub("Ã¡", "á",re.sub("Ã©", "é", re.sub("Ã­", "í",re.sub("Ã³", "ó",re.sub("Ãº", "ú", re.sub("Ã", "Á", re.sub("Ã", "Í", re.sub("Ã", "Ó", re.sub("Ã±", "ñ", re.sub("Ã", "Ñ", re.sub("Ã", "Ö", re.sub("Ã¼", "ü", re.sub("â", "", re.sub("â|â", " - ", re.sub("â¦", "...", re.sub("â", "\"", re.sub("â", "\"", re.sub("â", "'", re.sub("â¢", "·", offer.get("description", "").decode("unicode-escape").encode("utf-8")))))))))))))))))))))
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
