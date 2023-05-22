# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'telmotor.it'

xtr = '''title
<title>
[-]
city
Area|area
</title>
description
<h1 class="elementor-heading-title elementor-size-default">
</section>'''

xtr_url='''url
data-column-clickable="https://www.telmotor.it/
/"'''

stp = 'AAA'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.telmotor.it/lavora-con-noi/',
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
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding':'gzip, deflate',
        'accept-language':'es-ES,es;q=0.9',
        'cache-control':'max-age=0',
        # 'cookie':'PHPSESSID=18554ce4a05ccff7de189889782f078e; _ga=GA1.2.1949233151.1630067405; _gid=GA1.2.154315102.1630067405; _iub_cs-31627254=%7B%22consent%22%3Atrue%2C%22timestamp%22%3A%222021-08-27T12%3A30%3A08.800Z%22%2C%22version%22%3A%221.32.0%22%2C%22id%22%3A31627254%7D; euconsent-v2=CPLmIwEPLmIwoB7ECBITBoCsAP_AAH_AAAAAILtf_X__bX9j-_59f_t0eY1P9_r_v-Qzjhfdt-8F2L_W_L0X42E7NF36pq4KuR4Eu3LBIQNlHMHUTUmwaokVrzPsak2Mr6NKJ7LEmnMZO2dYGHtPn91TuZKY7_78__fz3z-v_t___9f3r-3_3__5_X---_e_V399zLv9____39nN___9uCCgBJhqXkAXZljgybRpVCiBGFYSHQCgAooBhaJrABgcFOysAj1BCwAQmoCMCIEGIKMGAQACCQBIREBIAWCARAEQCAAEAKkBCAAiYBBYAWBgEAAoBoWIEUAQgSEGRwVHKYEBUi0UE9lYAlF3saYQhlvgRQKP6KjARrNECwMhIWDmOAJAS8AA; _iub_cs-31627254-granular=%7B%7D',
        'referer':'https://www.telmotor.it/',
        'sec-ch-ua':'"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile':'?0',
        'sec-fetch-dest':'document',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'same-origin',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    }
    req = requests.get(url = web, headers = headers, verify = False)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://www.telmotor.it/{0}".format(x.get("url", "")) for x in sl.M]
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