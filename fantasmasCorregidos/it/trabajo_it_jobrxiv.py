# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests 
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
#from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'jobrxiv.org'

xtr = '''title
<title>
</title>
description
<div class="job_description">
<ul class="share-post">
city
<i class="fa fa-money"></i>
</span>'''

xtr_url = '''url
<a href=\\\\"https:\\\\/\\\\/jobrxiv.org\\\\/job
\\\\/\\\\"'''

stp = 'AAA'
page_ads =11 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://jobrxiv.org/jm-ajax/get_listings/',
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
        'accept':'*/*',
        'accept-encoding':'gzip, deflate',
        'accept-language':'es-ES,es;q=0.9',
        'content-length':'2155',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        #'cookie':'_ga=GA1.2.622130106.1622559104; _gid=GA1.2.473596082.1622559104',
        'origin':'https://jobrxiv.org',
        'referer':'https://jobrxiv.org/?job_region=27647',
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile':'?0',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
    }

    data = '''lang=&search_keywords=&search_location=&per_page=25&orderby=date&order=DESC&page=1&featured=&filled=&data_params%5Bper_page%5D=25&data_params%5Borderby%5D=date&data_params%5Border%5D=DESC&data_params%5Bfeatured%5D=&data_params%5Bfilled%5D=&data_params%5Bjob_types%5D=&data_params%5Bwpjmsf_enabled%5D=1&data_params%5Bpost_id%5D=201&data_params%5BdisableFormStateStorage%5D=&data_params%5Bcategories%5D=&data_params%5Blist_layout%5D=list&data_params%5Bshow_pagination%5D=false&data_params%5Bshow_filters%5D=false&data_params%5Bkeywords%5D=&data_params%5Blocation%5D=&show_pagination=false&wpjmsf_fields%5Bjob_types%5D%5B%5D=full-time&wpjmsf_fields%5Bjob_types%5D%5B%5D=part-time&wpjmsf_fields%5Bjob_region%5D%5B%5D=27647&wpjmsf_fields%5Bsearch_keywords%5D=&wpjmsf_fields%5Bsalary_min%5D=&wpjmsf_fields%5Borderby%5D=date&wpjmsf_taxonomies%5Bjob_region%5D=job_listing_region&wpjmsf_taxonomies%5Bjob_tags%5D=job_listing_tag&wpjmsf_taxonomies%5Bjob_category%5D=job_listing_category&wpjmsf_taxonomies%5Bjob_type%5D=job_listing_type&wpjmsf_config%5Bjob_types%5D%5Bcompare%5D=&wpjmsf_config%5Bjob_types%5D%5Bcompare_relation%5D=&wpjmsf_config%5Bsearch_categories%5D%5Bcompare%5D=&wpjmsf_config%5Bsearch_categories%5D%5Bcompare_relation%5D=&wpjmsf_config%5Bjob_region%5D%5Bcompare%5D=&wpjmsf_config%5Bjob_region%5D%5Bcompare_relation%5D=&wpjmsf_config%5Bjob_tags%5D%5Bcompare%5D=&wpjmsf_config%5Bjob_tags%5D%5Bcompare_relation%5D=&wpjmsf_config%5Bsearch_keywords%5D%5Bcompare%5D=&wpjmsf_config%5Bsearch_keywords%5D%5Bcompare_relation%5D=&wpjmsf_config%5Bsalary_min%5D%5Bcompare%5D=&wpjmsf_config%5Bsalary_min%5D%5Bcompare_relation%5D=&wpjmsf_config%5Binit%5D=true&wpjmsf_auto_updates%5Bjob_tags%5D%5Btaxonomy%5D=job_listing_tag&wpjmsf_auto_updates%5Bjob_tags%5D%5Bshow_count%5D=0&wpjmsf_auto_updates%5Bjob_tags%5D%5Bsmallest%5D=1&wpjmsf_auto_updates%5Bjob_tags%5D%5Blargest%5D=2&wpjmsf_auto_updates%5Bjob_tags%5D%5Bunit%5D=em&wpjmsf_auto_updates%5Bjob_tags%5D%5Bnumber%5D=25&wpjmsf_auto_updates%5Bjob_tags%5D%5Bformat%5D=flat&wpjmsf_auto_updates%5Bjob_tags%5D%5Borderby%5D=count&wpjmsf_auto_updates%5Bjob_tags%5D%5Border%5D=DESC&wpjmsf_auto_updates%5Bjob_tags%5D%5Bseparator%5D=&wpjmsf_auto_updates%5Bjob_tags%5D%5Btype%5D=eui_multiselect&form_data=job_types%255B%255D%3Dfull-time%26job_types%255B%255D%3Dpart-time%26search_keywords%3D%26salary_min%3D&filter_job_type%5B%5D=full-time&filter_job_type%5B%5D=part-time'''
    
    req = requests.post(url = web, headers = headers, data = data, verify = False)
    datos = req.text
    # print datos
    # exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_url)
    sl.WR = ["https://jobrxiv.org/job{0}".format(x.get("url", "")) for x in sl.M]

    urls = []
    
    for url in sl.WR:
        urls.append(re.sub("\\\\","",url))
    sl.WR = urls
    
    # Para pruebas
    sl.printWR()
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

        ad['title'] = re.sub(" - jobRxiv","",offer.get("title", ""))
        ad['description'] = offer.get("description", "")
        ad['url'] = offer.get("@url", "")
        ad['city'] = re.sub("Italy ","",offer.get("city", ""))
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
