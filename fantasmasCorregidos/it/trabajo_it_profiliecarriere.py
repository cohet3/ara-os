# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'profiliecarriere.it'

xtr = '''title
<h4 class="small-title">
</h4>
description
<div class="descrizione">
<h5 class="small-title">Area geografica</h5>
city
<div class="luoghi">
</div>'''

xtr_url = '''url
<a href="https://www.profiliecarriere.it/offerta-lavoro/
"'''

stp = 'idAnn='
page_ads = 5

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))

pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.profiliecarriere.it/offerte-lavoro-data/{page}' ,
        )
      }
    ),
)

def crawl(web):

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    #sl.step(stp)

    headers = {
        "accept":"*/*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"es-ES,es;q=0.9,de-DE;q=0.8,de;q=0.7,en;q=0.6,it;q=0.5",
        "content-length":"7",
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        #"cookie":"XSRF-TOKEN=eyJpdiI6IllpUkRLcTJEWk0ycE9CZ3dEeXdIb0E9PSIsInZhbHVlIjoienF3UVhmQUp6YVJRaTJ6d21pQ2g5RGlBaUhtT09WYzZOSEIzS2FxbjZaSk83RGkxc3FIc2tXSzYyOWI1dTk3cCIsIm1hYyI6IjgwMjAzNTMyZWNjMzBiYTFjNzUwMjZiYTMwZGMxZTljODMwYzdkMTQxYzI3MDgyMDk3ZDE2NjgxZDIxZTcyZDcifQ%3D%3D; profili_e_carriere_session=eyJpdiI6IndxZmhxMnJVcFRRamloZzhrWEQ1M1E9PSIsInZhbHVlIjoiZkUwVUpsYURlRFpPOVNBSitKMVJsWXlSSzdlMTM5SVwvNklpbFh3bVdydDlWUElDekRsZDRISjRoRUhkUHQ1UGciLCJtYWMiOiIwNjM2MGU3MjZkZDc1Y2NmOTljMjA0ODM5OWIzMWE5ZWMxYTcyNGFiNzg5ODIyMGFkYTdkMWZhNzIyZDhiMTQzIn0%3D",
        "origin":"https://www.profiliecarriere.it",
        "referer":"https://www.profiliecarriere.it/",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "x-csrf-token":"7bl8IkVTnyhMIREh6LCApGrVaxPNTbypXx3tYvwo",
        "x-requested-with":"XMLHttpRequest",
    }

    data = '''filtri='''

    req = requests.post(url = web, headers=headers, data = data, verify = False)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://www.profiliecarriere.it/offerta-lavoro/{0}".format(x.get("url", "")) for x in sl.M]
    sl.WR = list(dict.fromkeys(sl.WR))

    #Para pruebas
    # sl.printWR()
    #exit(0)
    #sl.printM()
    #sl.printstatus()
    #sl.WR = sl.WR[0:10]

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
        ad['salary'] = offer.get("salary",0)
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

        yield ad

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
