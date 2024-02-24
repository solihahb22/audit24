from .models import BebanDalamPenghuni, BebanDalamPencahayaan, BebanDalamPeralatan, BebanLuarDinding, \
    BebanLuarPintu, BebanInfiltrasiVentilasi
import math
import numpy as np


tahanan_thermal_beton = {
    'agregat_pasir_kerikil': 0.55,
    'agregat_ringan':1.94,
}
tahanan_udara_luar = 0.029
tahanan_udara_dalam = 0.120

tahanan_thermal_dinding ={
    'plester semen':1.39,
    'bata luar' : 0.76,
    'batu bata': 0.76,
    'bata biasa': 1.39,
    'kayu jati': 9.090909091,
    'kayu akasia':9.174311927,
    'kayu mahoni': 9.615384615,
    'hebel': 7.142857143,
    'batako':2.949852507
}
# satuan tahanan thermal = m.K/W

tahanan_thermal_pelapis={
    'wallpaper':5.555555556,
    'batu alam granit':	0.5780346821,
    'batu alam marbel':	0.4830917874,
    'batu alam limestone':	0.7936507937,
    'batu alam sandstone':	0.5464480874,
    'wood plastic composite':1.639344262,
    'gypsum':	1.388888889,
    'karpet':	16.66666667,
}


tahanan_thermal_jendela = {
    'kaca': 1.282051282,
}

tahanan_thermal_plafon={
    'grc':	0.6666666667,
    'wpc':	1.639344262,
    'metal alumunium':	1.666666667,
    'metal baja stainless':	6.25,
    'pvc':	5,
    'gypsum':	1.388888889,
    'akustik kayu pinus':	11.11111111,
    'akustik softwood':	11.11111111,
    'akustik karpet':	16.66666667,
    'akustik rockwool':	18.51851852,
    'eternit':	12.1,
    'cement fibre':	12.1,
    'triplek': 	8.333333333,
    'plywood':	8.333333333,
}
tahanan_thermal_lantai = {
    'keramik':	0.5882352941,
    'granit':	0.5780346821,
    'kayu jati':	9.090909091,
    'kayu akasia':	9.174311927,
    'kayu mahoni':	9.615384615,
    'batu alam granit':	0.5780346821,
    'batu alam marble':	0.4830917874,
    'batu alam limestone (marmer)':	0.7936507937,
    'batu alam sandstone':	0.5464480874,
    'vinyl':	5.882352941,
    'cor beton':	1.315789474,
    'karpet (cotton)':	16.66666667,
}


#arah_ke_matahari =['arah_n','arah_ne','arah_e','arah_se','arah_s','arah_sw','arah_w','arah_nw']
arah_ke_matahari_dinding = ['utara', 'timur laut', 'timur', 'tenggara', 'selatan', 'barat daya', 'barat', 'barat laut' ]
cltd_dinding_d_mpl390_kk350 = {
    7:[3,4,5,5,4,6,7,6],
    8:[3,4,5,5,4,5,6,5],
    9:[3,6,7,5,3,5,5,4],
    10:[3,8,10,7,3,4,5,4],
    11:[4,10,13,10,4,4,5,4],
    12:[4,11,15,12,5,5,5,4],
    13:[5,12,17,14,7,6,6,5],
    14:[6,13,18,16,9,7,6,6],
    15:[6,13,18,17,11,9,8,7],
    16:[7,13,18,18,13,12,10,8],
    17:[8,14,18,18,15,15,13,10],
    18:[9,14,18,18,16,18,17,12],
    19:[10,14,17,17,16,20,20,15],
    20:[11,13,17,17,16,21,22,17],
    'max':[11,14,18,18,16,21,23,18],
}


def get_cltd_dinding(awal_waktu_matahari, akhir_waktu_matahari, arah):
    waktu =[]
    cltd_arah = []
    for j in range(awal_waktu_matahari,akhir_waktu_matahari+1):
        waktu.append(j)
        cltd_semua_arah = cltd_dinding_d_mpl390_kk350.get(j)
        #cltd_arah = []
        for i,c in zip(arah_ke_matahari_dinding,cltd_semua_arah):
            #print(f'{i},{c}')
            if i == arah:
                cltd_arah.append(c)
    return waktu, cltd_arah


#update bagian ini menyesuaikan bagian user interface
def beban_kalor_dinding(list_dinding_per_sisi):
    luaran_per_sisi =[]
    sisis = []
    for i, dinding_per_sisi in enumerate(list_dinding_per_sisi):
        #hitung luas persisi
        luas_total =0
        tahanan_thermal_total=0
        bag_dinding = None
        for j,dinding in enumerate(dinding_per_sisi):
            if dinding.kategori =='pokok':
                luas_total += dinding.dim_luas
            #print(f'luas:{luas_total}')
            tahanan_thermal_total += dinding.tahanan_thermal*dinding.dim_tebal
            bag_dinding = dinding
        sisi = bag_dinding.sisi

        if bag_dinding.awal_kontak_matahari >0 and bag_dinding.akhir_kontak_matahari>0 and bag_dinding.temp_rerata_ruang_berdekatan==0:
            #ini dinding non partisi
            print(f'luas total:{luas_total}')
            tahanan_thermal_total += tahanan_udara_luar + tahanan_udara_dalam
            print(f'tahanan thermal total={tahanan_thermal_total}')
            koef_perpindahan_kalor = 1 / tahanan_thermal_total
            print(f'koef_perpindahan_kalor:{koef_perpindahan_kalor}')
            waktu, cltd = get_cltd_dinding(bag_dinding.awal_kontak_matahari, bag_dinding.akhir_kontak_matahari,
                                           bag_dinding.arah)
            print(f'cltd: {cltd} ')
            ti = bag_dinding.gedung.temperatur_obj
            tm = bag_dinding.gedung.temperatur_rh
            cltd_penyesuaian_dinding = [cltdkei + (25.5 - ti) + (tm - 29.4) for cltdkei in cltd]  # hitung per cltd
            print(f'cltd penyesuaian: {cltd_penyesuaian_dinding} ')
            q_dinding = [koef_perpindahan_kalor * luas_total * cltd_penyesuaian for cltd_penyesuaian in
                         cltd_penyesuaian_dinding]
            print(f'jumlah q dinding{len(q_dinding)} ')
            print(f'q dinding luar {bag_dinding.sisi}:{q_dinding}')
            results =[]
            for w,c,cp,qd in zip(waktu,cltd,cltd_penyesuaian_dinding,q_dinding):
                q_i = {
                    'waktu':w,
                    'cltd':c,
                    'cltd_peny': cp,
                    'q_d': qd,
                }
                results.append(q_i)
            luaran = {
                'sisi': sisi,
                'status_dinding': 'nonpartisi',
                'q': results,
            }
            luaran_per_sisi.append(luaran)
        elif bag_dinding.temp_rerata_ruang_berdekatan > 0:
            #dinding partisi
            koef_perpindahan_kalor = 1 / tahanan_thermal_total
            print(f'koef_perpindahan_kalor:{koef_perpindahan_kalor}')
            q_dinding = koef_perpindahan_kalor * luas_total * (bag_dinding.temp_rerata_ruang_berdekatan -
                                                                       bag_dinding.gedung.temperatur_obj)
            print(f'q dinding partisi {bag_dinding.sisi}:{q_dinding}')
            luaran = {
                'sisi': sisi,
                'status_dinding': 'partisi',
                'q': q_dinding,
            }
            luaran_per_sisi.append(luaran)
    return luaran_per_sisi


def beban_kalor_beton(list_beton_per_sisi):
    luaran_per_sisi =[]
    sisi = None
    for i, beton_per_sisi in enumerate(list_beton_per_sisi):
        #hitung luas persisi
        luas_total =0
        tahanan_thermal_total=0
        bag_beton = None
        status = None
        for j,beton in enumerate(beton_per_sisi):
            luas_total += beton.dim_luas
            print(f'tahanan thermal:{beton.tahanan_thermal}, tebal:{beton.dim_tebal}')
            tahanan_thermal_total += beton.tahanan_thermal*beton.dim_tebal
            bag_beton = beton
        print(f'sisi:{bag_beton.sisi}')
        print(f'tahanan_thermal_total:{tahanan_thermal_total}')
        sisi = bag_beton.sisi
        if bag_beton.awal_kontak_matahari >0 and bag_beton.akhir_kontak_matahari>0 and bag_beton.temp_rerata_ruang_berdekatan==0:
            #ini dinding non partisi
            print('non partisi')
            status = 'nonpartisi'
            #tahanan_thermal_total += tahanan_udara_luar + tahanan_udara_dalam
            #print(f'tahanan thermal total={tahanan_thermal_total}')
            koef_perpindahan_kalor = 1 / tahanan_thermal_total
            print(f'koef_perpindahan_kalor:{koef_perpindahan_kalor}')
            #perlu cek cltd beton apakah sama dengan dinding
            waktu, cltd = get_cltd_dinding(bag_beton.awal_kontak_matahari, bag_beton.akhir_kontak_matahari,
                                           bag_beton.arah)
            print(f'cltd: {cltd} ')
            ti = bag_beton.gedung.temperatur_obj
            tm = bag_beton.gedung.temperatur_rh
            cltd_penyesuaian_beton = [cltdkei + (25.5 - ti) + (tm - 29.4) for cltdkei in cltd]  # hitung per cltd
            print(f'cltd penyesuaian: {cltd_penyesuaian_beton} ')
            q_beton = [koef_perpindahan_kalor * luas_total * cltd_penyesuaian for cltd_penyesuaian in
                         cltd_penyesuaian_beton]
            print(f'jumlah q beton{len(q_beton)} ')
            print(f'q beton luar {bag_beton.sisi}:{q_beton}')
            results = []
            for w, c, cp, qd in zip(waktu, cltd, cltd_penyesuaian_beton, q_beton):
                q_i = {
                    'waktu': w,
                    'cltd': c,
                    'cltd_peny': cp,
                    'q_b': qd,
                }
                results.append(q_i)
            luaran = {
                'sisi': sisi,
                'status_beton': status,
                'q': results,
            }
            luaran_per_sisi.append(luaran)

        elif bag_beton.temp_rerata_ruang_berdekatan > 0:
            #dinding partisi
            print('partisi')
            status = 'partisi'
            koef_perpindahan_kalor = 1 / tahanan_thermal_total
            print(f'koef_perpindahan_kalor:{koef_perpindahan_kalor}')
            q_beton = koef_perpindahan_kalor * luas_total * (bag_beton.temp_rerata_ruang_berdekatan -
                                                                       bag_beton.gedung.temperatur_obj)
            print(f'q beton {bag_beton.sisi}:{q_beton}')
            luaran = {
                'sisi': sisi,
                'status_beton': status,
                'q': q_beton,
            }
            luaran_per_sisi.append(luaran)

    return luaran_per_sisi
#sudah di set di obyek pintu saat input data

tahanan_thermal_pintu={
    'alumunium':0.004524886878,
    'pvc':5,
    'fiberglass':	25,
    'besi':	0.02222222222,
    'kaca buram':	1.25,
    'baja':	0.02222222222,
    'kayu':6.31,
}
#cltd pintu menggunakan cltd dinding
def beban_kalor_pintu(list_pintu):
    luaran_per_sisi = []
    print(f'list pintu:{list_pintu}')
    for i, pintu_per_sisi in enumerate(list_pintu):
        # hitung luas persisi
        len_pintu = len(pintu_per_sisi)
        print(f'{len_pintu}')
        luas_total = 0
        tahanan_thermal_total = 0
        bag_pintu = None
        for j, pintu in enumerate(pintu_per_sisi):
            pintukei= pintu
            luas_total += pintu.dim_luas
            print(f'luas:{luas_total}')
            tahanan_thermal_total += pintu.tahanan_thermal * pintu.dim_tebal
            bag_pintu = pintu

        if bag_pintu.awal_kontak_matahari > 0 and bag_pintu.akhir_kontak_matahari > 0 and bag_pintu.temp_rerata_ruang_berdekatan == 0:
            # ini pintu non partisi
            print(f'luas total:{luas_total}')
            #tahanan_thermal_total += tahanan_udara_luar + tahanan_udara_dalam
            print(f'tahanan thermal total={tahanan_thermal_total}')
            koef_perpindahan_kalor = 1 / tahanan_thermal_total
            print(f'koef_perpindahan_kalor:{koef_perpindahan_kalor}')
            waktu, cltd = get_cltd_dinding(bag_pintu.awal_kontak_matahari, bag_pintu.akhir_kontak_matahari,
                                           bag_pintu.arah)
            print(f'cltd: {cltd} ')

            ti = bag_pintu.gedung.temperatur_obj
            tm = bag_pintu.gedung.temperatur_rh
            cltd_penyesuaian_pintu = [cltdkei + (25.5 - ti) + (tm - 29.4) for cltdkei in cltd]  # hitung per cltd
            print(f'cltd penyesuaian: {cltd_penyesuaian_pintu} ')
            q_pintu = [koef_perpindahan_kalor * luas_total * cltd_penyesuaian for cltd_penyesuaian in
                         cltd_penyesuaian_pintu]
            print(f'jumlah q dinding{len(q_pintu)} ')
            print(f'q dinding luar {bag_pintu.sisi}:{q_pintu}')
            luaran = {'waktu': waktu, 'q': q_pintu}
            luaran_per_sisi.append(luaran)
        elif bag_pintu.temp_rerata_ruang_berdekatan > 0:
            # dinding partisi
            koef_perpindahan_kalor = 1 / tahanan_thermal_total
            print(f'koef_perpindahan_kalor:{koef_perpindahan_kalor}')
            q_pintu = koef_perpindahan_kalor * luas_total * (bag_pintu.temp_rerata_ruang_berdekatan -
                                                               bag_pintu.gedung.temperatur_obj)
            print(f'q dinding partisi {bag_pintu.sisi}:{q_pintu}')
            luaran = {'waktu': None, 'q': q_pintu}
            luaran_per_sisi.append(luaran)
    return luaran_per_sisi


arah_ke_matahari_kaca = ['utara', 'timur laut', 'timur', 'tenggara', 'selatan', 'barat daya', 'barat', 'barat laut', 'horizontal' ]

#clf kaca pada waktu matahari
clf_kaca_waktu_matahari ={
    6:{'utara':0.73,'timur laut':0.56,'timur': 0.47,'tenggara':0.3,'selatan':0.09,'barat daya':0.07,'barat':0.06,'barat laut':0.07,'horizontal':0.12},
    7:{'utara':0.66,'timur laut':0.76,'timur': 0.72,'tenggara':0.57,'selatan':0.16,'barat daya':0.11,'barat':0.09,'barat laut':0.11,'horizontal':0.27},
    8:{'utara':0.65,'timur laut':0.74,'timur': 0.8,'tenggara':0.74,'selatan':0.23,'barat daya':0.14,'barat':0.11,'barat laut':0.14,'horizontal':0.44},
    9:{'utara':0.73,'timur laut':0.58,'timur':0.76,'tenggara':0.81,'selatan':0.38,'barat daya':0.16,'barat':0.13,'barat laut':0.17,'horizontal':0.59},
    10:{'utara':0.8,'timur laut':0.37,'timur':0.62,'tenggara':0.79,'selatan':0.58,'barat daya':0.19,'barat':0.15,'barat laut':0.19,'horizontal':0.72},
    11:{'utara':0.86,'timur laut':0.29,'timur':0.41,'tenggara':0.68,'selatan':0.75,'barat daya':0.22,'barat':0.16,'barat laut':0.2,'horizontal':0.81},
    12:{'utara':0.89,'timur laut':0.27,'timur':0.27,'tenggara':0.49,'selatan':0.83,'barat daya':0.38,'barat':0.17,'barat laut':0.21,'horizontal':0.85},
    13:{'utara':0.89,'timur laut':0.26,'timur':0.24,'tenggara':0.33,'selatan':0.8,'barat daya':0.59,'barat':0.31,'barat laut':0.22,'horizontal':0.85},
    14:{'utara':0.86,'timur laut':0.24,'timur':0.22,'tenggara':0.28,'selatan':0.68,'barat daya':0.75,'barat':0.53,'barat laut':0.3,'horizontal':0.81},
    15:{'utara':0.82,'timur laut':0.22,'timur':0.2,'tenggara':0.25,'selatan':0.5,'barat daya':0.83,'barat':0.72,'barat laut':0.52,'horizontal':0.71},
    16:{'utara':0.75,'timur laut':0.2,'timur':0.17,'tenggara':0.22,'selatan':0.35,'barat daya':0.81,'barat':0.82,'barat laut':0.73,'horizontal':0.58},
    17:{'utara':0.78,'timur laut':0.16,'timur':0.14,'tenggara':0.18,'selatan':0.27,'barat daya':0.69,'barat':0.81,'barat laut':0.82,'horizontal':0.42},
    18:{'utara':0.91,'timur laut':0.12,'timur':0.11,'tenggara':0.13,'selatan':0.19,'barat daya':0.45,'barat':0.61,'barat laut':0.69,'horizontal':0.25},
}
def get_clf_kaca(awal_waktu, akhir_waktu, arah):
    if awal_waktu < 6 or akhir_waktu > 18:
        return None
    else:
        waktu = []
        clf =[]
        for i in range(awal_waktu,akhir_waktu+1):
            waktu.append(i)
            clfkaca = clf_kaca_waktu_matahari.get(i)
            #print(f'clfkaca:{clfkaca}')
            clf_val = clfkaca.get(arah)
            #print(f'clfval:{clf_val}')
            clf.append(clf_val)
        return waktu, clf

#cltd index ke 0 --> jam matahari = 1 dst
cltd_kaca =[1,0,-1,-1,-1,-1,-1,0,1,2,4,5,7,7,8,8,7,7,6,4,3,2,2,1]


def get_cltd_kaca (awal_waktu_matahari, akhir_waktu_matahari):
    waktu = []
    cltd =[]
    for j in range(awal_waktu_matahari, akhir_waktu_matahari + 1):
        waktu.append(j)
        cltd_j = cltd_kaca[j-1]
        cltd.append(cltd_j)
    return waktu, cltd

#waktu_matahari	arah_n	arah_ne	arah_e	arah_se	arah_s	arah_sw	arah_w	arah_nw

#jenis kaca, ScG, shfg, cltd, clf
koefisien_peneduh_kaca_scg ={
    'kaca tunggal lembaran':{'tanpa peneduh dalam':1,'krei pelindung sedang':0.64, 'krei pelindung terang':0.55,'tirai gulung gelap':0.59,'tirai gulung terang':	0.25},
    'kaca tunggal pelat':{'tanpa peneduh dalam':0.95,'krei pelindung sedang': 0.64,'krei pelindung terang':0.55, 'tirai gulung gelap':0.59,'tirai gulung terang':0.25},
    'kaca tunggal_penyerap panas':{'tanpa peneduh dalam':0.7,'krei pelindung sedang':0.57,'krei pelindung terang':0.53,	'tirai gulung gelap':0.4,'tirai gulung terang':0.3},
    'kaca tunggal_penyerap panas':	{'tanpa peneduh dalam':0.5,'krei pelindung sedang':0.54,'krei pelindung terang':0.52,'tirai gulung gelap':0.4,'tirai gulung terang':0.25},
    'kaca rangkap lembaran biasa':	{'tanpa peneduh dalam':0.9,'krei pelindung sedang':0.57,'krei pelindung terang':	0.51,'tirai gulung gelap':0.6,'tirai gulung terang':0.25},
    'kaca rangkap pelat':	{'tanpa peneduh dalam':0.83,'krei pelindung sedang':0.57,'krei pelindung terang': 0.51,'tirai gulung gelap':	0.6,'tirai gulung terang':0.25},
    'kaca rangkap reflektif': {'tanpa peneduh dalam':{'min':0.2, 'max':0.4}, 'krei pelindung sedang': {'min':0.2,'max':0.33}, 'krei pelindung terang':	None,  'tirai gulung gelap':None,'tirai gulung terang':None},
}

#shgf
perolehan_kalor_matahari_kaca_32_lu ={
    'Januari':	{'utara':75,'teduh':75,	'timur laut':90,'barat laut':90,'timur':550,'barat':550,'tenggara':	785,'barat daya':785,'selatan':775,'horizontal':555},
	'Februari':	{'utara':85,'teduh':85,'timur laut':205,'barat laut':205,'timur':645,'barat':645,'tenggara':780,'barat daya':780,'selatan':700,'horizontal':685},
	'Maret':	{'utara':100,'teduh':100,'timur laut':330,'barat laut':330,'timur':695,'barat':695,'tenggara':700,'barat daya':700,'selatan':545,'horizontal':780},
	'April':	{'utara':115,'teduh':115,'timur laut':450,'barat laut':450,'timur':700,'barat':700,'tenggara':580,'barat daya':580,'selatan':355,'horizontal':845},
	'Mei':	{'utara':120,'teduh':120,'timur laut':530,'barat laut':530,'timur':685,'barat':685,'tenggara':480,'barat daya':480,'selatan':230,'horizontal':865},
	'Juni':	{'utara':140,'teduh':140,'timur laut':555,'barat laut':555,'timur':675,'barat':675,'tenggara':440,'barat daya':440,'selatan':190,'horizontal':870},
	'Juli':	{'utara':120,'teduh':120,'timur laut':530,'barat laut':530,'timur':685,'barat':685,'tenggara':480,'barat daya':480,'selatan':230,'horizontal':865},
	'Agustus':	{'utara':115,'teduh':115,'timur laut':450,'barat laut':450,'timur':700,'barat':700,'tenggara':580,'barat daya':580,'selatan':355,'horizontal':845},
	'September':	{'utara':100,'teduh':100,'timur laut':330,'barat laut':330,'timur':695,'barat':695,'tenggara':700,'barat daya':700,'selatan':545,'horizontal':780},
	'Oktober':	{'utara':	85,	'teduh':85,'timur laut':205,'barat laut':205,'timur':645,'barat': 645,'tenggara':780,'barat daya':780,'selatan':700,'horizontal':685},
	'November':	{'utara':	75,	'teduh':75,'timur laut':90,'barat laut':90,'timur':550,'barat':550,'tenggara':785,'barat daya':785,'selatan':775,'horizontal':555},
	'Desember':	{'utara':	69,	'teduh':69,'timur laut':69,'barat laut':69,'timur':510,'barat':510,'tenggara':775,'barat daya':775,'selatan':795,'horizontal':500},
}
perolehan_kalor_matahari_kaca_40_lu ={
    'Januari':{'utara':75,'teduh':75,'timur laut':63,'barat laut':63,'timur':480,'barat':480,'tenggara':755,'barat daya':755,'selatan':795,'horizontal':420},
    'Februari':	{'utara':85,'teduh':85,'timur laut':155,'barat laut':155,'timur':575,'barat':575,'tenggara':760,'barat daya':760,'selatan':750,'horizontal':565},
    'Maret':{'utara':100,'teduh':100,'timur laut':285,'barat laut':285,'timur':660,'barat':660,'tenggara':730,'barat daya':730,'selatan':640,'horizontal':690},
    'April':{'utara':115,'teduh':115,'timur laut':435,'barat laut':435,'timur':690,'barat':690,'tenggara':630,'barat daya':630,'selatan':475,'horizontal':790},
    'Mei':	{'utara':120,'teduh':120,'timur laut':515,'barat laut':515,'timur':690,'barat':690,'tenggara':545,'barat daya':545,'selatan':350,'horizontal':830},
    'Juni':	{'utara':140,'teduh':140,'timur laut':540,'barat laut':540,'timur':680,'barat':680,'tenggara':510,'barat daya':510,'selatan':300,'horizontal':840},
    'Juli':	{'utara':120,'teduh':120,'timur laut':515,'barat laut':515,'timur':690,'barat':690,'tenggara':545,'barat daya':545,'selatan':350,'horizontal':830},
    'Agustus':	{'utara':115,'teduh':115,'timur laut':435,'barat laut':435,'timur':690,'barat':690,'tenggara':630,'barat daya':630,'selatan':475,'horizontal':790},
    'September':{'utara':100,'teduh':100,'timur laut':285,'barat laut':285,'timur':660,'barat':660,'tenggara':730,'barat daya':730,'selatan':640,'horizontal':690},
    'Oktober':	{'utara':85,'teduh':85,'timur laut':155,'barat laut':155,'timur':575,'barat':575,'tenggara':760,'barat daya':760,'selatan':750,'horizontal':565},
    'November':	{'utara':75,'teduh':75,'timur laut':63,'barat laut':63,'timur':480,'barat':480,'tenggara':755,'barat daya':755,'selatan':795,'horizontal':420},
    'Desember':{'utara':57,'teduh':57,'timur laut':57,'barat laut':57,'timur':475,'barat':475,'tenggara':730,'barat daya':730,'selatan':800,'horizontal':355},
}
def get_shgf_kaca(lintang, arah):
    shgf = []
    daftar_lintang_rujukan = [32, 40]
    jarak_ke_lintang_rujukan = [abs(lintang - lintang_ref) for lintang_ref in daftar_lintang_rujukan]
    lintang_obj = min(jarak_ke_lintang_rujukan)
    daftar_shgf = None
    if lintang_obj < 36:
        daftar_shgf = perolehan_kalor_matahari_kaca_32_lu
    elif lintang_obj > 36:
        daftar_shgf = perolehan_kalor_matahari_kaca_40_lu
    #ambil berdasarkan arah
    daftar_bulan = daftar_shgf.keys()
    for i, bulan in enumerate(daftar_bulan):
        shgf.append(daftar_shgf.get(bulan).get(arah))
    return daftar_bulan, shgf

koef_thermal_kaca = {
    'single_glass':{ 'Al': 1.01, 'wood': 0.90, 'vinyl': 0.90},
    'double_glass_3per8':{'Al': 0.56, 'wood': 0.47,'vinyl': 0.47},
    'double_glass_3per8_efilm': { 'Al':0.48, 'wood':0.37,'vinyl':0.37 },
    'triple_glass_3per8':{'Al':0.43, 'wood':0.36,'vinyl':0.36 },
    'triple_glass_3per8_efilm':{'Al':0.34, 'wood':0.24,'vinyl':0.24 }
}


def beban_kalor_kaca(list_kaca):
    tahanan_total_kaca_per_sisi = 0
    luas_kaca = 0
    q_kacas = []
    result_qr = []
    koef_peneduh = []
    q_rad_transpose = None
    bulan_notempty = None
    sisi = None
    status = 'partisi'
    for i, kaca in enumerate(list_kaca):
        print(f'sisi:{kaca.sisi}')
        sisi = kaca.sisi
        luas_kaca = kaca.dim_luas
        print(f'luas_kaca: {luas_kaca}')
        print(f'kaca dim tebal: {kaca.dim_tebal}')
        tahanan_thermal = tahanan_thermal_jendela.get('kaca')/ kaca.dim_tebal
        print(f'tahanan thermal: {tahanan_thermal}')
        koef_peneduh_kaca = koefisien_peneduh_kaca_scg.get(kaca.material)
        print(f'sub_kategori_kaca: {kaca.sub_kategori_material}')
        sub_koef_peneduh_kaca = koef_peneduh_kaca.get(kaca.sub_kategori_material)
        #print(f'sub_koef_peneduh_kaca_cek: {sub_koef_peneduh_kaca_cek}')
        #sub_koef_peneduh_kaca = 0.25
        ####perlu ditambahkan kode pengecekan kalau sub_koef_peneduh_kaca adalah dictionary
        #### if isinstance(sub_koef_peneduh_kaca, dict):
        print(f'koef_peneduh_kaca:{koef_peneduh_kaca}')
        print(f'sub_koef_peneduh_kaca(sc):{sub_koef_peneduh_kaca}')
        lapisan = koef_thermal_kaca.get(kaca.jumlah_lapisan)
        koef_u_kaca = lapisan.get(kaca.jenis_frame)
        koef_perpindahan_kalor = 1/tahanan_thermal
        #koef_perpindahan_kalor =
        print(f'koef_perpindahan_kalor kaca {koef_perpindahan_kalor}')
        waktu, cltd = get_cltd_kaca(kaca.awal_kontak_matahari, kaca.akhir_kontak_matahari)
        ti = kaca.gedung.temperatur_obj
        tm = kaca.gedung.temperatur_rh
        cltd_penyesuaian_kaca = [cltdkei + (25.5-ti) + (tm-29.4) for cltdkei in cltd] #hitung per cltd
        #print(f'cltd_penyesuaian_kaca{cltd_penyesuaian_kaca}')
        q_konduksi_kaca = [koef_u_kaca*luas_kaca*cltd_penyesuaian for cltd_penyesuaian in cltd_penyesuaian_kaca]
        print(f'q_konduksi_kaca{q_konduksi_kaca}')
        result_kk = []
        list_r_kaca = []
        for w, c, cp, qk in zip(waktu, cltd, cltd_penyesuaian_kaca, q_konduksi_kaca):
            q_i = {
                'waktu': w,
                'cltd': c,
                'cltd_peny': cp,
                'q_k': qk,
            }
            result_kk.append(q_i)
        if kaca.awal_kontak_matahari > 0 and kaca.akhir_kontak_matahari > 0:
            # pada sisi non partisi
            status = 'nonpartisi'
            #q_radiasi_kaca = luas_kaca * koef_peneduh_kaca * faktor perolehan kalor shgf * clf
            waktu_mthr, clf_kaca = get_clf_kaca(kaca.awal_kontak_matahari, kaca.akhir_kontak_matahari, kaca.arah)
            print(f'waktu mthr:{waktu_mthr}')
            print(f'clf_kaca:{clf_kaca}')
            lintang = kaca.gedung.lintang
            bulan, shgf = get_shgf_kaca(lintang,kaca.arah)
            print(f'bulan:{bulan}')
            print(f'shgf:{shgf}')
            if not isinstance(sub_koef_peneduh_kaca, dict):
                q_rad_kaca_perbulan = [luas_kaca * sub_koef_peneduh_kaca*shgf_ke_i if shgf_ke_i is not None else None for shgf_ke_i in shgf  ]
                print(f'q_radiasi_perbulan:{q_rad_kaca_perbulan}')
                bulan_notempty, q_radiasi_kaca = calc_q_radiasi_kaca_detail(bulan,clf_kaca, q_rad_kaca_perbulan)
                print(f'q_radiasi_kaca:{q_radiasi_kaca}')
                q_rad_transpose = np.array(q_radiasi_kaca).T.tolist()
                print(f'z_radiasi_kaca:{q_rad_transpose}')
                print(f'dim_radiasi_kaca:{len(q_rad_transpose)}')
                #list_r_kaca =[]
                for w,clf,q in zip(waktu_mthr,clf_kaca,q_rad_transpose):
                    gab = []
                    gab.append(w)
                    gab.append(clf)
                    for iq in q:
                        gab.append(iq)
                    list_r_kaca.append(gab)

        q_kaca ={
            'sisi': sisi,
            'status': status,
            'q_konduksi': result_kk,
            'bulan': bulan_notempty,
            'q_radiasi':list_r_kaca,
        }
        q_kacas.append(q_kaca)

    return q_kacas

def calc_q_radiasi_kaca_detail(bulan,clf_kaca, q_rad_perbulan):
    list_bulan = list(bulan)
    q_rad_total =[]
    bulan_not_empty =[]
    for i, q_rad_ke_i in enumerate(q_rad_perbulan):
        if q_rad_ke_i is not None:
            q_rad_perhari=[ clf*q_rad_ke_i for clf in clf_kaca]
            q_rad_total.append( q_rad_perhari)
            bulan_not_empty.append(list_bulan[i])
    return bulan_not_empty, q_rad_total


#shgp
perolehan_kalor_aktivitas={
    'tidur':	70,
    'duduk tenang':	100,
    'berdiri':	150,
    'berjalan 3km per jam':	305,
    'pekerja kantor':	150,
    'mengajar':	175,
    'warung':	185,
    'toko pengecer':	185,
    'industri min':	300,
    'industri max':	600,
}
#shgp
perolehan_kalor_sensibel_aktivitas={
    'tidur':	75,
    'duduk tenang':	60,
    'berdiri':	50,
    'berjalan 3km per jam':	35,
    'pekerja kantor':55,
    'mengajar':50,
    'warung':	50,
    'toko pengecer':50,
    'industri min':	35,
    'industri max':	35,
}


#clf penghuni (index list di clf dimulai dari 1)
clf_penghuni_dan_alat_zona_a ={
2:[0.75,0.88,0.18,0.08,0.04,0.02,0.01,0.01,0.01,0.01,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
4:[0.75,0.88,0.93,0.95,0.22,0.1,0.05,0.03,0.02,0.02,0.01,0.01,0.01,0.01,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
6:[0.75,0.88,0.93,0.95,0.97,0.97,0.23,0.11,0.06,0.04,0.03,0.02,0.02,0.01,0.01,0.01,0.01,0.00,0.00,0.00,0.00,0.00,0.00,0.00],
8:[0.75,0.88,0.93,0.95,0.97,0.97,0.98,0.98,0.24,0.11,0.06,0.04,0.03,0.02,0.02,0.01,0.01,0.01,0.01,0.01,0.00,0.00,0.00,0.00],
10:[0.75,0.88,0.93,0.95,0.97,0.97,0.98,0.98,0.99,0.99,0.24,0.12,0.07,0.04,0.03,0.02,0.02,0.01,0.01,0.01,0.01,0.01,0.00,0.00],
12:[0.75,0.88,0.93,0.96,0.97,0.98,0.98,0.98,0.99,0.99,0.99,0.99,0.25,0.12,0.07,0.04,0.03,0.02,0.02,0.02,0.01,0.01,0.01,0.01],
    #lengkapi sampai 18
}
clf_penghuni_dan_alat_default = {
2: [0.60, 0.67,0.13, 0.09, 0.08, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
4: [0.61, 0.67, 0.72, 0.76, 0.20, 0.16, 0.13,0.11, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01],
6: [0.62, 0.68, 0.73, 0.77, 0.80, 0.83, 0.26, 0.20, 0.17, 0.15, 0.13, 0.11, 0.09, 0.08, 0.07, 0.06, 0.06, 0.05, 0.04, 0.03,0.03, 0.03, 0.02, 0.02],
8: [0.63, 0.69, 0.74, 0.77, 0.80, 0.83, 0.85, 0.87, 0.30, 0.24, 0.20, 0.17, 0.15, 0.13, 0.11, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03],
10:[0.63, 0.70, 0.75, 0.78, 0.81, 0.84, 0.86, 0.88, 0.89, 0.91, 0.33, 0.27, 0.22, 0.19, 0.17, 0.14, 0.12, 0.11, 0.09, 0.08, 0.07, 0.06, 0.05, 0.05],
12:[0.65, 0.71, 0.76, 0.79, 0.82, 0.84, 0.87, 0.88, 0.90, 0.91, 0.92, 0.93, 0.35, 0.29, 0.24, 0.21, 0.18, 0.16, 0.13, 0.12, 0.10, 0.09, 0.08, 0.07],
14:[0.67, 0.73, 0.78, 0.81, 0.83, 0.86, 0.88, 0.89, 0.91, 0.92, 0.93, 0.94, 0.95, 0.95, 0.37, 0.30, 0.25, 0.22, 0.19, 0.16, 0.15, 0.12, 0.11, 0.09],
16:[0.70, 0.76, 0.80, 0.83, 0.85, 0.87, 0.89, 0.90, 0.92, 0.93, 0.94, 0.95, 0.95, 0.96, 0.96, 0.97, 0.38, 0.31, 0.26, 0.23, 0.20, 0.17, 0.15, 0.13],
18:[0.74, 0.80, 0.83, 0.85, 0.87, 0.89, 0.91, 0.92, 0.93, 0.94, 0.95, 0.95, 0.96, 0.97, 0.97, 0.97, 0.98, 0.98, 0.39, 0.32, 0.27, 0.23, 0.2, 0.17],
}

def beban_kalor_penghuni (penghuni:BebanDalamPenghuni, zona='default'):
    print(f'total_aktivitas:{penghuni.total_aktivitas}')
    shg = perolehan_kalor_sensibel_aktivitas.get(penghuni.aktivitas)
    clf_penghuni = None
    if zona == 'a':
        clf_penghuni = clf_penghuni_dan_alat_zona_a.get(penghuni.total_aktivitas)
    elif zona == 'default':
        clf_penghuni = clf_penghuni_dan_alat_default.get(penghuni.total_aktivitas)

    print(f'clf penghuni:{clf_penghuni}')

    clf_sensibel = clf_penghuni[int(math.ceil(penghuni.lama_aktivitas))-1]
    print (f'clf sensibel:{clf_sensibel}')
    #clf_sensibel = clf_penghuni[4]
    q_sp = None
    q_lt = None
    q_sp = penghuni.jumlah_penghuni * shg * clf_sensibel
    print(f'penghuni: {penghuni.jumlah_penghuni}, shg: {shg}, clf sensibel{clf_sensibel}')
    clf_laten = 1
    q_lt = penghuni.jumlah_penghuni * shg * clf_laten
    print(f'penghuni: {penghuni.jumlah_penghuni}, shg: {shg}, clf laten{clf_laten}')
    print(f'q_sp:{q_sp}')
    print(f'q_lt:{q_lt}')
    q_penghuni = {
        'q_sp': q_sp,
        'q_lt': q_lt,
    }
    return q_penghuni

#list_alat : beberapa alat
def beban_kalor_alat(list_alat: [BebanDalamPeralatan], lama_dlm_ruang,total_dlm_ruang, zona='default',  l_f = 1):
    q_input = 0
    for i, alat in enumerate(list_alat):
        q_input += alat.beban * alat.jumlah
    print(f'q_input alat:{q_input}')
    clf_alat = 0
    if zona == 'default':
        if total_dlm_ruang in clf_penghuni_dan_alat_default.keys():
            clf_alat = clf_penghuni_dan_alat_default.get(total_dlm_ruang)[lama_dlm_ruang-1]
            print(f'clf_alat:{clf_alat}')
        else:
            dist = 18
            total = 18
            for val in enumerate(clf_penghuni_dan_alat_default.keys()):
                if abs(val-total_dlm_ruang)< dist:
                    dist = abs(val-total_dlm_ruang)
                    total = val
            clf_alat = clf_penghuni_dan_alat_default.get(total)[lama_dlm_ruang-1]
            print(f'clf_alat:{clf_alat}')
    print(f'clf_alat:{clf_alat}')
    q_alat = q_input * clf_alat * l_f
    print(f'q_alat:{q_alat}')
    return q_alat


#faktor penggunaan cat untuk beban pencahayaan
pantulan_cahaya_cat ={
    'putih': 0.85,
    'kuning':0.75,
    'abuabuterang':0.75,
    'biruterang':0.55,
    'birugelap':0.10,
    'maple': 0.07,
    'mahogany': 0.12,
    'walnut':0.16,
}
#clf pencahayaan
#index menyatakan lama jam setelah lampu dinyalakan
clf_penerangan = {
    'pemasangan xt nyala 10':[0.08, 0.62, 0.66, 0.69, 0.73, 0.75, 0.78, 0.8, 0.82, 0.84, 0.85, 0.32, 0.29, 0.26, 0.23, 0.21, 0.19, 0.17, 0.15],
    'pemasangan xt nyala 16':[0.19, 0.72, 0.75, 0.77, 0.8, 0.82, 0.84, 0.85, 0.87, 0.88, 0.89, 0.9, 0.91,0.92, 0.93, 0.94, 0.94, 0.4, 0.36],
    'pemasangan yt nyala 10':[0.01, 0.76, 0.81, 0.84, 0.88, 0.9, 0.92, 0.93, 0.95, 0.96, 0.97, 0.22, 0.18, 0.14, 0.12, 0.09, 0.08, 0.06, 0.05],
    'pemasangan yt nyala 16':[0.05, 0.79, 0.83, 0.87, 0.89, 0.91, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.98, 0.98, 0.99, 0.99, 0.99, 0.24, 0.2],
}
#status : key pada clf penerangan
def beban_kalor_pencahayaan(cahaya:BebanDalamPencahayaan, lama_jam_nyala,status='pemasangan xt nyala 10', f_ballas=1.2):
    #faktor penggunaan cat, faktor ballast, faktor beban pendingin
    f_u = pantulan_cahaya_cat.get(cahaya.warna_cat)
    print(f'fu:{f_u}')
    clf = clf_penerangan.get(status)[lama_jam_nyala]
    print(f'clf lampu:{clf}')
    q_lampu = cahaya.jenis_lampu * cahaya.jumlah_lampu * f_u * f_ballas * clf
    print(f'q_lampu:{q_lampu}')
    return q_lampu

#koefisien_stack koefisien_angin delta_t
koefisien_stack_rumah = {
    1: 0.000145,
    2: 0.000290,
    3: 0.000435,
}

koefisien_angin ={
    'shielding 1': {1: 0.000319, 2:0.000420, 3: 0.000494},
    'shielding 2': {1: 0.000246, 2:0.000325, 3: 0.000384},
    'shielding 3': {1: 0.000174, 2:0.000231, 3: 0.000271},
    'shielding 4': {1: 0.000104, 2:0.000137, 3: 0.000161},
    'shielding 5': {1: 0.000032, 2:0.000042, 3: 0.000049}
}
kebocoran_udara_efektif = {
    'ceiling general': 1.8,
    'ceiling drop': 0.19,
    'crawl space general': 10,
    'crawl space 200 x 400 vent': 10,
    'door frame general': 12,
    'door frame wood caulked': 0.3,
    'door frame wood uncaulked': 1.7,
    'window frame wood caulked': 0.3,
    'window frame wood uncaulked': 1.7,
    'windows awning not weatherstrippied': 1.6,
    'windows awning weatherstrippied': 0.8,
    'wall cast in place concrete': 0.5,
    'wall clay brick cavity wall, finished': 0.68,
    'stop kontak':2.5,
}
# dalam derajat celcius
temperatur_outlet_evaporator = 22
# langit-langit, pintu, stop kontak
#Dinding bagian dalam Langit-langit , Pintu, Stop kontak, Jendela dengan bingkai

def beban_kalor_air_exchange(pintus, penghuni, wo = 0.017, wi = 0.010):
    q_pintus=[]

    for i, pintu in enumerate(pintus):
        ach = pintu.frekwensi_buka_tutup* penghuni.jumlah_penghuni * pintu.waktu_pintu_terbuka /3600
        gedung = pintu.gedung
        q_pintu= ach*(gedung.dim_panjang * gedung.dim_lebar * gedung.dim_tinggi )/60
        print (f'q_pintu: {q_pintu}')
        q_sensible = 1.23 * q_pintu *(gedung.temperatur_rh - gedung.temperatur_obj)
        q_laten = 3010 * q_pintu * (wo - wi)
       #print (f'q_sensible pintu: {q_sensibles}')
        #print(f'q_laten pintu: {q_latens}')
        q_pintu ={
            'sisi': pintu.sisi,
            'q_sensible': q_sensible,
            'q_laten': q_laten,
        }
        q_pintus.append(q_pintu)
    return q_pintus
#komponen: langit-langit, pintu, stop_kontak: BebanInfiltrasiVentilasi
def beban_kalor_infiltrasi_ventilasi(beban_inv : BebanInfiltrasiVentilasi, pintus, penghuni, jendela=None, w0=0.017, w1=0.01):
    luas_kebocoran_udara = calculate_kebocoran_udara(beban_inv, pintus)
    print(f'luas_kebocoran_udara:{luas_kebocoran_udara}')
    koef_stack = koefisien_stack_rumah.get(beban_inv.level_lantai)
    delta_t = 273 * (beban_inv.gedung.temperatur_rh - temperatur_outlet_evaporator)
    koef_angin = koefisien_angin.get(beban_inv.kelas_shielding).get(beban_inv.level_lantai)
    q_infiltrasi = luas_kebocoran_udara * math.sqrt(koef_stack * delta_t + koef_angin * beban_inv.kec_angin_luar)
    print(f'q_infiltrasi:{q_infiltrasi }')
    q_sensibel_inf = 1.3 * q_infiltrasi
    print(f'q_sensibel:{q_sensibel_inf}')
    q_laten_inf = 3010 * q_infiltrasi * (w0 - w1)
    print(f' q_laten_inv:{ q_laten_inf}')
    #nama = beban_inv.nama_ruang.split(',')
    nama = [x.strip() for x in beban_inv.nama_ruang.split(',')]
    kategori = kebutuhan_udara_luar_m3_per_min_per_orang.get(nama[0])
    subkategori = kategori.get(nama[1])
    state = penghuni.state
    laju_udara_vent = subkategori.get(state)
    q_sensibel_vent = 1.3*penghuni.jumlah_penghuni*laju_udara_vent * (beban_inv.gedung.temperatur_rh - temperatur_outlet_evaporator)
    q_laten_vent = 3010*penghuni.jumlah_penghuni*laju_udara_vent* (w0 - w1)
    print(f'q_sensibel_vent{q_sensibel_vent}')
    print(f'q_laten_vent{q_laten_vent}')
    bk_inv_ven ={
        'q_sensibel_inf': q_sensibel_inf,
        'q_laten_inf': q_laten_inf,
        'q_sensibel_vent': q_sensibel_vent,
        'q_laten_vent':  q_laten_vent,
    }
    return bk_inv_ven

def calculate_kebocoran_udara(bk_inviltrasi: BebanInfiltrasiVentilasi, pintus ):
    kebocoran_udara = 0
    if bk_inviltrasi:
        kebocoran1 = bk_inviltrasi.jumlah_stop_kontak * kebocoran_udara_efektif.get('stop kontak')
        #kebocoran_udara.append(kebocoran1)
        kebocoran_udara += kebocoran1
        print(f'kebpcoran stop kontak: {kebocoran1}')
        kebocoran2 = bk_inviltrasi.gedung.dim_panjang * bk_inviltrasi.gedung.dim_lebar * kebocoran_udara_efektif.get(bk_inviltrasi.jenis_ceiling)
        #kebocoran_udara.append(kebocoran2 )
        print(f'kebpcoran ceiling: {kebocoran2}')
        kebocoran_udara += kebocoran2
    if pintus:
        kebocoran3 = 0
        for i, pintu in enumerate(pintus):
            kebocoran3 += pintu.dim_luas * kebocoran_udara_efektif.get(pintu.frame)
        #kebocoran_udara.append(kebocoran3)
        kebocoran_udara += kebocoran3
    return kebocoran_udara




kebutuhan_udara_luar_m3_per_min_per_orang={
    'kantor':{'ruang kerja':{'merokok':0.6, 'tdk merokok':0.15},
              'ruang pertemuan':{'merokok':1.05, 'tdk merokok':0.21},
              },
    'sekolah':{
        'kelas': {'merokok':0.75, 'tdk merokok':0.15},
        'laboratorium':{'merokok': None, 'tdk merokok':0.3},
        'perpustakaan':{'merokok':None, 'tdk merokok':0.15},
        },
    'ruang kerja':{
        'proses makanan': {'merokok':None, 'tdk merokok':0.15},
        'khazanah bank':{'merokok': None, 'tdk merokok': 0.15},
        'farmasi': {'merokok': None, 'tdk merokok': 0.21},
        'studio fotografi': {'merokok': None, 'tdk merokok': 0.21},
        'ruang gelap': {'merokok': None, 'tdk merokok': 0.60},
        'ruang cetak foto': {'merokok': None, 'tdk merokok': 0.15},
        }
}

def resume_beban_kalor (bk_dinding, bk_beton,bk_kaca,q_penghuni, q_lampu, q_alat,q_pintus, q_inv_ven):
    slrs = []
    bk_dr =[]
    bk_in_ven=[]
    ersh = []
    erlh = []
    q_partisi = 0;
    for bk_d in bk_dinding:
        if bk_d['status_dinding'] == 'nonpartisi':
            for qi in bk_d['q']:
                slr = {
                    'waktu': qi['waktu'],
                    'q_d': qi['q_d'],
                }
                slrs.append(slr)
        elif bk_d['status_dinding'] == 'partisi':
            q_partisi += bk_d['q']
    for i, bk_b in enumerate(bk_beton):
        if bk_b['status_beton'] == 'nonpartisi':
            for qi in bk_b['q']:
                if slrs[i]['waktu'] == qi['waktu']:
                    slrs[i]['q_d'] += qi['q_b']
                elif bk_b['status_beton'] == 'partisi':
                    q_partisi += bk_b['q']
    for bk_k in bk_kaca:
        if bk_k['status']=='partisi':
            q_partisi += bk_k['q_konduksi'][0]['q_k']
        else:
            for i,qk in enumerate(bk_k['q_konduksi']):
                if slrs[i]['waktu'] == qk['waktu']:
                    slrs[i]['q_k'] = qk['q_k']
            for i,qr in enumerate(bk_k['q_radiasi']):
                if slrs[i]['waktu'] == qr[0]:
                    slrs[i]['q_r'] = qr[6]
    slr_max =0
    ersh ={
        'bk_slr': slr_max,
    }
    for i,slr in enumerate(slrs):
        slrs[i]['q_partisi'] = q_partisi
        slrs[i]['total']= slr['q_partisi']+ slr['q_r']+slr['q_k']+slr['q_d']
        if slr_max < slrs[i]['total']:
            slr_max = slrs[i]['total']

    #beban kalor dalam ruangan
    q_s_total=0
    q_l_total=0
    penghuni = {
        'kategori':'penghuni',
        'q_sp': q_penghuni['q_sp'],
        'q_lt': q_penghuni['q_lt'],
    }
    q_s_total += q_penghuni['q_sp']
    q_l_total += q_penghuni['q_lt']
    lampu = {
        'kategori': 'cahaya',
        'q_sp': q_lampu,
        'q_lt': None,
    }
    q_s_total += q_lampu
    alat = {
        'kategori': 'peralatan',
        'q_sp': q_alat,
        'q_lt': None,
    }
    q_s_total += q_alat
    bk_dr.append(penghuni)
    bk_dr.append(lampu)
    bk_dr.append(alat)
    q_s_p =0
    q_l_p =0
    for q_pintu in q_pintus:
        q_s_p += q_pintu['q_sensible']
        q_l_p += q_pintu['q_laten']
    q_s_total += q_s_p
    q_l_total += q_l_p
    air_exchange = {
        'kategori': 'air exchange',
        'q_sp': q_s_p,
        'q_lt': q_l_p,
    }
    bk_dr.append(air_exchange)
    total = {
        'kategori':'Total',
        'q_sp': q_s_total,
        'q_lt': q_l_total,
    }
    ersh['bk_sdr']= total['q_sp']
    erlh ={
        'bk_ldr': total['q_lt'],
    }
    bk_dr.append(total)
    #beban kalor inviltrasi ventilasi
    inf ={
        'media':  'Infiltrasi',
        'q_sen': q_inv_ven['q_sensibel_inf'],
        'q_laten': q_inv_ven['q_laten_inf'],
    }
    ven ={
        'media': 'Ventilasi',
        'q_sen': q_inv_ven['q_sensibel_vent'],
        'q_laten': q_inv_ven['q_laten_vent'],
    }
    total = {
        'media': 'Total',
        'q_sen': q_inv_ven['q_sensibel_vent'] + q_inv_ven['q_sensibel_inf'],
        'q_laten': q_inv_ven['q_laten_vent'] + q_inv_ven['q_laten_inf'],
    }
    ersh['bk_siv']= total['q_sen']
    ersh['total']=  ersh['bk_siv'] + ersh['bk_sdr'] + ersh['bk_slr']
    ersh['safety']= 0.05* ersh['total']
    ersh['value']=  ersh['total'] + ersh['safety']

    erlh['bk_liv']= total['q_laten']
    erlh['total'] = erlh['bk_liv'] + erlh['bk_ldr']
    erlh['safety'] = 0.05 * erlh['total']
    erlh['value'] = erlh['total'] + erlh['safety']
    bk_in_ven.append(inf)
    bk_in_ven.append(ven)
    bk_in_ven.append(total)

    return slrs,bk_dr, bk_in_ven,ersh,erlh




