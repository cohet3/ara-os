# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context
from StringIO import StringIO
import gzip
from base_br import db_br, slavy, text, dalek
import libnacho

fetched_from = 'joinus.saint-gobain.com'
# no puedo quitar una tuberia del titulo he suprimido dos ofertas q les faltaba descripción.
xtr = '''title
<title>
\|
extra
<li class="offre-info--item">

city
<i class="icon icon-contrat-location"></i>
</li>
description
<div class="clearfix text-formatted field field--name-field-position-description field--type-text-long field--label-hidden field__item">
<div class="col-md-4 col-md-offset-1 col-sm-4 will-animate edito-medias">'''

xtr_url='''url
about="
"'''

stp = ''
page_ads = 20
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://joinus.saint-gobain.com/es-419?f%5B0%5D=pays%3Abr' ,
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
    # sl.step(stp)
    req =requests.get(url=web)
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ["https://joinus.saint-gobain.com{0}".format(x.get('url', '')) for x in sl.M]
       
    #Para pruebas
    # sl.printWR()
    #sl.printM()
    #sl.printstatus()
    sl.WR = sl.WR[1:-1]
    # exit()

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = re.sub(" |", "", offer.get("title", ""))
        ad['description'] = libnacho.xhtml(libnacho.emojis(offer.get("description", '')).decode('unicode-escape').encode('latin'))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary",'0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")
        
        if not ad["title"]:
            ad["title"] = re.sub("\|.*?$","",offer.get("title_aux",""))
            
        if not ad["salary"]:
            ad["salary"] = 0

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
