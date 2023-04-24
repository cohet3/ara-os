# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_es import db_es, slavy, text, dalek

# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'ibima.eu/category/empleo'

xtr = '''title
"name":"
- Instituto
description
<div class="g-font-size-16 g-line-height-1_8 g-mb-30">
Datos del contrato
contract
Modalidad de contratación:
</li>
company
<li>Ubicación:
</li>
salary
<li>Retribución bruta anual:
</li>
description2
<li>Jornada:
</div>
extra
<i class="fas fa-map-marker"></i>

city
<p class="mb-0">
</p>'''

xtr_url='''url
<a class="u-link-v5 g-color-gray-dark-v1 g-color-primary--hover" href="
"'''

stp = ''
page_ads = 10
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.ibima.eu/category/empleo',
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
    sl.step(stp)
    req =requests.get(url=web)
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ["{0}".format(x.get('url', '')) for x in sl.M]
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
        ad['description'] = offer.get("description", "") + offer.get("description2", "")
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "").decode('unicode-escape').encode('UTF-8')
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
