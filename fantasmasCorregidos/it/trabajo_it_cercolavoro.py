# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl
from base_it import db_it, slavy, text, dalek
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'cercolavoro.com'

xtr = '''title_aux
<title>
</title>
title
<h1 class="hero-title"><strong>
</h1>
company
<img class="logo-azienda-piccolo logo-azienda-secondo".*?title="
"
city
"addressLocality": "
"
description
<section>
</section>
salary
Retribuzione:</strong>
</li>
contract
<li>Orario:
</li>'''

stp = '/offerta.lavoro-.*?idfonte=\d{8,}$ -corso-di-formazione'
page_ads = 500
page_stp = 1
pagination_generator = lambda url: (url.format(page=x) for x in xrange(0,400,50))

pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.cercolavoro.com/lavoro?offset={page}&w=&l=italia&idl=',
        )
      }
    ),
)

def crawl(web):
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    sl.step(stp)

    #Para pruebas
    #sl.printWR()
    #sl.printstatus()
    # sl.WR = sl.WR[:5]

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)
    #sl.printM()

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['url'] = offer.get("@url", "")
        ad['description'] = offer.get("description", "")
        ad['title'] = re.sub('offerta di lavoro ','',offer.get("title", ""))
        ad['company'] = offer.get("company", "")
        ad['city'] = offer.get("city", "").lower()
        ad['province'] = offer.get("province", "")
        ad['salary'] = re.sub('non specificato','',offer.get("salary", ""))
        ad['contract'] = re.sub('Altro','',offer.get("contract", ""))
       
        if not offer.get("title",""):
            ad['title']= re.sub('offerta di lavoro |\|.*?$','',offer.get("title_aux",""))

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
