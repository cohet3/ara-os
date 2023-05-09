# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'allegion.wd5.myworkdayjobs.com'

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
page_ads = 10
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://allegion.wd5.myworkdayjobs.com/wday/cxs/allegion/careers/jobs',
        )
    }
     ),
)

def trad(tipo):
    traduccion = ''
    if tipo == "FULL_TIME":
        traduccion = "Indefinido"
    elif tipo == "TEMPORARY":
        traduccion = "Temporal"
    elif tipo == "CONTRACTOR":
        traduccion = "Freelance"
    elif tipo == "INTERN":
        traduccion = "Prácticas"

    if "PART_TIME" in tipo:
        if traduccion:
            traduccion = traduccion + ", media jornada"
        else:
            traduccion = 'Media jornada'
    else:
        if traduccion:        
            traduccion = traduccion + ", jornada completa"
        else:
            traduccion = 'Jornada completa'

    return traduccion

def crawl(web):

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    #sl.step(stp)

    headers = {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es',
        'Connection':'keep-alive',
        'Content-Length':'106',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=666a9cfb464e553d97237362913282ebd9c204ab-allegion_pSessionId=mgn2676dri7osl201k0cprfseq&instance=wd5prvps0001f; wday_vps_cookie=2888184330.1075.0000; TS014c1515=018b6354fe47295c659781ceb943e65b31975c15e87b998f687c01a8ac83936c94c27106aba4bd38be4f57eab58a11c015806fa9c2; timezoneOffset=-60; wd-browser-id=c95ce9aa-869c-4a10-9379-b632514ac11c',
        'Host':'allegion.wd5.myworkdayjobs.com',
        'Origin':'https://allegion.wd5.myworkdayjobs.com',
        'Referer':'https://allegion.wd5.myworkdayjobs.com/es/careers/jobs?locations=94e33d79ccff1077c23047e6a03b68bc',
        'sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    data = '''{"appliedFacets":{"locations":["94e33d79ccff1077c23008cee093686f","94e33d79ccff1077c2301b0bd2936874"]},"limit":20,"offset":0,"searchText":""}'''

    req = requests.post(url = web, headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    urls = ["https://allegion.wd5.myworkdayjobs.com/es/careers{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = urls
    #Para pruebas
    #sl.printWR()
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
        ad['description'] = re.sub("&amp;","",re.sub("&amp;","&",re.sub("&#39;","'",re.sub("\\\\n","\n",re.sub("<.*?>","",re.sub("&lt;","<",re.sub("&gt;",">",offer.get("description", ""))))))))
        ad['url'] = offer.get("@url", "")
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
