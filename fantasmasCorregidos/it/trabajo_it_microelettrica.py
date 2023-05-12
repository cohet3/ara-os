# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
import libnacho
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'microelettrica.com'

xtr = '''title
<h1.*?>
</h1>
description
text&q;:&q;&l;p kb-paragraph&g;
&l;/li&g;&l;/ul&g;&l;p kb-paragraph&g;&l;/p&g;&l;p kb-paragraph&g;&l;
company
contact&q;:&q;&l;p kb-paragraph&g;

city
S.p.A.&l;br&g;
&l;br&g;Phone'''

xtr_url = '''url
<li> <a href="
"'''

stp = 'AAA'
page_ads = 21 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.microelettrica.com/en/jobs-and-career/content-page-57.json',
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
    #sl.step(stp)

    req = requests.get(url = web, verify = False)
    datos = req.text
    #print datos
    #exit(0)
    
    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://www.microelettrica.com{0}".format(x.get("url", "")) for x in sl.M if not 'jobsrozzano' in x.get("url","")]
    sl.WR = list(dict.fromkeys(sl.WR))

    # Para pruebas
    #sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    #exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = libnacho.xhtml(re.sub("&l;|/li&g;|&l;|li&g;|/strong&g;|/p&g;|ul kb-list&g;|a;amp;|&q;|},&q;|component&q;|:&q;|page-intro&q;|},{&q;|anchor&q;|:&q;|copy-text&q;|,&q;|attributes&q;|:{&q;|content&q;|:&q;|p kb-paragraph&g;|strong&g;","", offer.get("description", "")).decode('unicode-escape').encode('UTF-8'))
        ad['url'] = offer.get("@url", "")
        ad['city'] = re.sub("&l;br&g;", "" , offer.get("city", ""))
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
