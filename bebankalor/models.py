from django.db import models


# Create your models here.
class ProfilGedung (models.Model):
    KATEGORI_LINTANG = (
        ('LS', 'Lintang Selatan'),
        ('LU', 'Lintang Utara'),
    )
    KATEGORI_BUJUR = (
        ('BB', 'Bujur Barat'),
        ('BT', 'Bujur Timur'),
    )

    nama = models.CharField(max_length=50)
    #nama_ruang = models.CharField(max_length=50, default='sekolah, kelas')
    alamat_lokasi = models.CharField(max_length=150)
    lintang = models.FloatField(max_length=5,default=0)
    posisi_lintang = models.CharField(max_length=50, choices=KATEGORI_LINTANG,default='LU')
    bujur = models.FloatField(max_length=5,default=0)
    posisi_bujur = models.CharField(max_length=50, choices=KATEGORI_BUJUR,default='BB')
    dim_panjang = models.FloatField(max_length=5)
    dim_lebar = models.FloatField(max_length=5)
    dim_tinggi = models.FloatField(max_length=5)
    temperatur_rh = models.FloatField(max_length=5) #temperatur rata-rata harian
    temperatur_obj = models.FloatField(max_length=5) #temperatur yg ingin dicapai
    kecepatan_angin = models.FloatField(max_length=5,default=0)


    def __str__(self):
        #return f'{self.nama}: {self.alamat_lokasi}, {self.lintang} {self.posisi_lintang}, {self.bujur}, {self.posisi_bujur}'
        return f'{self.nama}'


class BebanLuar (models.Model):
    KATEGORI_BEBAN_LUAR = (
        ('dinding', 'dinding'),
        ('kaca', 'kaca'),
        ('pintu','pintu'),
        ('ceiling','ceiling')
    )

    gedung = models.ForeignKey(ProfilGedung, on_delete= models.PROTECT)
    kategori = models.CharField(max_length=50, choices=KATEGORI_BEBAN_LUAR)
    sisi = models.CharField(max_length=15,default="notspecified")
    dim_luas = models.FloatField(max_length=5)
    dim_tebal = models.FloatField(max_length=5)
    kontak_matahari = models.CharField(max_length=1)# y or n
    material = models.CharField(max_length=50)# perlu diset saat input data untuk kinerja komputasi, tdk perlu akses ke db
    tahanan_thermal = models.FloatField(max_length=5)
    rasio_kelembaban_udara_ruangan = models.FloatField(max_length=5, default=0)
    rasio_kelembaban_udara_luar = models.FloatField(max_length=5, default=0)

KATEGORI_PARTISI=(
        ('P', 'partisi'),
        ('N', 'non-partisi')
    )

class BebanLuarDinding (models.Model):
    KATEGORI_SISI = (
        ('sisi_barat', 'Sisi Barat'),
        ('sisi_selatan', 'Sisi Selatan'),
        ('sisi_timur', 'Sisi Timur'),
        ('sisi_utara', 'Sisi Utara'),
    )
    KATEGORI_LAPISAN =(
        ('pokok','pokok'),
        ('tambahan','tambahan')
    )

    gedung = models.ForeignKey(ProfilGedung, on_delete= models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    nama_ruang = models.CharField(max_length=50,default='ruang1')
    sisi = models.CharField(max_length=15,choices=KATEGORI_SISI)
    arah = models.CharField(max_length=15, default='timur')
    kategori = models.CharField(max_length=50,choices=KATEGORI_LAPISAN, default='pokok')
    dim_luas = models.FloatField(max_length=5, default=0)
    dim_tebal = models.FloatField(max_length=5)
    partisi = models.CharField(max_length=1, choices=KATEGORI_PARTISI, default='P')  # lainnya 'N'
    awal_kontak_matahari = models.IntegerField(default=0)
    akhir_kontak_matahari = models.IntegerField(default=0)
    temp_rerata_ruang_berdekatan = models.FloatField(max_length=5, default=0)
    material = models.CharField(max_length=50)# perlu diset saat input data untuk kinerja komputasi, tdk perlu akses ke db
    tahanan_thermal = models.FloatField(max_length=5)

    def clean_temp_rerata_ruang_berdekatan(self):
        data_partisi = self.cleaned_data['partisi']
        data = self.clean_data['temp_rerata_ruang_berdekatan']
        if data_partisi == 'N':
            data = 0
        return data
    def clean_awal_kontak_matahari(self):
        data_partisi = self.cleaned_data['partisi']
        data = self.clean_data['awal_kontak_matahari']
        if data_partisi == 'P':
            data = 0
        return data

    def clean_akhir_kontak_matahari(self):
        data_partisi = self.cleaned_data['partisi']
        data = self.clean_data['akhir_kontak_matahari']
        if data_partisi == 'P':
            data = 0
        return data

class BebanLuarBeton (models.Model):
    KATEGORI_SISI = (
        ('sisi_barat', 'Sisi Barat'),
        ('sisi_selatan', 'Sisi Selatan'),
        ('sisi_timur', 'Sisi Timur'),
        ('sisi_utara', 'Sisi Utara'),
    )
    gedung = models.ForeignKey(ProfilGedung, on_delete= models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    nama_ruang = models.CharField(max_length=50,default='ruang1')
    sisi = models.CharField(max_length=15,choices=KATEGORI_SISI)
    arah = models.CharField(max_length=15, default='')
    dim_tebal = models.FloatField(max_length=5)
    dim_luas =  models.FloatField(max_length=5, default=0)
    partisi = models.CharField(max_length=1, choices= KATEGORI_PARTISI, default='P')  # lainnya 'N'
    awal_kontak_matahari = models.IntegerField(default=0)
    akhir_kontak_matahari = models.IntegerField(default=0)
    temp_rerata_ruang_berdekatan = models.FloatField(max_length=5, default=0)
    material = models.CharField(max_length=50)# perlu diset saat input data untuk kinerja komputasi, tdk perlu akses ke db
    tahanan_thermal = models.FloatField(max_length=5)



class BebanLuarPintu (models.Model):
    KATEGORI_SISI = (
        ('sisi_barat', 'Sisi Barat'),
        ('sisi_selatan', 'Sisi Selatan'),
        ('sisi_timur', 'Sisi Timur'),
        ('sisi_utara', 'Sisi Utara'),
    )
    gedung = models.ForeignKey(ProfilGedung, on_delete= models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    nama_ruang = models.CharField(max_length=50, default='ruang1')
    sisi = models.CharField(max_length=15,choices=KATEGORI_SISI)
    dim_luas = models.FloatField(max_length=5, default=0)
    dim_tebal = models.FloatField(max_length=5)
    partisi = models.CharField(max_length=1, choices= KATEGORI_PARTISI, default='P') # lainnya 'N'
    awal_kontak_matahari = models.IntegerField(max_length=1, default=0)
    akhir_kontak_matahari = models.IntegerField(max_length=1, default=0)
    temp_rerata_ruang_berdekatan = models.FloatField(max_length=5, default=0)
    material = models.CharField(max_length=50)# perlu diset saat input data untuk kinerja komputasi, tdk perlu akses ke db
    frekwensi_buka_tutup = models.IntegerField()
    waktu_pintu_terbuka = models.FloatField(max_length=5)
    tahanan_thermal = models.FloatField(max_length=5)
    frame = models.CharField(max_length=50, default = 'door frame wood caulked')


class BebanLuarKaca (models.Model):
    KATEGORI_SISI = (
        ('sisi_barat', 'Sisi Barat'),
        ('sisi_selatan', 'Sisi Selatan'),
        ('sisi_timur', 'Sisi Timur'),
        ('sisi_utara', 'Sisi Utara'),
    )
    gedung = models.ForeignKey(ProfilGedung, on_delete= models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    nama_ruang = models.CharField(max_length=50, default='ruang1')
    sisi = models.CharField(max_length=15,choices=KATEGORI_SISI)
    dim_luas = models.FloatField(max_length=5, default=0)
    dim_tebal = models.FloatField(max_length=5)
    partisi = models.CharField(max_length=1, choices=KATEGORI_PARTISI, default='P')  # lainnya 'N'
    awal_kontak_matahari = models.IntegerField(default=0)
    akhir_kontak_matahari = models.IntegerField(default=0)
    material = models.CharField(max_length=50)# perlu diset saat input data untuk kinerja komputasi, tdk perlu akses ke db
    sub_kategori_material = models.CharField(max_length=50,default='tirai gulung sedang')
    jumlah_lapisan = models.CharField(max_length=50,default='single_glass')
    jenis_frame = models.CharField(max_length=50, default='Al')
    arah = models.CharField(max_length=50)
    temp_rerata_ruang_berdekatan = models.FloatField(max_length=5, default=0)


class BebanLuarCeiling (models.Model):
    gedung = models.ForeignKey(ProfilGedung, on_delete= models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    dim_luas = models.FloatField(max_length=5)
    dim_tebal = models.FloatField(max_length=5)
    kontak_matahari = models.CharField(max_length=1)# y or n
    material = models.CharField(max_length=50)# perlu diset saat input data untuk kinerja komputasi, tdk perlu akses ke db
    tahanan_thermal = models.FloatField(max_length=5)


class BebanDalamPenghuni(models.Model):
    gedung = models.ForeignKey(ProfilGedung, on_delete=models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    nama_ruang = models.CharField(max_length=50, default='ruang1')
    aktivitas = models.CharField(max_length = 50, default='None')
    jumlah_penghuni = models.IntegerField()
    lama_aktivitas = models.IntegerField()
    total_aktivitas = models.IntegerField()
    state = models.CharField(max_length=50, default='tdk merokok')

class BebanDalamPencahayaan(models.Model):
    gedung = models.ForeignKey(ProfilGedung, on_delete=models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    nama_ruang = models.CharField(max_length=50, default='ruang1')
    jenis_lampu = models.IntegerField()
    jumlah_lampu = models.IntegerField()
    warna_cat = models.CharField(max_length=10, default='putih')

class BebanDalamPeralatan(models.Model):
    gedung = models.ForeignKey(ProfilGedung, on_delete=models.PROTECT)
    level_lantai = models.IntegerField(default=1)
    nama_ruang = models.CharField(max_length=50, default='ruang1')
    jenis_alat = models.CharField(max_length=50)
    beban = models.FloatField(max_length=5)
    jumlah = models.IntegerField(default=0)
    lama_penggunaan = models.FloatField(max_length=5, default=0)


class BebanInfiltrasiVentilasi(models.Model):
    gedung = models.ForeignKey(ProfilGedung, on_delete=models.PROTECT)
    level_lantai = models.IntegerField()
    nama_ruang = models.CharField(max_length=50, default='sekolah, kelas')
    jumlah_stop_kontak = models.IntegerField()
    kec_angin_luar = models.FloatField(max_length=5)
    kelas_shielding = models.CharField(max_length=20, default='shielding 1')
    jenis_ceiling = models.CharField(max_length=20, default='ceiling drop')


