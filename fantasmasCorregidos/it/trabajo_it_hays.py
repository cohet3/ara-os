# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_it import db_it, slavy, text, dalek
import libnacho
#from pprint import pprint

# from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'hays.it'

xtr = '''title
"title":"
"
description
"description":"
","
contract
"employmentType":"
"
company
"name":"
"
city
"addressLocality":"
"
province
"addressRegion":"
"'''

xtr_url = '''url
"applicationUrl".*?:.*?"
"'''

nextPage = '''codPage
"nextPageToken":"
"'''

stp = '/Job/Detail/\w+'
page_ads = 30
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(1, 2))
# with Controller.from_port(port = 9051) as controller:
# pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            "MILANO", "ROMA", "TORINO", "BOLOGNA", "BERGAMO", "MONZA-BRIANZA", "MODENA", "ITALIA", "LOMBARDIA", "PADOVA", "PAVIA", "BRESCIA", "VENETO", "VARESE", "VERONA", "FIRENZE", "PIEMONTE", "COMO", "GENOVA", "LECCO", "VICENZA", "MANTOVA", "CUNEO", "EMILIA ROMAGNA", "LODI", "TOSCANA", "ALESSANDRIA", "NAPOLI", "REGGIO EMILIA", "VENEZIA", "NORD ITALIA", "RIMINI", "PIACENZA", "CAMPANIA", "RAVENNA", "LAZIO", "TRIESTE", "CREMONA", "NOVARA", "TREVIS",
        )
    }
     ),
)



# def renew():
# torproxy.renew(controller)
# torproxy.connect()
# print "mi ip: ",torproxy.show_my_ip()
def crawl(web):


    # sl hace peticiones y extrae ofertas
    # sl2 solo se usa para extraer las urls
    sl = slavy.slavy()
    sl.start(web)
    #sl2.start(web)
    sl.metaExtract = True

    headers= {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-ES,es;q=0.9',
        'activityurl':'/ricerca-offerte?q=&location=&specialismId=&subSpecialismId=&locationf=&industryf=&sortType=0&jobType=-1&flexiWorkType=-1&payTypefacet=-1&minPay=-1&maxPay=-1&jobSource=HaysGCJ&searchPageTitle=Offerte%20di%20lavoro%20in%20Italia%20%7C%20Hays%20Recruitment%20Italia&searchPageDesc=Sei%20alla%20ricerca%20di%20un%20nuovo%20lavoro%20in%20Italia%3F%20Hays%20Recruitment%20pu%C3%B2%20aiutarti%20a%20trovare%20il%20ruolo%20perfetto.%20Scopri%20le%20nostre%20ultime%20offerte%20di%20lavoro%20in%20Italia%20e%20candidati%20oggi%20stesso!',
        'Authorization':'Bearer eyJhbGciOiJIUzUxMiJ9.eyJndWlkIjoiY2RiODJhYmQtMjE5Ni00M2I2LWFlMWMtNzlmYTVhNmRmNDlhIiwiZG9tYWluTmFtZSI6Iml0bCIsInN1YiI6ImNkYjgyYWJkLTIxOTYtNDNiNi1hZTFjLTc5ZmE1YTZkZjQ5YSIsImlhdCI6MTY3MTc4NDkzMiwibmJmIjoxNjcxNzg0OTMyLCJhdWQiOiJodHRwczovL3d3dy5oYXlzLml0LyIsImlzcyI6Imh0dHBzOi8vbS5oYXlzLmNvbSIsImV4cCI6MTcwMjg4ODkzMn0.2SR0VyKrpX6dLPtE_h2huAIeKm8K8kJfVh8b1GAKpJOgyT-CRtDq5l65tNOeemXKV_uY_0S_8m-G64n7jDLQ-g',
        'cache-control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':'650',
        'Content-Type':'application/json',
        'Host':'mapi.hays.com',
        'Origin':'https://www.hays.it',
        'Referer':'https://www.hays.it/',
        'sec-ch-ua':'"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'cross-site',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-auth':'aDX5UzaKVndUKKfP:eZ3lPmjX8gl3zqVg63Tih3cOC/2+BOy4RBlitihsp0Y=',
        'x-date':'2022-12-23T09:42:21+0100',
        'x-session':'cc5cef3b-ada1-40ed-9864-bf69dd18a6ee',
    }
    x = 0
    repite = True
    while repite:
        if x == 0:
            #data ='''{"facetLocation":"","flexibleWorking":"false","fullTime":"false","industry":"","isSponsored":false,"jobType":"","partTime":"false","query":"","locations":"BARCELONA","salMax":"","salMin":"","sortType":"RELEVANCE_DESC","specialismId":"","subSpecialismId":"","typeOnlyFilter":"","userAgent":"-Desktop","radius":100,"isCrossCountry":false,"isResponseCountry":true,"responseSiteLocale":"ehr-ES","pageToken":"0","jobId":"","jobRefrence":"","crossCountryUrl":"https://m.hays-response.es_HR,","payType":"","type":"search","cookieDomain":".hays.es"}'''
            # data ='''{"facetLocation":"","flexibleWorking":"false","fullTime":"false","industry":"","isSponsored":false,"jobType":"","partTime":"false","query":"","locations":"''' + web + '''","salMax":"","salMin":"","sortType":"RELEVANCE_DESC","specialismId":"","subSpecialismId":"","typeOnlyFilter":"","userAgent":"-Desktop","radius":100,"isCrossCountry":false,"isResponseCountry":true,"responseSiteLocale":"ehr-ES","pageToken":"0","jobId":"","jobRefrence":"","crossCountryUrl":"https://m.hays-response.it_HR,","payType":"","type":"search","cookieDomain":".hays.it"}'''
            data ='''{"facetLocation":"","flexibleWorking":"false","fullTime":"false","industry":[""],"isSponsored":false,"jobType":[""],"partTime":"false","query":"","locations":"''' + web + '''","salMax":"","salMin":"","sortType":"RELEVANCE_DESC","specialismId":"","subSpecialismId":"","typeOnlyFilter":"","userAgent":"-Desktop","radius":100,"isCrossCountry":false,"isResponseCountry":true,"responseSiteLocale":"ihr-IT","pageToken":"0","jobId":"","jobRefrence":"","crossCountryUrl":"https://m.hays-response.it_HR","payType":"","type":"search","cookieDomain":".hays.it"}'''
            x += 1
        else:
            #data ='''{"facetLocation":"","flexibleWorking":"false","fullTime":"false","industry":"","isSponsored":false,"jobType":"","partTime":"false","query":"","locations":"BARCELONA","salMax":"","salMin":"","sortType":"RELEVANCE_DESC","specialismId":"","subSpecialismId":"","typeOnlyFilter":"","userAgent":"-Desktop","radius":100,"isCrossCountry":false,"isResponseCountry":true,"responseSiteLocale":"ehr-ES","pageToken":"''' + codigo + '''","jobId":"","jobRefrence":"","crossCountryUrl":"https://m.hays-response.es_HR,","payType":"","type":"search","cookieDomain":".hays.es"}'''
            data ='''{"facetLocation":"","flexibleWorking":"false","fullTime":"false","industry":[""],"isSponsored":false,"jobType":[""],"partTime":"false","query":"","locations":"''' + web + '''","salMax":"","salMin":"","sortType":"RELEVANCE_DESC","specialismId":"","subSpecialismId":"","typeOnlyFilter":"","userAgent":"-Desktop","radius":100,"isCrossCountry":false,"isResponseCountry":true,"responseSiteLocale":"ihr-IT","pageToken":"''' + codigo + '''","jobId":"","jobRefrence":"","crossCountryUrl":"https://m.hays-response.it_HR","payType":"","type":"search","cookieDomain":".hays.it"}'''        
        
        req = requests.post(url = 'https://mapi.hays.com/jobportalapi/int/s/itl/it/jobportal/job/browse/v1/jobsv2', headers = headers, data = data)
        try:
            datos = req.json()['data']['result']['jobs']
        except Exception as e:
            print('[ERROR] datos vacio?: ' , e)
            datos = ''

        # print datos
        # exit(0)

        #pprint(req.headers)
        #exit()
        # sl.WR = ["virtual:{0}".format(datos.encode("UTF-8"))]

        if repite:
            codPage=''
            sl.extract(nextPage)
            # Fuerza a que no repita más búsquedas por defecto, si sl.M contiene el código, se cambiará a True para seguir haciendo paginación
            repite = False
            codigo = []
            if len(sl.M):
                for y in sl.M:
                    codigo.append("{0}".format(y.get("codPage", "")))
                codigo = codigo[0]
                # Si puede extraer el código, es porque hay más páginas para extraer
                repite = True
        
        sl.extract(xtr_url)
        sl.WR = []
        for y in sl.M:
            sl.WR.append("{0}".format(y.get("url", "")))


        if not len(datos):
            raise Exception('[WARN] Empty Model')

        for offer in datos:
            # continue
            ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                    published_at='')

            ad['title'] = offer.get("title", "").encode("utf-8")
            ad['description'] = libnacho.xhtml(offer.get("description", "")).encode("utf-8")
            ad['url'] = offer.get("applicationUrl", "")
            ad['city'] = offer.get("location", "").encode("utf-8")
            ad['province'] =offer.get("city", "").encode("utf-8")
            ad['salary'] = offer.get("salary", '0')
            ad['company'] = offer.get("company", "")
            contrato = offer.get("contract", "")
            if contrato == 'C':
                ad['contract'] = 'TEMPORARY'
            elif contrato == 'P':
                ad['contract'] = 'FULL_TIME'

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
