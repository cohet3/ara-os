# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'posizioniaperte.bancaifis.it'

xtr = '''title
"title":"
",
description
"description":"
",
city
"addressLocality": "
"\}\}'''

xtr_url = '''url
<a href="/annunci-lavoro
"'''

stp = '/annunci-lavoro/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 8))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://posizioniaperte.bancaifis.it/?ctl191=1&StartupViewID=TableView&RunDefaultAction=true&PagerAnnunci={page}',
        )
    }
     ),
)


# def renew():
# torproxy.renew(controller)
# torproxy.connect()
# print "mi ip: ",torproxy.show_my_ip()

def crawl(web): 

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    # sl.step(stp)

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9,en;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        # 'Cookie':'AltamiraLanguageCookie=Culture=it-IT; ASP.NET_SessionId=delmgppr4wz4v3jiabghuije; Altamira.Web.Security=; Altamira.Web.Security.JWT.Token=; Altamira.Web.Security.JWT.RefreshToken=; Altamira.CookiePrivacy=1,0,0; visid_incap_2521437=3uDkxom1Sl2HLYHjZqS3t885qGIAAAAAQUIPAAAAAADkDemzT04hDJx8hVPx5rrm; incap_ses_313_2521437=PVw0CCuZhhyZ7ykHDQBYBM85qGIAAAAAMFa6noz2GaS6acMOAOyYNA==; _hjFirstSeen=1; _hjSession_994086=eyJpZCI6ImU2MjgwZGM1LWI4NTctNGZkNC1hNDlkLTM2YzZhNTNmMWZjOSIsImNyZWF0ZWQiOjE2NTUxOTIwMTg0NzEsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gid=GA1.2.512963820.1655192019; OptanonAlertBoxClosed=2022-06-14T07:33:44.821Z; _gcl_au=1.1.1336010648.1655192025; _uetsid=526768e0ebb411ec8a28ff46f81ba7d5; _uetvid=526801b0ebb411ecb73c5b6ea5236417; _fbp=fb.1.1655192025278.1589572930; _hjSessionUser_994086=eyJpZCI6IjJiZDQ1Mzg5LTYxYmMtNTBjYS1hNzRjLTI0MjdlYTgyOGQ5YiIsImNyZWF0ZWQiOjE2NTUxOTIwMTgzOTksImV4aXN0aW5nIjp0cnVlfQ==; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+14+2022+09%3A44%3A24+GMT%2B0200+(hora+de+verano+de+Europa+central)&version=6.29.0&isIABGlobal=false&hosts=&genVendors=&consentId=d3991295-5ada-4584-b9d5-9e92ff1da13e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=ES%3BMD&AwaitingReconsent=false; _ga_6N3SYC17LQ=GS1.1.1655192024.1.1.1655192664.60; _ga=GA1.1.962009753.1655192019',
        'Host':'posizioniaperte.bancaifis.it',
        'Referer':'https://posizioniaperte.bancaifis.it/?ctl191=7&StartupViewID=TableView&RunDefaultAction=true&PagerAnnunci=7',
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

    req = requests.get(url = web, headers = headers)
    datos = req.text
    #print datos
    #exit(0)
    
    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://posizioniaperte.bancaifis.it/annunci-lavoro{0}".format(x.get("url", "")) for x in sl.M]

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
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", ""))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] =offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

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


    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_it, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()

