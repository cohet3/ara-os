# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'consulmarche.com'

xtr = '''title
<h1 class="page-title">
</h1>
description
<div itemprop="description" class="job-overview col-md-12 col-sm-12">
<strong id="jmfe-label-job_location" class="jmfe-custom-field-label">
city
<div id="jmfe-custom-job_location" class="jmfe-custom-field ">
</div>'''

stp = '/offerta-lavoro/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'http://www.consulmarche.com/jm-ajax/get_listings/',
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
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
    "Connection":"keep-alive",
    "Content-Length":"1081",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie":"_ga=GA1.2.864403475.1599568483; _gid=GA1.2.342696018.1599568483; _gat=1",
    "Host":"www.consulmarche.com",
    "Origin":"http://www.consulmarche.com",
    "Referer":"http://www.consulmarche.com/opportunita-di-carriera/",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
    }
    req = requests.post(url=web, data="lang=&search_keywords=&search_location=&filter_job_type%5B%5D=acquisti-logistica&filter_job_type%5B%5D=amministrazione&filter_job_type%5B%5D=commerciale-marketing&filter_job_type%5B%5D=consulente&filter_job_type%5B%5D=edp&filter_job_type%5B%5D=manageriale&filter_job_type%5B%5D=neodiplomato-neolaureato&filter_job_type%5B%5D=personale&filter_job_type%5B%5D=produzione&filter_job_type%5B%5D=segreteria&filter_job_type%5B%5D=tecnica&filter_job_type%5B%5D=&per_page=20&orderby=featured&order=DESC&page=1&show_pagination=false&form_data=search_keywords%3D%26search_region%3D0%26filter_job_type%255B%255D%3Dacquisti-logistica%26filter_job_type%255B%255D%3Damministrazione%26filter_job_type%255B%255D%3Dcommerciale-marketing%26filter_job_type%255B%255D%3Dconsulente%26filter_job_type%255B%255D%3Dedp%26filter_job_type%255B%255D%3Dmanageriale%26filter_job_type%255B%255D%3Dneodiplomato-neolaureato%26filter_job_type%255B%255D%3Dpersonale%26filter_job_type%255B%255D%3Dproduzione%26filter_job_type%255B%255D%3Dsegreteria%26filter_job_type%255B%255D%3Dtecnica%26filter_job_type%255B%255D%3D", headers=headers)
    data = req.json()["html"]
    sl.WR = ["virtual:{0}".format(data.encode("utf-8"))]
    sl.step(stp)
    sl.WR = ["{0}".format(url) for url in sl.WR]
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

