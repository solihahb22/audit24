from django import forms

from django.core.exceptions import ValidationError
from .models import BebanDalamPencahayaan, BebanDalamPeralatan, BebanInfiltrasiVentilasi,ProfilGedung,\
                     BebanLuarDinding, BebanDalamPenghuni, BebanLuarKaca, BebanLuarPintu, BebanLuarCeiling, BebanLuarBeton
from . import audit_lib

def nama_ruang():
    pilihan = [
        ('kantor, ruang kerja', 'kantor, ruang kerja'),
        ('kantor, ruang pertemuan','kantor, ruang pertemuan'),
        ('sekolah, kelas', 'sekolah, kelas'),
        ('sekolah, laboratorium', 'sekolah, laboratorium'),
        ('sekolah, perpustakaan','sekolah, perpustakaan'),
        ('ruang kerja, proses makanan', 'ruang kerja, proses makanan'),
        ('ruang kerja, khazanah bank','ruang kerja, khazanah bank'),
        ('ruang kerja, farmasi','ruang kerja, farmasi'),
        ('ruang kerja, studio fotografi','ruang kerja, studio fotografi'),
        ('ruang kerja, ruang gelap','ruang kerja, ruang gelap'),
        ('ruang kerja, ruang cetak foto','ruang kerja, ruang cetak foto'),
    ]
    return pilihan

def merokok():
    state =[
        ('tdk merokok', 'tdk merokok'),
        ('merokok', 'merokok'),
    ]
    return state

class ProfilGedungForm(forms.ModelForm):
    #nama_ruang = forms.ChoiceField(choices= nama_ruang())

    class Meta:
        model = ProfilGedung
        fields = '__all__'  # cara yang tidak secure
        widgets = {
            'alamat_lokasi': forms.Textarea(),
            'dim_panjang': forms.TextInput(attrs={'placeholder': 'meter'}),
             'dim_lebar': forms.TextInput(attrs={'placeholder': 'meter'}),
            'dim_tinggi':forms.TextInput(attrs={'placeholder': 'meter'}),
            'temperatur_rh':forms.TextInput(attrs={'placeholder': 'Celcius'}),
            'temperatur_obj':forms.TextInput(attrs={'placeholder': 'Celcius'}),
            'kecepatan_angin': forms.TextInput(attrs={'placeholder': 'meter/second'}),
        }


def material_dinding_dan_pelapis():
    material1 = [ (f'{key}',f'{key}') for key in audit_lib.tahanan_thermal_dinding]
    material2 = [(f'{key}', f'{key}') for key in audit_lib.tahanan_thermal_pelapis]
    return material1 +material2

def material_dinding():
    material1 = [ (f'{key}',f'{key}') for key in audit_lib.tahanan_thermal_dinding]
    return material1

def material_pelapis():
    material = [(f'{key}',f'{key}') for key in audit_lib.tahanan_thermal_pelapis]
    return material


def material(key):
    material = []
    if key=="pintu":
        material =[(f'{key}',f'{key}') for key in audit_lib.tahanan_thermal_pintu]
    if key == "kaca":
        material = [(f'{key}', f'{key}') for key in audit_lib.koefisien_peneduh_kaca_scg]
    return material

def arah_matahari (key):
    if key == 'dinding':
        arah = [(f'{arah}', f'{arah}') for arah in audit_lib.arah_ke_matahari_dinding]
    elif  key == 'kaca':
        arah = [(f'{arah}', f'{arah}') for arah in audit_lib.arah_ke_matahari_kaca]
    return arah

AWAL_KONTAK_DINDING =[
    (7, '07:00'),(8,'08:00'),(9,'09:00'),(10,'10:00'),(11,'11:00'),(12,'12:00'),(13,'13:00')
]
AKHIR_KONTAK_DINDING =[
    (12,'12:00'),(13,'13:00'),(14,'14:00'),(15,'15:00'),(16,'16:00'),(17,'17:00'),(18,'18:00')]
AWAL_KONTAK_KACA =[
    (5,'05:00'),(6,'06:00'),(7,'07:00'),(8,'08:00'),(9,'09:00'),(10,'10:00'),(11,'11:00'),(12,'12:00'),(13,'13:00')
]
AKHIR_KONTAK_KACA =[
    (12,'12:00'),(13,'13:00'),(14,'14:00'),(15,'15:00'),(16,'16:00'),(17,'17:00'),(18,'18:00')]

KATEGORI_PARTISI =[
    ('P','Partisi'),
    ('N','Non-partisi'),
]

class DindingForm(forms.ModelForm):
    material = forms.ChoiceField(choices=material_dinding())
    partisi = forms.ChoiceField(choices=KATEGORI_PARTISI)
    arah = forms.ChoiceField(choices=arah_matahari('dinding'))
    awal_kontak_matahari = forms.ChoiceField(choices=AWAL_KONTAK_DINDING)
    akhir_kontak_matahari = forms.ChoiceField(choices=AKHIR_KONTAK_DINDING)
    class Meta:
        model = BebanLuarDinding
        exclude =['tahanan_thermal',]

def material_beton():
    material_b = [(f'{beton}', f'{beton}') for beton in audit_lib.tahanan_thermal_beton]
    return material_b

class BetonForm(forms.ModelForm):
    material = forms.ChoiceField(choices=material_beton())
    arah = forms.ChoiceField(choices=arah_matahari('dinding'))
    partisi = forms.ChoiceField(choices=KATEGORI_PARTISI)
    awal_kontak_matahari = forms.ChoiceField(choices=AWAL_KONTAK_DINDING)
    akhir_kontak_matahari = forms.ChoiceField(choices=AKHIR_KONTAK_DINDING)
    class Meta:
        model = BebanLuarBeton
        exclude =['tahanan_thermal',]


def sub_kategori_peneduh():
    sub_kategori =[
        ('tanpa peneduh dalam','tanpa peneduh dalam'),
        ('krei pelindung sedang','krei pelindung sedang'),
        ('krei pelindung terang','krei pelindung terang'),
        ('tirai gulung gelap','tirai gulung gelap'),
        ('tirai gulung sedang','tirai gulung sedang'),
    ]
    return sub_kategori


JUMLAH_LAPISAN =[
    ('single_glass', 'Lapisan Tunggal'),
    ('double_glass_3per8','Lapisan Ganda 3/8 Inchi'),
    ('double_glass_3per8_efilm','Lapisan Ganda 3/8 Inchi E-film'),
    ('triple_glass_3per8','Lapisan Ganda 3/8 Inchi'),
    ('triple_glass_3per8_efilm','Lapisan Ganda 3/8 Inchi E-film'),
]
JENIS_FRAME=[
    ( 'Al', 'Alumunium'),
    ('wood', 'Wood'),
    ('vinyl', 'Vinyl')
]


class KacaForm(forms.ModelForm):
    material = forms.ChoiceField(choices=material("kaca"))
    arah = forms.ChoiceField(choices=arah_matahari('kaca'))
    sub_kategori_material = forms.ChoiceField(choices=sub_kategori_peneduh())
    awal_kontak_matahari = forms.ChoiceField(choices=AWAL_KONTAK_KACA)
    akhir_kontak_matahari = forms.ChoiceField(choices=AKHIR_KONTAK_KACA)
    jumlah_lapisan = forms.ChoiceField(choices=JUMLAH_LAPISAN)
    jenis_frame = forms.ChoiceField(choices=JENIS_FRAME)
    class Meta:
        model = BebanLuarKaca
        exclude =['tahanan_thermal',]

def kategori_frame():
    frame =[
        ('door frame general','door frame general'),
        ('door frame wood caulked', 'door frame wood caulked'),
        ('door frame wood uncaulked', 'door frame wood uncaulked'),
    ]
    return frame
class PintuForm(forms.ModelForm):
    material = forms.ChoiceField(choices=material("pintu"))
    frame = forms.ChoiceField(choices=kategori_frame())
    awal_kontak_matahari = forms.ChoiceField(choices=AWAL_KONTAK_DINDING)
    akhir_kontak_matahari = forms.ChoiceField(choices=AKHIR_KONTAK_DINDING)
    class Meta:
        model = BebanLuarPintu
        exclude =['tahanan_thermal',]
class CeilingForm(forms.ModelForm):
    class Meta:
        model = BebanLuarCeiling
        exclude =['tahanan_thermal',]


def warna_cat():
    warna = [(f'{key}',f'{key}') for key in audit_lib.pantulan_cahaya_cat.keys()]
    return warna


class PencahayaanForm(forms.ModelForm):
    warna_cat = forms.ChoiceField(choices=warna_cat())
    class Meta:
        model = BebanDalamPencahayaan
        fields = "__all__"

def aktivitas(key):
    aktivitas_list = []
    if key=="perolehan_kalor":
        aktivitas_list =[(f'{key}',f'{key}') for key in audit_lib.perolehan_kalor_aktivitas]

    return aktivitas_list
def total_aktivitas():
    total_aktivitas =[(f'{key}',f'{key}') for key in audit_lib.clf_penghuni_dan_alat_default]
    return total_aktivitas
class PenghuniForm(forms.ModelForm):
    aktivitas = forms.ChoiceField(choices=aktivitas("perolehan_kalor"))
    total_aktivitas = forms.ChoiceField(choices=total_aktivitas())
    state = forms.ChoiceField(choices=merokok())
    class Meta:
        model = BebanDalamPenghuni
        fields = "__all__"

class BebanDalamPeralatanForm(forms.ModelForm):
    class Meta:
        model = BebanDalamPeralatan
        fields = "__all__"

def ceiling_categ():
    ceil =[
        ('ceiling general', 'ceiling general'),
        ('ceiling drop', 'ceiling drop'),
    ]
    return ceil

def get_shileding_categ():
    shield = [(f'{key}',f'{key}') for key in audit_lib.koefisien_angin.keys()]
    return shield

KATEGORI_LEVEL =(
    (1, 'Lantai 1'),
    (2, 'Lantai 2'),
    (3, 'Lantai 3'),
)
class BebanInfiltrasiVentilasiForm(forms.ModelForm):
    jenis_ceiling = forms.ChoiceField(choices=ceiling_categ())
    kelas_shielding = forms.ChoiceField(choices=get_shileding_categ())
    nama_ruang = forms.ChoiceField(choices=nama_ruang())
    level_lantai = forms.ChoiceField(choices=KATEGORI_LEVEL)

    class Meta:
        model = BebanInfiltrasiVentilasi
        fields= "__all__"


class SearchProfil(forms.Form):
    gedung = forms.ModelChoiceField(queryset=ProfilGedung.objects.all())
    lantai = forms.ChoiceField(choices=KATEGORI_LEVEL)






