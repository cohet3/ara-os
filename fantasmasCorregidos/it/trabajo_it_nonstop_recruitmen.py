# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'nonstop-recruitment.com'

xtr = '''title
<title>
</title>
description
<div class="job_description">
<div class="job_application application">'''

xtr_url = '''url
<a href=\\\\"https:\\\\/\\\\/nonstopconsulting.com\\\\/job\\\\/
"'''

stp = '/job/'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 6))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'action=KAajax_getjoblist&jobindustry=0&consultant=&jobcat=&jobtype=&texttosearch=&minsal=0&maxsal=1000000&maxavsal=1000000&salstep=5&showjobswithoutsalary=true&dist=50&avdist=50&diststep=1&showjobswithoutlocation=true&geolocation_drd=&pos_lat=0&pos_long=0&north_lat=90&south_lat=-90&west_long=-180&east_long=180&kk=1379855795&KA_isTest=false&KA_IsShowTestJobs=false&attributeitem1=0&attributeitem2=19839&attributeitem3=0&attributeitem4=0&attributeitem5=0&attributeitem6=0&pagenumber={page}&KA_ajaxCallChecker=1379855795&KA_currPage=https%3A%2F%2Fnonstopconsulting.com%2Fen%2Fvacancies%2F&KA_needSearchLink=false',
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

    headers= {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate',
        'accept-language':'es-ES,es;q=0.9',
        'content-length':'606',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie':'pll_language=en; _ga=GA1.2.493478861.1637134003; _fbp=fb.1.1637134003293.33043075; _hjid=042ce03f-9194-4fce-996d-4f6b36594a52; _hjSessionUser_1755429=eyJpZCI6ImJlZmYzMjg0LWJmODAtNTQxZC04NDhkLWExMmUwMmE0NmVkZiIsImNyZWF0ZWQiOjE2MzkwNTIxMjMzMTMsImV4aXN0aW5nIjp0cnVlfQ==; PHPSESSID=svr26pi9i51svmfo6auvsg8bt1; _gid=GA1.2.265742761.1639983847; _gat_UA-102334815-1=1; _hjSession_1755429=eyJpZCI6ImI4MTk4MTllLTBjMmItNGQwMy1hNzg2LWYxZTFiOTc3YmI0MSIsImNyZWF0ZWQiOjE2Mzk5ODM4NDcwOTR9; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0',
        'origin':'https://nonstopconsulting.com',
        'referer':'https://nonstopconsulting.com/en/vacancies/',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
    }
    req = requests.post(url="https://nonstopconsulting.com/jm-ajax/get_listings", headers=headers, data=web)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://nonstopconsulting.com/job/{0}".format(re.sub("\\\\","",x.get("url", ""))) for x in sl.M]
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
