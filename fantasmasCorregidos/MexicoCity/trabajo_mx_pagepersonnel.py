# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl
from base_mx import db_es, slavy, text, dalek
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'pagepersonnel.com.mx'

xtr = '''title_aux
<title>
</title>
title
"title" : "
",
company
"name" : "
",
contract
"employmentType" : "
",
description
"description" : "
",
salary
"minValue" : "
",
city
"addressLocality" : "
",
province
"addressRegion" : "
",'''

stp = 'job-detail'
page_ads = 35
pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 2) )

pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'http://www.pagepersonnel.com.mx/jobs/asistentes/',
            'http://www.pagepersonnel.com.mx/jobs/banca-y-servicios-financieros/',
            'http://www.pagepersonnel.com.mx/jobs/cadena-de-suministro-y-compras/',
            'http://www.pagepersonnel.com.mx/jobs/finanzas-e-impuestos/',
            'http://www.pagepersonnel.com.mx/jobs/healthcare/',
            'http://www.pagepersonnel.com.mx/jobs/ingenier%C3%ADa-y-manufactura/',
            'http://www.pagepersonnel.com.mx/jobs/mercadotecnia/',
            'http://www.pagepersonnel.com.mx/jobs/recursos-humanos/',
            'http://www.pagepersonnel.com.mx/jobs/tecnolog%C3%ADas-de-la-informaci%C3%B3n/',
            'http://www.pagepersonnel.com.mx/jobs/ventas/',
            
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
    # sl.printWR()
    #sl.printstatus()
    #sl.WR = sl.WR[0:5]

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')
        
        ad['url'] = offer.get("@url", "")
        ad['title'] = offer.get("title", "").strip().capitalize()
        ad['company'] = offer.get("company", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = "Ciudad de México" if offer.get("province","").strip().lower() == "distrito federal" else offer.get("province", "") 
        ad['contract'] = offer.get("contract", "")
        ad['description'] = offer.get("description", "").capitalize()
        ad['salary'] = re.sub('-.*?$|\D','',offer.get("salary", ""))

        if not ad['title']:
            ad['title'] = re.sub('- \d{5,}.*?$ |\|.*?$','',offer.get("title_aux", "")).strip().capitalize()
            
        if not ad['salary']:
            ad['salary'] = 0
            
        if ad['contract']:
            if offer.get("contract", "").find('Permanent'):
                ad['contract'] = 'tiempo completo'
                    
            if offer.get("contract", "").find('Temporary'):
                ad['contract'] = 'medio tiempo'

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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
