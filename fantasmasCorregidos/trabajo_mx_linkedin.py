# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, json, requests
from StringIO import StringIO
import gzip
from base_mx import *

from stem.control import Controller
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'linkedin.mx'

xtr = '''title
<h3 class="sub-nav-cta__header">
</h3>
company
<div class="sub-nav-cta__sub-text-container">
</a>
city
<span class="sub-nav-cta__meta-text">
(,|</span>)
description
<div class="description__text description__text--rich">
</div>
contract
Tipo de empleo</h3>
</span>'''

xtr_stp = '''url
data-id="
"'''

xtr_stp = '''idoferta
<a class="base-card__full-link" href="
"'''

stp = "/jobs/view/"
page_ads = 25 
page_stp = 1

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0, 4500, 25))
# with Controller.from_port(port = 9051) as controller:
#     pass
pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.linkedin.com/jobs/search?keywords=&location=M%C3%A9xico&geoId=103323778&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum={page}',
        )
    }
     ),
)


# def renew():
#     torproxy.renew(controller)
#     torproxy.connect()
#     print "mi ip: ",torproxy.show_my_ip()

def crawl(web):
    sl = slavy.slavy()
    sl.start(web)
    sl.step(stp)
    sl.metaExtract = True

    # sl.printWR()
    # sl.printM()
    # sl.printstatus()
    # sl.WR = sl.WR[0:5]
    # exit(0)

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')
    sl.headers["Host"] = "mx.linkedin.com"
    sl.headers["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    sl.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    sl.headers["Accept-Language"] = "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
    sl.headers["Accept-Encoding"] = "gzip, deflate, br"
    sl.headers["DNT"] = "1"
    sl.headers["Connection"] = "keep-alive"
    #sl.headers["Cookie"] = "JSESSIONID=ajax:8197322034764725567; lang=v=2&lang=es-es; bcookie="v=2&cf678d37-f6ca-4b9e-8be5-48399b7887ad"; bscookie="v=1&202006180944002a39c67d-d431-44fd-8f6d-2235941e730fAQHs730EY5ScS74BkJ_7gFkljnIyyRgn"; lissc=1; lidc="b=VGST03:g=2069:u=1:i=1592473440:t=1592559840:s=AQGGnid0Bqsq9Vhori8uFqvc7-c4P-mH"; recent_history=AQGpq_fbblvIggAAAXLG1k27_C9B8eRIzR29CKDaMl0xFBRvsHEeWcZlZLVEPgDIBaucRpNGWjJHTwGsSZIY1Fv8DRFKb1BslPpwm4tRiTbxyBzljWU88jc_OigLhdiMUjN9FjIJM6Ym0nL9vIU0-TsRRlYZ5bGO7Y-VJFntlXlZmbSRqz6bAgwA2I_MfvuV71qnCZ5O3f212Ia9xgJ4sYn9wH_RbIIyhBIGqGxUJCyScVUu8pmAmm0rdcDisOkwBOT_Lz5wkRL3YPefqu0EpqZ4b6dQQ2GvWHlQSeWjQCrt5mSg5xlT-V6u_eaBwwSRf9oZthusCZX1Jm9j-p6A27xNbcheDP_DXz8h9aX-vD0RqiJu9pLwt_MzOKm_81P-abXGrwCAJYwQxw1NQZCJoatM0ELKewSJYOvkB6QLz6PEAzVuwRWcc63F9Xz144d7iQHVw_NVCTHdeiVcGhfd8MrZqAkvla336PFXgrFTmLDVxEQF6CtIXg; _ga=GA1.2.1199650844.1592473442; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-408604571%7CMCIDTS%7C18432%7CMCMID%7C46966410969026161275081730905216083573%7CMCOPTOUT-1592486902s%7CNONE%7CvVersion%7C4.6.0; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; _gcl_au=1.1.390421371.1592473442; _gat=1"
    sl.headers["Upgrade-Insecure-Requests"] = "1"
    sl.headers["Cache-Control"] = "max-age=0"
    sl.headers["TE"] = "Trailers"
    sl.extract(xtr)
    #sl.printM()
    #exit(0)

    if not len(sl.M):
        for y in range(1,10):
            sl.polite(2,4)
            renew()
            sl.start(web)
            sl.metaExtract = True
            sl.extract(xtr_stp)
            sl.WR = ["https://mx.linkedin.com/jobs/view/{0}".format(y.get("idoferta","")) for y in sl.M]
            sl.headers["Host"] = "mx.linkedin.com"
            sl.headers["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
            sl.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            sl.headers["Accept-Language"] = "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"
            sl.headers["Accept-Encoding"] = "gzip, deflate, br"
            sl.headers["DNT"] = "1"
            sl.headers["Connection"] = "keep-alive"
            #sl.headers["Cookie"] = "JSESSIONID=ajax:8197322034764725567; lang=v=2&lang=es-es; bcookie="v=2&cf678d37-f6ca-4b9e-8be5-48399b7887ad"; bscookie="v=1&202006180944002a39c67d-d431-44fd-8f6d-2235941e730fAQHs730EY5ScS74BkJ_7gFkljnIyyRgn"; lissc=1; lidc="b=VGST03:g=2069:u=1:i=1592473440:t=1592559840:s=AQGGnid0Bqsq9Vhori8uFqvc7-c4P-mH"; recent_history=AQGpq_fbblvIggAAAXLG1k27_C9B8eRIzR29CKDaMl0xFBRvsHEeWcZlZLVEPgDIBaucRpNGWjJHTwGsSZIY1Fv8DRFKb1BslPpwm4tRiTbxyBzljWU88jc_OigLhdiMUjN9FjIJM6Ym0nL9vIU0-TsRRlYZ5bGO7Y-VJFntlXlZmbSRqz6bAgwA2I_MfvuV71qnCZ5O3f212Ia9xgJ4sYn9wH_RbIIyhBIGqGxUJCyScVUu8pmAmm0rdcDisOkwBOT_Lz5wkRL3YPefqu0EpqZ4b6dQQ2GvWHlQSeWjQCrt5mSg5xlT-V6u_eaBwwSRf9oZthusCZX1Jm9j-p6A27xNbcheDP_DXz8h9aX-vD0RqiJu9pLwt_MzOKm_81P-abXGrwCAJYwQxw1NQZCJoatM0ELKewSJYOvkB6QLz6PEAzVuwRWcc63F9Xz144d7iQHVw_NVCTHdeiVcGhfd8MrZqAkvla336PFXgrFTmLDVxEQF6CtIXg; _ga=GA1.2.1199650844.1592473442; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-408604571%7CMCIDTS%7C18432%7CMCMID%7C46966410969026161275081730905216083573%7CMCOPTOUT-1592486902s%7CNONE%7CvVersion%7C4.6.0; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; _gcl_au=1.1.390421371.1592473442; _gat=1"
            sl.headers["Upgrade-Insecure-Requests"] = "1"
            sl.headers["Cache-Control"] = "max-age=0"
            sl.headers["TE"] = "Trailers"
            sl.extract(xtr)
            if len(sl.M):
                break

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',
                  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] =offer.get("province", "")
        ad['salary'] = offer.get("salary", '0')
        ad['company'] = offer.get("company", "")
        ad['contract'] = offer.get("contract", "")

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
