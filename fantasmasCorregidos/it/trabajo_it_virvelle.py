# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'virvelle.com'

xtr = '''title
<h1 class="big-title" itemprop="title">
</h1>
description
<div class="paragrafo" itemprop="description" style="padding-top:0;">
<div class="row">
city
span class="svg-icon svg-baseline label-box" itemprop="addressLocality">Luogo:
</span>'''

stp = '/offerte-di-lavoro/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 3))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.virvelle.com/wp-admin/admin-ajax.php?id=&post_id=offerte_lavoro&slug=offerte_lavoro&canonical_url=https%3A%2F%2Fwww.virvelle.com%2Fengage%2Fofferte-di-lavoro%2F&posts_per_page=9&page=0&offset=0&post_type=offerte_lavoro&repeater=template_1&seo_start_page={page}&preloaded=false&preloaded_amount=0&order=DESC&orderby=date&action=alm_get_posts&query_type=standard',
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
    "accept":"application/json, text/plain, */*",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
    # "cookie":"_ga=GA1.2.1997351028.1599211513; _gid=GA1.2.822366223.1599211513; _iub_cs-92165399=%7B%22consent%22%3Atrue%2C%22timestamp%22%3A%222020-09-04T10%3A09%3A43.087Z%22%2C%22version%22%3A%221.2.4%22%2C%22id%22%3A92165399%7D",
    "referer":"https://www.virvelle.com/engage/offerte-di-lavoro/",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    }
    req =requests.post(url =web, headers= headers, data="id=&post_id=offerte_lavoro&slug=offerte_lavoro&canonical_url=https%3A%2F%2Fwww.virvelle.com%2Fengage%2Fofferte-di-lavoro%2F&posts_per_page=9&page=0&offset=0&post_type=offerte_lavoro&repeater=template_1&seo_start_page=1&preloaded=false&preloaded_amount=0&order=DESC&orderby=date&action=alm_get_posts&query_type=standard", verify = False)
    data =req.json()["html"]
    sl.WR = ["virtual:{0}".format(data.encode("utf-8"))]
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
        ad['description'] = re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", ""))
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

