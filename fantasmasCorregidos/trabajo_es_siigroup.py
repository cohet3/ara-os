# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_es import db_es, slavy, text, dalek
import libnacho

# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'sii-group.es'

xtr = '''title
"title":"
",
description
"description":"
","
contract
employmentType":\["
"\],
city
"address":"
"'''

xtr_url = '''url
<a href=\\\\"https:\\\\/\\\\/siigroup-spain.com\\\\/trabajo\\\\
\\\\/\\\\">'''

stp = '/job/'
page_ads = 10
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'lang=es&search_keywords=&search_location=&filter_job_type%5B%5D=asturias&filter_job_type%5B%5D=barcelona&filter_job_type%5B%5D=illes-balears&filter_job_type%5B%5D=madrid&filter_job_type%5B%5D=remoto&filter_job_type%5B%5D=valencia&filter_job_type%5B%5D=&per_page=10&orderby=featured&order=DESC&page=2&show_pagination=false&form_data=search_keywords%3D%26search_location%3D%26filter_job_type%255B%255D%3Dasturias%26filter_job_type%255B%255D%3Dbarcelona%26filter_job_type%255B%255D%3Dilles-balears%26filter_job_type%255B%255D%3Dmadrid%26filter_job_type%255B%255D%3Dremoto%26filter_job_type%255B%255D%3Dvalencia%26filter_job_type%255B%255D%3D',
        )
    }
     ),
)


def crawl(web):
    

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'505',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie':'_gid=GA1.2.1179970151.1682405884; cookiehub=eyJhbnN3ZXJlZCI6dHJ1ZSwicHJlY29uc2VudCI6ZmFsc2UsInJldmlzaW9uIjoxLCJkbnQiOmZhbHNlLCJjb29raWVMYXdzIjp0cnVlLCJ0b2tlbiI6IiIsInRpbWVzdGFtcCI6IjIwMjMtMDQtMjVUMDY6NTg6MDkuNjk4WiIsImNhdGVnb3JpZXMiOlt7ImNpZCI6MSwiaWQiOiJuZWNlc3NhcnkiLCJ2YWx1ZSI6dHJ1ZSwicHJlY29uc2VudCI6ZmFsc2UsImZpcmVkIjp0cnVlfSx7ImNpZCI6MywiaWQiOiJhbmFseXRpY3MiLCJ2YWx1ZSI6dHJ1ZSwicHJlY29uc2VudCI6ZmFsc2UsImZpcmVkIjpmYWxzZX0seyJjaWQiOjQsImlkIjoibWFya2V0aW5nIiwidmFsdWUiOnRydWUsInByZWNvbnNlbnQiOmZhbHNlLCJmaXJlZCI6ZmFsc2V9XX0=; _ga_V6BKGDKVCR=GS1.1.1682405884.1.1.1682405996.0.0.0; _ga_Q4SHRR9HGM=GS1.1.1682405884.1.1.1682405996.0.0.0; _ga=GA1.1.1769501310.1682405884',
        'Host':'siigroup-spain.com',
        'Origin':'https://siigroup-spain.com',
        'Referer':'https://siigroup-spain.com/ofertas-de-empleo/',
        'sec-ch-ua':'"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }
    data = '''lang=es&search_keywords=&search_location=&filter_job_type%5B%5D=barcelona&filter_job_type%5B%5D=madrid&filter_job_type%5B%5D=remoto&filter_job_type%5B%5D=valencia&filter_job_type%5B%5D=&per_page=10&orderby=featured&order=DESC&page=1&remote_position=&show_pagination=false&form_data=search_keywords%3D%26search_location%3D%26filter_job_type%255B%255D%3Dbarcelona%26filter_job_type%255B%255D%3Dmadrid%26filter_job_type%255B%255D%3Dremoto%26filter_job_type%255B%255D%3Dvalencia%26filter_job_type%255B%255D%3D'''
    req = requests.post(url='https://siigroup-spain.com/jm-ajax/get_listings/', data=data, headers=headers)
    
    html = req.text
    # print html
    # exit(0)
    sl.WR = ['virtual:{0}'.format(html.encode('utf-8'))]
    sl.extract(xtr_url)
    sl.WR = ["https://siigroup-spain.com/trabajo{0}/".format(x.get("url", "")) for x in sl.M]

    # Para pruebas
    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:10]
    # exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.headers = {}
    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                  published_at='')

        ad['title'] = re.sub("\\\\","",offer.get("title", "").decode("unicode-escape").encode("utf-8"))
        ad['description'] = libnacho.emojis(re.sub("\\\\","",re.sub("\[.*?\]","",offer.get("description", "")).decode("unicode-escape").encode("utf-8")))
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "").decode("unicode-escape").encode("utf-8")
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
