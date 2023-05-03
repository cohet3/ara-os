# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'turistore.sherlockhr.computrabajo.com'

xtr = '''title
<title>
</title>
description
<p class="mt30 t_word_wrap">
<h3 class="mt20 fwB">Resumen del empleo</h3>
extra
<div class="vt"><span class="icon i_address"></span></div>
<div class="w100 pl15">
city

</div>
extra
<div class="vt"><span class="icon i_salary"></span></div>
<div class="w100 pl15">
salary

</div>
extra
<div class="vt"><span class="icon i_workday"></span></div>
<div class="w100 pl15">
contract

</div>'''

xtr_url = '''url
<h3 itemprop="title" class="fs20"><a itemprop="url" href="
">'''

stp = '/ofertas/'
page_ads = 36

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://superpapelera.sherlockhr.computrabajo.com/ofertas/' ,
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
    sl.step(stp)
    headers = { 
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'es-ES,es;q=0.9',
            'cache-control':'max-age=0',
            # 'cookie':'_ga=GA1.2.1426512509.1679648492; _gid=GA1.2.1920613820.1683095987; __RequestVerificationToken=AvpGVGv1g9mBl0Onc7eUlLn_AtjyKncfvBJTo7mmfk0UWlgGq4ZiybRnCl2fLynd2evb_65Z7RIz3r5SpFs0blcDz8w1; SCV=SID=02; _gat=1',
            'sec-ch-ua':'"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    data='''8A5R96S8kHWcVRx_zJaIS0r_yAeHljEkKeMtO5uR7f01'''
    req =requests.get(url=web, data=data, headers=headers)
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ["https://superpapelera.sherlockhr.computrabajo.com{0}".format(x.get('url', '')) for x in sl.M]

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
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
        ad['url'] = offer.get("@url", "")
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()