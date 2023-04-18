# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_br import db_br, slavy, text, dalek, torproxy
# Si alguna vez da error de demasiadas cabeceras
# import httplib
# httplib._MAXHEADERS = 1000
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'presenzapsicologia.abler.com.br'

xtr = '''title
"title": "
",
description
"description": "
",
contract
"employmentType": "
",
company
"name": "
",
city
"addressLocality": "
",
province
"addressRegion": "
",
salary
"QuantitativeValue",.*?"value":
,'''

xtr_url = '''url
"slug":"
"'''

# stp = '/ver/'
page_ads = 21

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 5))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            ' https://presenzapsicologia.abler.com.br/api_v/v1/vagas.json?&page=1' ,
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
    # sl.inputEncoding = 'latin1' # 'iso-8859-1'
    # sl.outputEncoding = 'utf-8'
    sl.start(web)
    sl.metaExtract = True
    req = requests.get(url = web, verify = False)
    datos = req.json()['vacancies']['data']
    sl.WR = []
    for d in datos:
        sl.WR.append('https://presenzapsicologia.abler.com.br/vagas/{0}'.format(d['attributes']['slug']))

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
    #Para simular navegacion comentar los if y el extract, descomentar lo siguiente y tabular el for
    #for url in sl.WR:
    #    req = requests.get(url)
    #    datos = req.text
    #    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
    #    sl.extract(xtr)
    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
        ad['url'] = offer.get("@url", "")
        #Para simular navegacion comentar la linea anterior y descomentar la siguiente
        #ad['url'] = url
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_br, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()