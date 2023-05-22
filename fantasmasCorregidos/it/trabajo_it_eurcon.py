# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'eurcon.it'

xtr = '''title
<title>
(\||</title>)
description
<div class="et_pb_text_inner"><p>
</ul>
city
<span style="font-size: 18px;">Il luogo di lavoro è
e provincia'''

xtr_url='''url
<h2 class="entry-title"><a href="
"''' 

stp = ''
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'http://www.eurcon.it/lavora-con-noi/',
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

    sl.extract(xtr_url)
    sl.WR = ["{0}".format(x.get("url", "")) for x in sl.M]
    # Para pruebas
    sl.printWR()
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
        ad['description'] = re.sub("\\\\", "", re.sub("Â", "", re.sub("Ã¡", "á",re.sub("Ã©", "é", re.sub("Ã­", "í",re.sub("Ã³", "ó",re.sub("Ãº", "ú",re.sub("Ã", "Á", re.sub("Ã", "É",re.sub("Ã", "Í", re.sub("Ã±", "ñ", re.sub("Ã", "Ñ", re.sub("Ã", "Ö", re.sub("Ã", "Ü", re.sub("Ã¼", "ü", re.sub("â", "", re.sub("â|â", " - ", re.sub("â¦", "...", re.sub("â", "\"", re.sub("â", "\"", re.sub("â", "'", re.sub("â¢", "·", offer.get("description", "").decode("unicode-escape").encode("utf-8")))))))))))))))))))))))
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
