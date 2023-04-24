# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_es import db_es, slavy, text, dalek

# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'careers.hpe.com'

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
stp = 'job/'
page_ads = 10
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 20, 10))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '{{"appliedFacets":{{"locations":["f607629c2aa1011f182d68a0412cec45","62b0c47c914b01d0875d6d8c0924a163"]}},"limit":20,"offset":{page},"searchText":""}}',
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
    
    headers = {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US',
        'Connection':'keep-alive',
        'Content-Length':'141',
        'Content-Type':'application/json',
        # 'Cookie':'PLAY_SESSION=3c083ea63165f9efc4c1f958e59ef919a45b8044-hpe_pSessionId=jpsufpbkirvng0ielef296siq4&instance=wd5prvps0007i; wday_vps_cookie=2485531146.8755.0000; TS014c1515=018b6354fe230d6992d8502179bd74c7d361bf71c12eeef175735f1ef165db3915b221034b8521bc73fae83e7663b85c95607ae778; PLAY_LANG=en-US; timezoneOffset=-120; wd-browser-id=fc6c27b2-0ca1-4462-92f2-aebedabef05a',
        'Host':'hpe.wd5.myworkdayjobs.com',
        'Origin':'https://hpe.wd5.myworkdayjobs.com',
        'Referer':'https://hpe.wd5.myworkdayjobs.com/en-US/Jobsathpe?locations=f607629c2aa1011f182d68a0412cec45&locations=62b0c47c914b01d0875d6d8c0924a163',
        'sec-ch-ua':'"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }
    
    req = requests.post(url = 'https://hpe.wd5.myworkdayjobs.com/wday/cxs/hpe/Jobsathpe/jobs', headers = headers, data = web)
    datos = req.text
    # print datos
    # exit(0)
    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)

    sl.WR = ["https://hpe.wd5.myworkdayjobs.com/en-US/Jobsathpe{0}".format(x.get("url", "")) for x in sl.M]

    
    # Para pruebas
    # sl.printWR()
    # print "\nEn total hay " + str(len(sl.WR)) + " enlace(s)"
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
        
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] =offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = trad(offer.get("contract", ""))

        if not ad["title"]:
            ad["title"] = re.sub("\|.*?$", "", offer.get("title_aux", ""))

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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
