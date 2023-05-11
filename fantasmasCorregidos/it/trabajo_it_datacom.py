# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'datacom.uk.com'

xtr = '''title
<h1 class="page-title">
</h1>
description
<h2 class="job-overview-title">Job Description:</h2>
Application Form
city
target="_blank">
</a></div>'''

stp = '/job/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            '',
        )
    }
     ),
)



def crawl(web): 

    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    sl.step(stp)

    sl.headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'436',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie':'_ga=GA1.3.343542230.1570090556; _gid=GA1.3.441703186.1570090556; _gat=1',
        'Host':'datacom.uk.com',
        'Origin':'https://datacom.uk.com',
        'Referer':'https://datacom.uk.com/jobs',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.94',
        'X-Requested-With':'XMLHttpRequest',

    }

    req = requests.post(url='https://datacom.uk.com/jm-ajax/get_listings/', data='lang=&search_keywords=&search_location=Italy&filter_job_type%5B%5D=contract&filter_job_type%5B%5D=permanent&filter_job_type%5B%5D=temporary&filter_job_type%5B%5D=&per_page=10&orderby=featured&order=DESC&page=1&show_pagination=false&form_data=search_keywords%3D%26search_location%3DItaly%26filter_job_type%255B%255D%3Dcontract%26filter_job_type%255B%255D%3Dpermanent%26filter_job_type%255B%255D%3Dtemporary%26filter_job_type%255B%255D%3', headers=sl.headers, verify = False)

    resul = req.json()['html']
    sl.WR = ['virtual:{0}'.format(resul.encode('utf-8'))]

    sl.step(stp)

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
