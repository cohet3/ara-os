# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
import libnacho
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'portale.during.it'

xtr = '''company
"name": "
"
city
"addressLocality": "
"
title
<h1 property="title" class="title">
</h1>
description
<div class="main col-md-8">
<aside class="col-md-4 col-lg-3 col-lg-offset-1">'''

stp = '/offerta-lavoro/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 60, 10))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '__RequestVerificationToken=pISg-AcQIHXYcGWLdcLlpVr07AC2m_yjRW7T_VowZ1UaX7UZW_EW9m_NESrANTgzFDoO1Ax3rNjeTwl0Rz5FxmahVlPQ8rlGl4CLgXhjMdg1&Start={page}&Length=10&IdJob=0&Keywords=&X-Requested-With=XMLHttpRequest',
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
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
    "Connection":"keep-alive",
    "Content-Length":"204",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"ai_user=Y9F0|2020-09-01T10:05:36.203Z; ASP.NET_SessionId=dvxnh1kwlhbgjbopxhuglhen; ARRAffinity=d305cb31365f56b824c391302a9289cdd1ab0bb0d78be153c515d313968b2822; __RequestVerificationToken=OAkvzWA-atU-hRMcEsl1GdKVYGFPSumcLhNPggBuyCce0yfNF6BOETceIYnI8oJ7Uu0cCU8M6a-B3v_Q25cCSbw5F0K9NGlHUT0jX7nX8VE1; ai_session=FxR90|1599581609014.51|1599581609014.51; tp_stylesheet=light_blue; tp_layout_mode=wide; footer_bg=dark; _ga=GA1.2.1866888963.1599581622; _gid=GA1.2.459958611.1599581622",
    "Host":"portale.during.it",
    "Origin":"https://portale.during.it",
    "Referer":"https://portale.during.it/ricerca-annunci",
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-origin",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
    }
    
    req= requests.post(url="https://portale.during.it/CompanyJobOrder/PublishedGetList?Length=15", data=web, headers=headers)
    data=req.text.encode("utf-8")
    sl.WR = ["virtual:{0}".format(data)]
    sl.step(stp)

    sl.WR = ["{0}".format(url.decode("utf-8")) for url in sl.WR]

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
        ad['description'] = libnacho.emojis(re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", "")))
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

