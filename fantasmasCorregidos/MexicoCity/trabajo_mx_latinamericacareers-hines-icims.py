# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek, torproxy
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'latinamericacareers-hines.icims.com'

xtr = '''company
"Organization","name":"
",
city
"addressLocality":"
",
province
"addressRegion":"
",
contract
"employmentType":"
",
description
"description":"
","
title
"title":"
",'''

xtr_url = '''url
<a href="https://latinamericacareers-hines.icims.com/jobs/
"'''

stp = '/jobs/'
page_ads = 11

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
#with Controller.from_port(port = 9051) as controller:
    #pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://latinamericacareers-hines.icims.com/jobs/search?ss=1&in_iframe=1&searchLocation=13400--' ,
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
    #sl.step(stp)

    headers = {
        "accept":"application/json, text/plain, */*",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"es-ES,es;q=0.9",
        "content-length":"145",
        "content-type":"application/json;charset=UTF-8",
        #"cookie":"AMCV_A717776A5245B1250A490D44%40AdobeOrg=-1891778711%7CMCIDTS%7C18516%7CMCMID%7C68545847003421113601231717201633185181%7CMCAAMLH-1600338446%7C6%7CMCAAMB-1600338446%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1599740846s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C2.4.0; _ga=GA1.2.1997958143.1599733647; _gcl_au=1.1.1126614976.1599733647; mbox=session#e62a547df0bc4d83a194ddcb5e0ef4c5#1599735863|PC#e62a547df0bc4d83a194ddcb5e0ef4c5.37_0#1662978803; s_nr=1599734002637-New; _fbp=fb.1.1599748943381.1951810567; mousestats_vi=911584c6e163b0b97750; _mkto_trk=id:992-TVA-391&token:_mch-icims.com-1599748943391-36777; LPVID=c0M2YxNjNkY2Q4OWYyZjcw; AMCV_88CA58E65A265B560A495E1E%40AdobeOrg=1075005958%7CMCIDTS%7C18529%7CMCMID%7C70028511826290103040896134862736848821%7CMCOPTOUT-1600884030s%7CNONE%7CvVersion%7C4.4.1; AMCV_945D02BE532957400A490D4C%40AdobeOrg=870038026%7CMCIDTS%7C18541%7CMCMID%7C67808484560413944440213656476478362890%7CMCAID%7CNONE%7CMCOPTOUT-1601912544s%7CNONE%7CvVersion%7C5.0.0; rh_omni_tc=701f2000001Css0AAC; JSESSIONID=B3D347FDEB01B81737F5C23C952F80FE; cookie_icims_iframe_content_height=1655; icimsCookiesEnabledCheck=1; jsEnabled=true",
        "origin":"https://latinamericacareers-hines.icims.com",
        "referer":"https://latinamericacareers-hines.icims.com/jobs/search?ics_geolocation=Mexico+City%2C+MX&in_iframe=1",
        "search-engine-provider":"google",
        "sec-fetch-dest":"empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "x-newrelic-id":"UQMFUFdUGwcCVFdTBAc=",
    }

    data = '''{"fields":["title","url","postDate","category","locations","description"],"filters":{"zipRadius":25,"locations":[{"address":"Mexico City, MX"}]}}'''

    # req = requests.post(url=web, headers=headers, data=data)
    req = requests.get(url=web)
    datos = req.text
    # print datos
    # exit(0)
    sl.WR = ["virtual:{0}".format(datos.encode("utf-8"))]
    sl.extract(xtr_url)
    sl.WR = ["https://latinamericacareers-hines.icims.com/jobs/{0}".format(x.get("url","")) for x in sl.M]
    urls = []
    for url in sl.WR:
        if not 'login' in url:
            urls.append(url)
    sl.WR = urls
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
        ad['description'] = re.sub("\\\\", "", re.sub("Â", "", re.sub("Ã¡", "á",re.sub("Ã©", "é", re.sub("Ã­", "í",re.sub("Ã³", "ó",re.sub("Ãº", "ú",re.sub("Ã", "Á", re.sub("Ã", "É",re.sub("Ã", "Í", re.sub("Ã±", "ñ", re.sub("Ã", "Ñ", re.sub("Ã", "Ö", re.sub("Ã", "Ü", re.sub("Ã¼", "ü", re.sub("â", "", re.sub("â|â", " - ", re.sub("â¦", "...", re.sub("â", "\"", re.sub("â", "\"", re.sub("â", "'", re.sub("â¢", "·", offer.get("description", "").decode("unicode-escape").encode("utf-8")))))))))))))))))))))))
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
