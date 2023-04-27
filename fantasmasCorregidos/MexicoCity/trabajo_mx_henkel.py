# -*- coding: utf-8 -*-
import re, sys, HTMLParser, urllib2, ssl, requests
from base_mx import db_es, slavy, text, dalek
ssl._create_default_https_context = ssl._create_unverified_context

fetched_from = 'henkel.mx'

xtr = '''city
<p class="bab-job-location">Mexico,
[,]
title
<h1 class="bab-job-title">
</h1>
description
<div class="text" >
<div class="bab-job-additional-info">'''


xtr_url = '''url
"link":"
"'''

stp = '/carrera/empleo-y-solicitud/'
page_ads = 12

pagination_generator = lambda url: (url.format(page=page) for page in xrange(0,100,10))

pages = (
    ('Trabajo', {
        'trabajo_subcat': (
            'https://www.henkel.mx/ajax/collection/mx/1347434-1347434/queryresults/asJson?select_1347434_0_Career_Level_18682_Career%20Level=&select_1347434_5_Functional_Area_18674_Functional%20Area=&select_1347434_31_Digital_1030670_Digital=&select_1347434_34_Locations_279384=Latin%20America&select_1347434_35_North_America_279406=*&select_1347434_36_United_States_877514=*&select_1347434_37_CA_279624=*&select_1347434_44_CT_279524=*&select_1347434_49_MO_878260=*&select_1347434_53_KY_1032138=*&select_1347434_55_NY_1032214=*&select_1347434_58_UT_1033094=*&select_1347434_60_SD_1033440=*&select_1347434_62_MI_1033446=*&select_1347434_66_NH_1033492=*&select_1347434_68_MN_1033538=*&select_1347434_73_PA_1033556=*&select_1347434_77_IL_1033562=*&select_1347434_86_OH_1033574=*&select_1347434_93_WI_1033600=*&select_1347434_97_WA_1033634=*&select_1347434_99_NJ_1033654=*&select_1347434_101_AR_1033818=*&select_1347434_103_TN_1033838=*&select_1347434_106_MA_1033906=*&select_1347434_109_NC_1033952=*&select_1347434_113_SC_1033986=*&select_1347434_116_IN_1034018=*&select_1347434_123_TX_1034060=*&select_1347434_127_GA_1034076=*&select_1347434_130_PR_1038994=*&select_1347434_132_VA_1042382=*&select_1347434_135_OR_1045454=*&select_1347434_137_FL_1047494=*&select_1347434_142_DC_1234470=*&select_1347434_144_CAN_1036320=*&select_1347434_145_Ontario_1040560=*&select_1347434_147_Quebec_1135560=*&select_1347434_149_Latin_America_279556=Mexico&select_1347434_150_Mexico_279558=*&select_1347434_151_Estado_De_M_xico_1032130=*&select_1347434_154_Nuevo_Le_n_1032164=*&select_1347434_156_Guanajuato_1061520=*&select_1347434_158_Jalisco_1102548=*&select_1347434_160_Brazil_279780=*&select_1347434_161_S_o_Paulo_1032892=*&select_1347434_165_Minas_Gerais_1043252=*&select_1347434_167_Cear__1059816=*&select_1347434_169_Pernambuco_1059820=*&select_1347434_171_Paran__1063138=*&select_1347434_173_Rio_Grande_Do_Sul_1497978=*&select_1347434_175_Bahia_1570716=*&select_1347434_177_Colombia_280054=*&select_1347434_178_Distrito_Capital_De_Bogot__1032148=*&select_1347434_180_ARG_1032202=*&select_1347434_181_Capital_Federal_1032204=*&select_1347434_183_CHL_1035536=*&select_1347434_184_Santiago_Metropolitan_Region_1035538=*&select_1347434_186_PER_1041660=*&select_1347434_187_Lima_1041662=*&select_1347434_189_La_Libertad_1044554=*&select_1347434_191_VEN_1044068=*&select_1347434_192_Carabobo_1044070=*&select_1347434_194_Europe_877522=*&select_1347434_195_Austria_279480=*&select_1347434_196_Vienna_1032110=*&select_1347434_198_Vorarlberg_1032956=*&select_1347434_200_Belgium_279664=*&select_1347434_201_Brussels_Capital_Region_1032548=*&select_1347434_203_Flemish_Brabant_1034764=*&select_1347434_205_Czech_Republic_846844=*&select_1347434_206_Prague_1037038=*&select_1347434_208_France_279696=*&select_1347434_209__le_De_France_1032556=*&select_1347434_212_Auvergne_Rh_ne_Alpes_1038370=*&select_1347434_214_Ile_De_France_1194908=*&select_1347434_216_Auvergne_Rh_ne_Alpes_1440168=*&select_1347434_218_Hungary_279452=*&select_1347434_219_Budapest_1032180=*&select_1347434_221_Kom_rom_Esztergom_1040476=*&select_1347434_223_B_k_s_1060346=*&select_1347434_225_Ireland_280244=*&select_1347434_226_Leinster_1032562=*&select_1347434_228_Italy_279754=*&select_1347434_229_Lombardy_1032104=*&select_1347434_233_Frosinone_1032574=*&select_1347434_235_Netherlands_279530=*&select_1347434_236_Utrecht_1032118=*&select_1347434_238_North_Holland_1037142=*&select_1347434_240_Groningen_1037340=*&select_1347434_242_North_Brabant_1053948=*&select_1347434_244_Poland_279646=*&select_1347434_245_Mazowieckie_1033792=*&select_1347434_247__wi_tokrzyskie_Province_1112362=*&select_1347434_249_Opole_Province_1122444=*&select_1347434_251_Lower_Silesia_Province_1539598=*&select_1347434_253_Portugal_279790=*&select_1347434_254_Lisbon_1477722=*&select_1347434_256_Russia_279400=*&select_1347434_257_Moscow_1059022=*&select_1347434_259_Leningrad_Region_1092424=*&select_1347434_262_Moscow_Region_1095204=*&select_1347434_264_Perm_Territory_1105748=*&select_1347434_266_Khabarovsk_Region_1175132=*&select_1347434_268_Krasnodar_Region_1130012=*&select_1347434_270_Novosibirsk_Region_1146474=*&select_1347434_272_Sverdlovsk_Region_1134518=*&select_1347434_274_Samara_Region_1318012=*&select_1347434_276_Tyumen_Region_1451246=*&select_1347434_279_Bashkortostan_1451318=*&select_1347434_281_Orenburg_Region_1539616=*&select_1347434_283_Serbia_399964=*&select_1347434_284_Central_Serbia_1034974=*&select_1347434_287_Vojvodina_1133248=*&select_1347434_289_Slovakia_279394=*&select_1347434_290_Bratislavsky_Kraj_1032098=*&select_1347434_292_Spain_279512=*&select_1347434_293_Catalonia_1032040=*&select_1347434_296_United_Kingdom_280094=*&select_1347434_297_England_1032032=*&select_1347434_299_Croatia_900708=*&select_1347434_300_Zagreb_County_1040048=*&select_1347434_302_Germany_279422=*&select_1347434_303_Bavaria_1032050=*&select_1347434_306_North_Rhine_Westphalia_1032072=*&select_1347434_308_Lower_Saxony_1032092=*&select_1347434_310_Hamburg_1032220=*&select_1347434_312_Baden_W_rttemberg_1032552=*&select_1347434_317_Schleswig_Holstein_1032608=*&select_1347434_319_Saxony_1032654=*&select_1347434_321_Hesse_1139524=*&select_1347434_323_Berlin_1140486=*&select_1347434_325_Saarland_1158052=*&select_1347434_327_SWE_1032056=*&select_1347434_328_Stockholm_1032058=*&select_1347434_330__sterg_tland_1195950=*&select_1347434_332_CHE_1035652=*&select_1347434_333_Basel_Country_1035660=*&select_1347434_335_ROU_1036594=*&select_1347434_336_Bucuresti_1036624=*&select_1347434_338_FIN_1038946=*&select_1347434_339_Southern_Finland_1038948=*&select_1347434_341_EST_1061434=*&select_1347434_342_Tartu_1061436=*&select_1347434_344_Harju_1094714=*&select_1347434_346_LVA_1061586=*&select_1347434_347_Rigas_1061588=*&select_1347434_349_BLR_1578670=*&select_1347434_350_Minsk_Voblast_1578672=*&select_1347434_352_Asia_Pacific_878136=*&select_1347434_353_Australia_279772=*&select_1347434_354_Queensland_1037134=*&select_1347434_356_New_South_Wales_1040252=*&select_1347434_359_Victoria_1042546=*&select_1347434_362_Japan_279630=*&select_1347434_363_Kanagawa_Ken_1037814=*&select_1347434_366_Osaka_Fu_1038552=*&select_1347434_369_Tokyo_To_1041202=*&select_1347434_371_Hyogo_Ken_1047536=*&select_1347434_373_Shiga_Ken_1047542=*&select_1347434_375_South_Korea_279580=*&select_1347434_376_Seoul_1032626=*&select_1347434_381_Busan_1055792=*&select_1347434_383_Incheon_1239078=*&select_1347434_385_Taiwan_280538=*&select_1347434_386_Taipei_1115448=*&select_1347434_388_Thailand_279544=*&select_1347434_389_Chon_Buri_1032826=*&select_1347434_391_Bangkok_1032844=*&select_1347434_393_Samut_Prakan_1117316=*&search_filter=&startIndex={page}&loadCount=10' ,
        )
      }
    ),
)

def crawl(web):
    
    sl = slavy.slavy()
    sl.start(web)
    sl.metaExtract = True
    # sl.step(stp)

    req = requests.get(url=web)
    data = req.json()['results']

    for d in data:
        sl.WR.append('https://www.henkel.mx{0}'.format(d['link']))

    #Para pruebas
    # sl.printWR()
    #~ exit(0)
    #sl.printM()
    #sl.printstatus()
    #~ sl.WR = sl.WR[0:5]

    if not len(sl.WR):
        raise Exception('[WARN] Empty web region')

    sl.extract(xtr)

    if not len(sl.M):
        raise Exception('[WARN] Empty Model')

    for offer in sl.M:
        ad = dict(title='', url='', city='', province='', salary=0, company='', description='', contract='',  published_at='')

        ad['title'] = offer.get("title", "")
        ad['description'] = offer.get("description", "")
        ad['url'] = offer.get("@url", "")
        ad['city'] = offer.get("city", "")
        ad['province'] = offer.get("province", "")
        ad['salary'] = offer.get("salary",'0')
        ad['company'] = offer.get("company", "henkel")
        ad['contract'] = offer.get("contract", "")


        yield ad

#saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator, debug=False)
#saltcellar.crawl = crawl
#saltcellar.exterminate()

#new code for test auto debug script
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

    saltcellar = dalek.Dalek(pages, page_ads, fetched_from, db_es, pagination_generator,debug_mode)
    saltcellar.crawl = crawl
    saltcellar.exterminate()
