# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'jobsearch.serco.eu'

xtr = '''title
<h1 class="job_title">
</h1>
description
<div class="main">
<div class="sidebar">
extra
<i class="far far fa-map-marker-alt"></i>

city
<td>
</td>'''

stp = '/job/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://jobsearch.serco.eu/jobs/search',
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
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"es-ES,es;q=0.9,en;q=0.8,pt;q=0.7",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Length":"142",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"youWantTheCookieShown=https%3A%2F%2Fjobsearch.serco.eu%2F; _pk_ses.35.36e9=*; youWantTheCookie=yes; _pk_id.35.36e9=aed7f5347dbf3cb3.1597061322.1.1597061613.1597061322.; ci_session=a%3A8%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22ff7150db05a2f36292758262fcc596a2%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A14%3A%22139.47.106.235%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A115%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F84.0.4147.105+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1597061634%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3Bs%3A4%3A%22lang%22%3Bs%3A2%3A%22en%22%3Bs%3A20%3A%22disable_content_wrap%22%3Bb%3A0%3Bs%3A6%3A%22inputs%22%3Ba%3A11%3A%7Bs%3A8%3A%22keywords%22%3Bs%3A24%3A%22%28e.g.+job+title%2C+skills%29%22%3Bs%3A7%3A%22country%22%3Bs%3A3%3A%22109%22%3Bs%3A8%3A%22location%22%3Bs%3A33%3A%22%28e.g.+post%2Fzipcode%2C+region%2C+city%29%22%3Bs%3A8%3A%22distance%22%3Bs%3A0%3A%22%22%3Bs%3A8%3A%22category%22%3Bs%3A2%3A%22-1%22%3Bs%3A9%3A%22region_id%22%3Bs%3A0%3A%22%22%3Bs%3A13%3A%22custom_fields%22%3Bs%3A0%3A%22%22%3Bs%3A8%3A%22contract%22%3Bs%3A2%3A%22-1%22%3Bs%3A4%3A%22page%22%3Bs%3A1%3A%221%22%3Bs%3A11%3A%22is_internal%22%3Bs%3A0%3A%22%22%3Bs%3A8%3A%22is_event%22%3Bs%3A0%3A%22%22%3B%7D%7Db41cf329545178b632e8d04ff309df8e",
    "Host":"jobsearch.serco.eu",
    "Origin":"https://jobsearch.serco.eu",
    "Referer":"https://jobsearch.serco.eu/",
    "Sec-Fetch-Dest":"document",
    "Sec-Fetch-Mode":"navigate",
    "Sec-Fetch-Site":"same-origin",
    "Sec-Fetch-User":"?1",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    }
    req = requests.post(url=web, headers=headers, data="keywords=%28e.g.+job+title%2C+skills%29&country=109&location_geo=&location=%28e.g.+post%2Fzipcode%2C+region%2C+city%29&contract=-1&category=-1")
    data=req.text.encode("utf-8")
    sl.WR = ["virtual:{0}".format(data)]
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

