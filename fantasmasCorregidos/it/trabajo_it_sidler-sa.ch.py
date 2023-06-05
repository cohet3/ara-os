# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'sidler-sa.ch'

xtr = '''title
<title>
</title>
extra
<span class="text-description">Location</span>

city
<strong class="small-heading">
</strong>
description
<div class="content-single">
<div class="author-single">'''

xtr_url='''url
"><a href=\\\\"https:\\\\/\\\\/www.sidler-sa.ch\\\\/en\\\\/offerta-lavoro\\\\
"'''

stp = '/en/ -privacy -cookie -node -applicant -faq -contacts'
page_ads =25 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.sidler-sa.ch/en/jm-ajax/get_listings/',
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
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9',
            'Connection':'keep-alive',
            'Content-Length':'218',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie':'_gid=GA1.2.791850736.1685972113; _gat_gtag_UA_19175144_1=1; wp-wpml_current_language=en; _ga_YJV3BGM0XP=GS1.1.1685972112.1.1.1685972157.0.0.0; _ga_507KXD4B8B=GS1.1.1685972112.1.1.1685972157.0.0.0; _ga=GA1.2.190039718.1685972113'
            'Host':'www.sidler-sa.ch',
            'Origin':'https://www.sidler-sa.ch',
            'Referer':'https://www.sidler-sa.ch/en/job-offers',
            'Sec-Ch-Ua':'"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
    }
    data='''lang=en&search_keywords=&search_location=&search_categories%5B%5D=&per_page=20&orderby=featured&order=DESC&page=1&show_pagination=false&form_data=search_categories%255B%255D%3D%26search_location%3D%26search_keywords%3D'''
   
    req =requests.post(url=web, data=data, headers=headers)
    datos = req.text
    # print (datos)
    # exit(0)

    sl.WR = ['virtual:{0}'.format(datos.encode('utf-8'))]
    
    sl.extract(xtr_url)
    sl.WR = ["https://www.sidler-sa.ch/en/offerta-lavoro{0}".format(x.get('url', '')) for x in sl.M]


    # Para pruebas
    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    #sl.WR = sl.WR[0:5]
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
