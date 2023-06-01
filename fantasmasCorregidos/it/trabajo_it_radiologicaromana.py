# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'radiologicaromana.it'

xtr = '''title
"validThrough":".*?","title":"
","description":"
description

",
city
"address":"
"'''

xtr_url = '''url
<a href=\\\\"https:\\\\/\\\\/www.radiologicaromana.it\\\\/offerta-lavoro\\\\/
\\\\/\\\\">'''

stp = '/offerta-lavoro/'
page_ads = 11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            #'https://www.radiologicaromana.it/lavora-con-noi/',
            'https://www.radiologicaromana.it/jm-ajax/get_listings/',
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

    headers = {
        "accept":"*/*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"es-ES,es;q=0.9",
        "content-length":"574",
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        #"cookie":"customerly_jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImp0aSI6IjI0OGI0ZmUyLTBlZmYtMTFlYi05ODVlLTAyZWIzNzE5YzAzNSJ9.eyJpc3MiOiJodHRwczpcL1wvY3VzdG9tZXJseS5pbyIsImp0aSI6IjI0OGI0ZmUyLTBlZmYtMTFlYi05ODVlLTAyZWIzNzE5YzAzNSIsImlhdCI6MTYwMjc3NzQ1NSwibmJmIjoxNjAyNzc3NDU1LCJleHAiOjI1ODAzOTM0NTUsInR5cGUiOjEsImFwcCI6IjhiYTg0Y2I2IiwiaWQiOm51bGx9.AbxvbEVD40pEhfHZJJzTzUfTjZ4ap_W1BhwPkl2CWiE",
        "origin":"https://www.radiologicaromana.it",
        "referer":"https://www.radiologicaromana.it/lavora-con-noi/",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        "x-requested-with":"XMLHttpRequest",
    }

    for x in xrange(1, 2):
        data = '''lang=&search_keywords=&search_location=&filter_job_type%5B%5D=freelance&filter_job_type%5B%5D=full-time&filter_job_type%5B%5D=internship&filter_job_type%5B%5D=part-time&filter_job_type%5B%5D=temporary&filter_job_type%5B%5D=&per_page=10&orderby=featured&order=DESC&page={0}&show_pagination=false&form_data=search_keywords%3D%26search_location%3D%26filter_job_type%255B%255D%3Dfreelance%26filter_job_type%255B%255D%3Dfull-time%26filter_job_type%255B%255D%3Dinternship%26filter_job_type%255B%255D%3Dpart-time%26filter_job_type%255B%255D%3Dtemporary%26filter_job_type%255B%255D%3D'''.format(x)

        req = requests.post(url=web, headers=headers, data=data, verify = False)
        datos = req.text
        sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
        sl.extract(xtr_url)
        sl.WR = ["https://www.radiologicaromana.it/offerta-lavoro/{0}".format(x.get("url","")) for x in sl.M]

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
            ad['description'] = re.sub("\\\\","",re.sub("\\\\n|\\\\r|\\\\t","", offer.get("description", "")))
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
