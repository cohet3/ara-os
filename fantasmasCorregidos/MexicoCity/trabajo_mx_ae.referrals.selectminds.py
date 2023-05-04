# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_mx import db_es, slavy, text, dalek
import libnacho
# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'ae.referrals.selectminds.com'

xtr = '''title
<h1 class="title">
</h1>
extra
<span class="loc_icon entypo">&#128269;

city
</span>
</a>
description
<div class="job_description">
<div id="jJobInsideInfo"'''

xtr_token = '''token
id = "tsstoken" value ="
"'''

xtr_searchID = '''searchID
JobSearch.id":
\}'''

xtr_url = '''url
<a href=\\\\"https://ae.referrals.selectminds.com/jobs/
\\\\"'''

stp = 'AAA'
page_ads = 21
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://ae.referrals.selectminds.com/',
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
    sl.extract(xtr_token)

    token = '{0}'.format(sl.M[0].get('token', ''))

    cookies = ''
    for cookie in sl.cookies:
        #print repr(cookie)
        nombre = re.search('(?:name=\')(?P<select>\S+)(?:\',)', repr(cookie)).group('select')
        valor = re.search('(?:value=\')(?P<select>\S+)(?:\',)', repr(cookie)).group('select')
        cookies = cookies + nombre + '=' + valor + '; '

    # print token
    # print cookies
    # exit(0)

#################POST################# realiza búsqueda y saca jobSearchID
    headers= {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'202',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':cookies,
        'Host':'ae.referrals.selectminds.com',
        'Origin':'https://ae.referrals.selectminds.com',
        'Referer':'https://ae.referrals.selectminds.com/',
        'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile':'?0',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'tss-token':token,
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
    }
    
    # Data para trabajos de España
    # data ='''keywords=&geo_location=Spain&geo_lat=40.4203&geo_long=-3.70577&geo_level=country&geo_area_id=20215059&geo_region_area_id=&geo_country_area_id=20215059&geo_search_radius_units=km&geo_search_radius_km=150'''
    
    # Data para trabajos de Italia
    # data ='''keywords=&geo_location=Italy&geo_lat=41.90305&geo_long=12.4958&geo_search_radius_km=150&geo_search_radius_units=km&geo_level=country&geo_area_id=20110484&geo_region_area_id=&geo_country_area_id=20110484'''
    
    # Data para trabajos de Chile
    # data ='''keywords=&geo_location=Chile&geo_lat=-33.43721&geo_long=-70.65002&geo_search_radius_km=150&geo_search_radius_units=km&geo_level=country&geo_area_id=23488354&geo_country_area_id=23488354'''
    
    # Data para trabajos de Brasil
    # data = '''keywords=&geo_location=Brazil&geo_lat=-15.77839&geo_long=-47.92863&geo_search_radius_km=150&geo_search_radius_units=km&geo_level=country&geo_area_id=23028911&geo_country_area_id=23028911'''
    
    # Data para trabajos de Portugal
    # data = '''keywords=&geo_location=Portugal&geo_lat=38.72572&geo_long=-9.15025&geo_search_radius_km=150&geo_search_radius_units=km&geo_level=country&geo_area_id=20317122&geo_country_area_id=20317122'''

    # Data para trabajos en Mexico
    data = '''keywords=&geo_location=M%C3%A9xico&geo_lat=19.43196&geo_long=-99.13316&geo_level=country&geo_area_id=22000493&geo_region_area_id=&geo_country_area_id=22000493&geo_search_radius_units=mi&geo_search_radius_km=40.25'''
    
    req = requests.post(url = 'https://ae.referrals.selectminds.com/ajax/jobs/search/create', headers = headers, data = data)
    datos = req.text
    #print datos
    #exit(0)

    sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

    sl.extract(xtr_searchID)
    searchID = "{0}".format(sl.M[0].get("searchID", ""))
    # print searchID
    # exit(0)

    # Usar solo si el país tiene paginación
    for page in xrange(1,4):
    #################POST################# Obtiene los resuldados de la búsqueda anterior para sacar las urls
        headers= {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'es-ES,es;q=0.9,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'0',
            'Cookie':cookies,
            'Host':'ae.referrals.selectminds.com',
            'Origin':'https://ae.referrals.selectminds.com',
            'Referer':'https://ae.referrals.selectminds.com/',
            'sec-ch-ua':'" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            'sec-ch-ua-mobile':'?0',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
            'tss-token':token,
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
        }
        data ='''JobSearch.id=''' + searchID + '''&page_index=''' + str(page) + '''&site-name=default906&include_site=true'''
        urlResults = 'https://ae.referrals.selectminds.com/ajax/content/job_results?JobSearch.id={0}&page_index={1}&site-name=default906&include_site=true'.format(searchID, page)
        req = requests.post(url = urlResults, headers = headers, data = data)
        datos = req.text
        # print datos
        # exit(0)

        sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

        sl.extract(xtr_url)
        sl.WR = ["https://ae.referrals.selectminds.com/jobs/{0}".format(x.get("url", "")) for x in sl.M]

        # Para pruebas
        # sl.printWR()
        # sl.printM()
        # sl.printstatus()
        # sl.WR = sl.WR[0:5]
        # continue
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
            ad['description'] = offer.get("description", "")
            ad['url'] = offer.get("@url", "")
            ad['city'] = libnacho.emojis(offer.get("city", ""))
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
