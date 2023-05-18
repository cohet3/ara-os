# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'airliquide.wd3.myworkdayjobs.com'

xtr = '''city
"addressLocality" : "
"
extra
"hiringOrganization" : {

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
"externalPath":"/job/
"'''

stp = 'AAA'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://airliquidehr.wd3.myworkdayjobs.com/wday/cxs/airliquidehr/AirLiquideExternalCareer/jobs' ,
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

    headers={
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es',
        'Connection':'keep-alive',
        'Content-Length':'112',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=5a05209284c0a92d86c95c17504cb928a74aee1b-airliquidehr_pSessionId=nmi7ihgqi64hoqd9vvr6gcueat&instance=wd3prvps0004e; wday_vps_cookie=2569442826.64050.0000; timezoneOffset=-120; wd-browser-id=e26f392b-0f48-407b-892a-5f34a578d591; CALYPSO_CSRF_TOKEN=443e96c1-48ed-49b8-be30-37404c53bf08; TS014c1515=01f6296304790a65e7050b8618904e276be29793db32b8e59a07c4ff841bd1b5c80b6a32a51587f4761387f96156b0a552d55a2ae5',
        'Host':'airliquidehr.wd3.myworkdayjobs.com',
        'Origin':'https://airliquidehr.wd3.myworkdayjobs.com',
        'Referer':'https://airliquidehr.wd3.myworkdayjobs.com/es/AirLiquideExternalCareer?locationCountry=8cd04a563fd94da7b06857a79faaf815',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-CALYPSO-CSRF-TOKEN':'443e96c1-48ed-49b8-be30-37404c53bf08',
        'sec-ch-ua':'"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
    }
    data = '''{"appliedFacets":{"locationCountry":["8cd04a563fd94da7b06857a79faaf815"]},"limit":20,"offset":0,"searchText":""}'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://airliquidehr.wd3.myworkdayjobs.com/es/AirLiquideExternalCareer/job/{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls

    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
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
        ad['description'] = re.sub("•","-",offer.get("description", ""))
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_it, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()