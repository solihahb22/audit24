from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect,reverse
from .forms import ProfilGedungForm, DindingForm, PintuForm,KacaForm,CeilingForm, \
    PenghuniForm, PencahayaanForm, BebanDalamPeralatanForm, SearchProfil, BetonForm, BebanInfiltrasiVentilasiForm
from .models import ProfilGedung, BebanLuar, BebanLuarDinding, BebanLuarKaca, BebanLuarPintu, BebanDalamPenghuni,\
            BebanDalamPencahayaan, BebanDalamPeralatan, BebanLuarBeton, BebanInfiltrasiVentilasi
from django.core import serializers
from . import audit_lib
from django.db.models import Count, ProtectedError


# Create your views here.
from django.contrib.auth.decorators import login_required


def index(request):
    initial_data = {'nama': 'Gedung B Kampus A', 'alamat_lokasi': 'alamat1','dim_panjang':1, 'dim_lebar':1,
                    'dim_tinggi':1,'kolom_panjang':1,'kolom_lebar':1, 'kolom_jumlah':1,'temperatur_rh':27,'temperatur_obj':25.5}
    #form = ProfilGedungForm(initial=initial_data)
    form = ProfilGedungForm(None)
    profiles = ProfilGedung.objects.all().order_by('-id')
    context = None
    pesan = None
    edited = True
    if request.method == "POST":
        #request.session['test'] = 'session berfungsi'
        form = ProfilGedungForm(request.POST)
        if form.is_valid():
            nama = form.cleaned_data['nama']
            #alamat_lokasi = form.cleaned_data['alamat_lokasi']
            lintang = form.cleaned_data['lintang']
            posisi_lintang = form.cleaned_data['posisi_lintang']
            bujur= form.cleaned_data['bujur']
            posisi_bujur = form.cleaned_data['posisi_bujur']
            #dim_panjang = form.cleaned_data['dim_panjang']
            #dim_lebar = form.cleaned_data['dim_lebar']
            #dim_tinggi = form.cleaned_data['dim_tinggi']
            #temperatur_rh = form.cleaned_data['temperatur_rh']
            #temperatur_obj = form.cleaned_data['temperatur_obj']
            '''
            profil = ProfilGedung.objects.create(nama=nama, alamat_lokasi=alamat_lokasi, dim_panjang=dim_panjang,
                                       dim_lebar= dim_lebar, dim_tinggi=dim_tinggi, temperatur_rh=temperatur_rh,
                                       temperatur_obj=temperatur_obj )
            '''
            form.save()
            """
            request.session['profil'] = f'{nama},{alamat_lokasi},{dim_panjang},{dim_lebar},{dim_tinggi},{kolom_panjang},\
                                        {kolom_lebar},{kolom_jumlah},{temperatur_rh},{temperatur_obj}'
            """
            #gdg = dict([('nama',f'{nama}'),('alamat_lokasi',f'{alamat_lokasi}')])
            request.session['nama']=nama
            request.session['lintang'] = lintang
            request.session['posisi_lintang']= posisi_lintang
            request.session['bujur']= bujur
            request.session['posisi_bujur']=posisi_bujur
            request.session.modified = True
            profil_gdg = f'{nama},{lintang}, {posisi_lintang},{bujur},{posisi_bujur}'

            pesan = f'Profil gedung sudah dibuat, lanjut ke penentuan beban kalor luar'
            profiles = ProfilGedung.objects.all()
            context = {
                'form': form,
                'pesan': pesan,
                'profiles': profiles,
            }
            return render(request, 'bebankalor/profil_gedung.html',context)
        else:
            pesan = 'Profil gedung gagal dibuat!'
            context = {
                'form': form,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/profil_gedung.html', context)
    else:
        pesan = "Input profil gedung"
        context ={
            'form': form,
            'pesan':pesan,
            'profiles':profiles,
            'edited': edited,
        }
    return render(request, 'bebankalor/profil_gedung.html',context)

def view_profil(request,id):
    profiles = ProfilGedung.objects.all().order_by('-id')
    profil = get_object_or_404(ProfilGedung, id=id)
    request.session['id_profil'] = profil.id
    request.session['nama'] = profil.nama
    request.session['lintang'] = profil.lintang
    request.session['posisi_lintang'] = profil.posisi_lintang
    request.session['bujur'] = profil.bujur
    request.session['posisi_bujur'] = profil.posisi_bujur
    request.session.modified = True
    form = ProfilGedungForm(instance=profil)
    edited = False
    pesan = 'View Profil Gedung'
    context = {
        'form': form,
        'pesan':pesan,
        'profil':profil,
        'profiles':profiles,
        'edited': edited,
    }
    return render(request, 'bebankalor/profil_gedung.html', context)

def view_dinding(request,id):

    dinding = get_object_or_404(BebanLuarDinding, id=id)
    dindings = BebanLuarDinding.objects.filter(gedung=dinding.gedung, level_lantai=dinding.level_lantai, sisi=dinding.sisi).order_by('-sisi')

    form_dinding = DindingForm(instance=dinding)
    edited = False
    pesan = '--view'
    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    context = {
        'form_dinding': form_dinding,
        'dindings': dindings,
        'dinding': dinding,
        'pesan': pesan,
        'kat_partisi': kat_partisi,
        'edited': False,
    }
    # return redirect('bebankalor:setbebanluar',context)
    return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)

def view_kaca(request,id):
    kaca = get_object_or_404(BebanLuarKaca, id=id)
    kacas = BebanLuarKaca.objects.filter(gedung=kaca.gedung, level_lantai=kaca.level_lantai, sisi=kaca.sisi).order_by('-sisi')

    partisi = kaca.awal_kontak_matahari==0
    form_kaca = KacaForm(instance=kaca)

    edited = False
    pesan = 'View Kaca'
    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    context = {
        'form_kaca': form_kaca,
        'kacas': kacas,
        'kaca': kaca,
        'pesan': pesan,
        'kat_partisi': kat_partisi,
        'edited': False,
    }
    # return redirect('bebankalor:setbebanluar',context)
    return render(request, 'bebankalor/beban_kalor_luar_kaca.html', context)

def view_pintu(request,id):
    pintu = get_object_or_404(BebanLuarPintu, id=id)
    pintus = BebanLuarPintu.objects.filter(gedung=pintu.gedung, level_lantai=pintu.level_lantai, sisi=pintu.sisi).order_by('-sisi')

    partisi = pintu.awal_kontak_matahari==0
    form_pintu = PintuForm(instance=pintu)

    edited = False
    pesan = 'View Pintu'

    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    context = {
        'form_pintu': form_pintu,
        'pintus': pintus,
        'pintu': pintu,
        'pesan': pesan,
        'kat_partisi': kat_partisi,
        'edited': False,
    }
    # return redirect('bebankalor:setbebanluar',context)
    return render(request, 'bebankalor/beban_kalor_luar_pintu.html', context)

def view_beton(request,id):
    beton = get_object_or_404(BebanLuarBeton, id=id)
    betons = BebanLuarBeton.objects.filter(gedung=beton.gedung, level_lantai=beton.level_lantai,
                                           sisi=beton.sisi).order_by('-sisi')

    partisi = beton.partisi
    form_beton = PintuForm(instance=beton)
    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    edited = False
    pesan = 'View Beton'

    context = {
        'beton': beton,
        'form_beton': form_beton,
        'betons': betons,
        'pesan': pesan,
        'kat_partisi': kat_partisi,
        'edited': False,
    }
    # return redirect('bebankalor:setbebanluar',context)
    return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)

def view_alat(request,id):
    alat = get_object_or_404(BebanDalamPeralatan, id=id)
    alats = BebanDalamPeralatan.objects.filter(gedung=alat.gedung, level_lantai=alat.level_lantai)

    form_alat = BebanDalamPeralatanForm(instance=alat)

    edited = False
    pesan = 'View Peralatan'

    context = {
        'form_alat': form_alat,
        'alats': alats,
        'pesan': pesan,
        'edited': False,
    }
    # return redirect('bebankalor:setbebanluar',context)
    return render(request, 'bebankalor/beban_dalam_alat.html', context)

def update_profil(request,id):
    profiles = ProfilGedung.objects.all().order_by('-id')
    profil = get_object_or_404(ProfilGedung, id=id)
    form = ProfilGedungForm(instance=profil)
    edited = True
    pesan = 'Edit Profil Gedung'
    if request.method == 'POST':
        form = ProfilGedungForm(request.POST,instance=profil)
        if form.is_valid():
           form.save()
           return redirect('bebankalor:viewprofil',id = profil.id)
    context = {
        'form': form,
        'pesan':pesan,
        'profiles':profiles,
        'profile':profil,
        'edited': edited,
    }
    return render(request, 'bebankalor/profil_gedung.html', context)

def update_dinding(request,id):
    dinding = get_object_or_404(BebanLuarDinding, id=id)
    dindings = BebanLuarDinding.objects.filter(gedung=dinding.gedung, level_lantai=dinding.level_lantai).order_by('-sisi')
    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    form = DindingForm(instance=dinding)
    edited = True
    context=None
    pesan = '--edit :'+ dinding.partisi
    if request.method == 'POST':
        form = DindingForm(request.POST,instance=dinding)
        if form.is_valid():
            form.save()
            partisi = form.cleaned_data['partisi']
            if partisi == 'N':
                #temp_rerata_ruang_berdekatan = 0
                dinding.temp_rerata_ruang_berdekatan =0
            elif partisi == 'P':
                dinding.akhir_kontak_matahari = 0
                dinding.awal_kontak_matahari = 0
            dinding.save()
            context = {
                   'form_dinding': form,
                   'pesan': pesan,
                   'dindings': dindings,
                   'dinding': dinding,
                   'edited': edited,
                   'kat_partisi': kat_partisi,
            }
            return redirect('bebankalor:viewdinding',id = dinding.id)
            #return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)
        else :
            pesan += str(form.errors)
            context = {
                'form_dinding': form,
                'pesan': pesan,
                'dindings': dindings,
                'dinding': dinding,
                'edited': edited,
                'kat_partisi': kat_partisi,
            }
            return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)
    context = {
        'form_dinding': form,
        'pesan':pesan,
        'dindings':dindings,
        'dinding':dinding,
        'edited': edited,
        'kat_partisi': kat_partisi,

    }
    return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)

def update_kaca(request,id):
    kaca = get_object_or_404(BebanLuarKaca, id=id)
    kacas = BebanLuarKaca.objects.filter(gedung=kaca.gedung, level_lantai=kaca.level_lantai).order_by('-sisi')
    form = KacaForm(instance=kaca)
    edited = True
    pesan = 'Edit Spek Kaca'
    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    if request.method == 'POST':
        form = KacaForm(request.POST,instance=kaca)
        if form.is_valid():
           form.save()
           partisi = form.cleaned_data['partisi']
           if partisi == 'N':
               # temp_rerata_ruang_berdekatan = 0
               kaca.temp_rerata_ruang_berdekatan = 0
           elif partisi == 'P':
               kaca.akhir_kontak_matahari = 0
               kaca.awal_kontak_matahari = 0
           kaca.save()
           context = {
               'form_kaca': form,
               'pesan': pesan,
               'kacas': kacas,
               'kaca': kaca,
               'kat_partisi':kat_partisi,
           }
           #return redirect('bebankalor:viewkaca',id = kaca.id)
           return render(request, 'bebankalor/beban_kalor_luar_kaca.html', context)
    context = {
        'form_kaca': form,
        'pesan':pesan,
        'kacas':kacas,
        'kaca':kaca,
        'edited': edited,
        'kat_partisi': kat_partisi,
    }
    return render(request, 'bebankalor/beban_kalor_luar_kaca.html', context)

def update_pintu(request,id):
    pintu = get_object_or_404(BebanLuarPintu, id=id)
    pintus = BebanLuarPintu.objects.filter(gedung=pintu.gedung, level_lantai=pintu.level_lantai).order_by('-sisi')
    form = PintuForm(instance=pintu)
    edited = True
    pesan = 'Edit Spek Pintu'
    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    if request.method == 'POST':
        form = PintuForm(request.POST,instance=pintu)
        if form.is_valid():
           form.save()
           partisi = form.cleaned_data['partisi']
           if partisi == 'N':
               # temp_rerata_ruang_berdekatan = 0
               pintu.temp_rerata_ruang_berdekatan = 0
           elif partisi == 'P':
               pintu.akhir_kontak_matahari = 0
               pintu.awal_kontak_matahari = 0
           pintu.save()
           context = {
               'form_pintu': form,
               'pesan': pesan,
               'pintus': pintus,
               'pintu': pintu,
               'edited': edited,
               'kat_partisi': kat_partisi,
           }
           #return redirect('bebankalor:viewdinding',id = dinding.id)
           return render(request, 'bebankalor/beban_kalor_luar_pintu.html', context)
    context = {
        'form_pintu': form,
        'pesan':pesan,
        'pintus':pintus,
        'pintu':pintu,
        'edited': edited,
        'kat_partisi': kat_partisi,
    }
    return render(request, 'bebankalor/beban_kalor_luar_pintu.html', context)
def update_beton(request,id):
    beton = get_object_or_404(BebanLuarBeton, id=id)
    betons = BebanLuarBeton.objects.filter(gedung=beton.gedung, level_lantai=beton.level_lantai).order_by('-sisi')
    form = BetonForm(instance=beton)
    edited = True
    pesan = 'Edit Spek Pintu'
    kat_partisi = [
        ("P", 'Partisi'),
        ('N', 'Non Partisi'),
    ]
    if request.method == 'POST':
        form = BetonForm(request.POST,instance=beton)
        if form.is_valid():
           form.save()
           partisi = form.cleaned_data['partisi']
           if partisi == 'N':
               # temp_rerata_ruang_berdekatan = 0
               beton.temp_rerata_ruang_berdekatan = 0
           elif partisi == 'P':
               beton.akhir_kontak_matahari = 0
               beton.awal_kontak_matahari = 0
           beton.save()
           context = {
               'form_beton': form,
               'pesan': pesan,
               'betons': betons,
               'beton': beton,
               'edited': edited,
               'kat_partisi':kat_partisi,
           }
           #return redirect('bebankalor:viewdinding',id = dinding.id)
           return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)
    context = {
        'form_beton': form,
        'pesan':pesan,
        'betons':betons,
        'beton':beton,
        'edited': edited,
        'kat_partisi': kat_partisi,
    }
    return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)

def update_penghuni(request,id):
    penghuni = get_object_or_404(BebanDalamPenghuni, id=id)
    form = PenghuniForm(instance=penghuni)
    edited = True
    pesan = 'Edit Data Penghuni'
    if request.method == 'POST':
        form = PenghuniForm(request.POST, instance=penghuni)
        if form.is_valid():
            form.save()
            context = {
                'form_penghuni': form,
                'pesan': pesan,
                'penghuni': penghuni,
                'edited': edited,
            }
            # return redirect('bebankalor:viewdinding',id = dinding.id)
            return render(request, 'bebankalor/beban_dalam_penghuni.html', context)
    context = {
        'form_penghuni': form,
        'pesan': pesan,
        'penghuni': penghuni,
        'edited': edited,
    }
    return render(request, 'bebankalor/beban_dalam_penghuni.html', context)

def update_cahaya(request,id):
    cahaya = get_object_or_404(BebanDalamPencahayaan, id=id)
    cahayas = BebanDalamPencahayaan.objects.filter(gedung=cahaya.gedung, level_lantai=cahaya.level_lantai)
    form = PencahayaanForm(instance=cahaya)
    edited = True
    pesan = 'Edit Data Pencahayaan'
    if request.method == 'POST':
        form = PencahayaanForm(request.POST, instance=cahaya)
        if form.is_valid():
            form.save()
            context = {
                'form_cahaya': form,
                'pesan': pesan,
                'cahaya': cahaya,
                'cahayas': cahayas,
                'edited': edited,
            }
            # return redirect('bebankalor:viewdinding',id = dinding.id)
            return render(request, 'bebankalor/beban_dalam_cahaya.html', context)
    else:
        context = {
            'form_cahaya': form,
            'pesan': pesan,
            'cahaya': cahaya,
            'cahayas': cahayas,
            'edited': edited,
        }
        return render(request, 'bebankalor/beban_dalam_cahaya.html', context)

def update_alat(request,id):
    alat = get_object_or_404(BebanDalamPeralatan, id=id)
    alats = BebanDalamPeralatan.objects.filter(gedung=alat.gedung, level_lantai=alat.level_lantai)
    form = BebanDalamPeralatanForm(instance=alat)
    edited = True
    pesan = 'Edit Data Pencahayaan'
    if request.method == 'POST':
        form = BebanDalamPeralatanForm(request.POST, instance=alat)
        if form.is_valid():
            form.save()
            context = {
                'form_alat': form,
                'pesan': pesan,
                'alat': alat,
                'alats': alats,
                'edited': edited,
            }
            # return redirect('bebankalor:viewdinding',id = dinding.id)
            return render(request, 'bebankalor/beban_dalam_alat.html', context)
    else:
        context = {
            'form_alat': form,
            'pesan': pesan,
            'alat': alat,
            'alats': alats,
            'edited': edited,
        }
        return render(request, 'bebankalor/beban_dalam_alat.html', context)

def update_infven(request,id):
    inf = get_object_or_404(BebanInfiltrasiVentilasi, id=id)
    form = BebanInfiltrasiVentilasiForm(instance=inf)
    edited = True
    pesan = 'Edit Data Penghuni'
    if request.method == 'POST':
        form = BebanInfiltrasiVentilasiForm(request.POST, instance=inf)
        if form.is_valid():
            form.save()
            context = {
                'form_inv': form,
                'pesan': pesan,
                'beban_inv': inf,
                'edited': edited,
            }
            # return redirect('bebankalor:viewdinding',id = dinding.id)
            return render(request, 'bebankalor/beban_infiltrasi_d_ventilasi.html', context)
    context = {
        'form_inv': form,
        'pesan': pesan,
        'beban_inv': inf,
        'edited': edited,
    }
    return render(request, 'bebankalor/beban_infiltrasi_d_ventilasi.html', context)

def delete_profil(request,id):
    pg = get_object_or_404(ProfilGedung, id=id)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            pg.delete()
            return HttpResponseRedirect(reverse('bebankalor:index'))
        except ProtectedError:
            judul = 'Tambahkan Identitas Unit Boiler'
            profiles = ProfilGedung.objects.all()
            form = ProfilGedungForm(None)
            pesan = "Unit boiler tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'profiles': profiles,
                'error': True,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/profil_gedung.html', context)
    else:
        context = {
            'object': pg,
        }
        return render(request, 'bebankalor/confirm_deletepg.html', context)

def delete_dinding(request,id):
    dinding = get_object_or_404(BebanLuarDinding, id=id)
    dindings = BebanLuarDinding.objects.filter(gedung=dinding.gedung,
                                               level_lantai=dinding.level_lantai).order_by('-sisi')
    form = DindingForm(instance=dinding)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            dinding.delete()
            return HttpResponseRedirect(reverse('bebankalor:setdinding'))
        except ProtectedError:
            judul = 'Tambahkan Dinding'
            form = ProfilGedungForm(None)
            pesan = "Dinding tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'error': True,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)
    else:
        context = {
            'object': dinding,
        }
        return render(request, 'bebankalor/confirm_deletedinding.html', context)

def delete_kaca(request,id):
    kaca = get_object_or_404(BebanLuarDinding, id=id)
    kacas = BebanLuarKaca.objects.filter(gedung=kaca.gedung,
                                               level_lantai=kaca.level_lantai).order_by('-sisi')
    form = KacaForm(instance=kaca)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            kaca.delete()
            return HttpResponseRedirect(reverse('bebankalor:setkaca'))
        except ProtectedError:
            judul = 'Tambahkan Kaca'
            form = KacaForm(None)
            pesan = "Kaca tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'error': True,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/beban_kalor_luar_kaca.html', context)
    else:
        context = {
            'object': kaca,
        }
        return render(request, 'bebankalor/confirm_deletekaca.html', context)

def delete_beton(request,id):
    beton = get_object_or_404(BebanLuarBeton, id=id)
    betons = BebanLuarBeton.objects.filter(gedung=beton.gedung,
                                                   level_lantai=beton.level_lantai).order_by('-sisi')
    form = BetonForm(instance=beton)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            beton.delete()
            return HttpResponseRedirect(reverse('bebankalor:setbeton'))
        except ProtectedError:
            judul = 'Tambahkan Beton'
            form = BetonForm(None)
            pesan = "Beton tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'error': True,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)
    else:
        context = {
            'object': beton,
        }
        return render(request, 'bebankalor/confirm_deletebeton.html', context)

def delete_pintu(request, id):
    pintu = get_object_or_404(BebanLuarPintu, id=id)
    pintus = BebanLuarPintu.objects.filter(gedung=pintu.gedung,
                                                   level_lantai=pintu.level_lantai).order_by('-sisi')
    form = PintuForm(instance=pintu)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            pintu.delete()
            return HttpResponseRedirect(reverse('bebankalor:setpintu'))
        except ProtectedError:
            judul = 'Tambahkan Pintu'
            form = PintuForm(None)
            pesan = "Pintu tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'error': True,
                'pesan': pesan,
                }
            return render(request, 'bebankalor/beban_kalor_luar_pintu.html', context)
    else:
        context = {
           'object': pintu,
        }
        return render(request, 'bebankalor/confirm_deletepintu.html', context)

def delete_penghuni(request, id):
    penghuni = get_object_or_404(BebanDalamPenghuni, id=id)
    form = PenghuniForm(instance=penghuni)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            penghuni.delete()
            return HttpResponseRedirect(reverse('bebankalor:setppenghuni'))
        except ProtectedError:
            judul = 'Tambahkan Penghuni'
            form = PintuForm(None)
            pesan = "Pintu tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'error': True,
                'pesan': pesan,
                }
            return render(request, 'bebankalor/beban_dalam_penghuni.html', context)
    else:
        context = {
           'object': penghuni,
        }
        return render(request, 'bebankalor/confirm_deletepenghuni.html', context)

def delete_cahaya(request, id):
    cahaya = get_object_or_404(BebanDalamPencahayaan, id=id)
    #cahayas = BebanDalamPencahayaan.objects.filter(gedung=cahaya.gedung, level_lantai=cahaya.level_lantai)
    form = PencahayaanForm(instance=cahaya)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            cahaya.delete()
            return HttpResponseRedirect(reverse('bebankalor:setcahaya'))
        except ProtectedError:
            judul = 'Tambahkan Pencahayaan'
            form = PencahayaanForm(None)
            pesan = "Pencahayaan tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'error': True,
                'pesan': pesan,
                }
            return render(request, 'bebankalor/beban_dalam_cahaya.html', context)
    else:
        context = {
           'object': cahaya,
        }
        return render(request, 'bebankalor/confirm_deletecahaya.html', context)

def delete_alat(request, id):
    alat = get_object_or_404(BebanDalamPeralatan, id=id)
    #cahayas = BebanDalamPencahayaan.objects.filter(gedung=cahaya.gedung, level_lantai=cahaya.level_lantai)
    form = BebanDalamPeralatanForm(instance=alat)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            alat.delete()
            return HttpResponseRedirect(reverse('bebankalor:setalat'))
        except ProtectedError:
            judul = 'Tambahkan Peralatan'
            form = BebanDalamPeralatanForm(None)
            pesan = "Pencahayaan tidak bisa dihapus"
            context = {
                'judul': judul,
                'form': form,
                'error': True,
                'pesan': pesan,
                }
            return render(request, 'bebankalor/beban_dalam_alat.html', context)
    else:
        context = {
           'object': alat,
        }
        return render(request, 'bebankalor/confirm_deletealat.html', context)
def delete_infven(request,id):
    beban_inv = get_object_or_404(BebanInfiltrasiVentilasi, id=id)
    form_inv = BebanInfiltrasiVentilasiForm(instance=beban_inv)
    context = {}
    pesan = None
    error = False
    if request.method == "POST":
        try:
            beban_inv.delete()
            return HttpResponseRedirect(reverse('bebankalor:setinfiltrasiventilasi'))
        except ProtectedError:
            judul = 'Tambahkan Inviltrasi Ventilasi'
            form = BebanInfiltrasiVentilasiForm(None)
            pesan = "Inviltrasi ventilasi tidak bisa dihapus"

            context = {
                'judul': judul,
                'form_inv': form,
                'beban_inv': beban_inv,
                'error': True,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/beban_infiltrasi_d_ventilasi.html', context)
    else:
        context = {
           'object': beban_inv,
        }
        return render(request, 'bebankalor/confirm_deleteinv.html', context)


def set_dinding_bl(request):
    pesen = None
    partisi = True
    dinding = []
    nama = None
    form = None
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session\
            and 'bujur' in request.session and 'posisi_bujur' in request.session :
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']
        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();

        if request.method == "POST":
            form = DindingForm(request.POST)
            if form.is_valid():
                #kategori = form.cleaned_data['kategori']
                kategori ="dinding"
                sisi = form.cleaned_data['sisi']
                dim_panjang = form.cleaned_data['dim_panjang']
                dim_lebar = form.cleaned_data['dim_lebar']
                dim_tebal = form.cleaned_data['dim_tebal']
                kontak_matahari = form.cleaned_data['kontak_matahari']
                material = form.cleaned_data['material']
                tahanan_thermal = audit_lib.tahanan_thermal_dinding.get(material)
                # define spek dinding
                data_dinding = BebanLuar.objects.create(gedung = gedung,kategori = kategori, sisi = sisi,
                                                        dim_panjang = dim_panjang, dim_lebar = dim_lebar,
                                                        kontak_matahari = kontak_matahari, material = material,
                                                        tahanan_thermal = tahanan_thermal)
                data_dinding_list = serializers.serialize('json', data_dinding)
               # add to session
                if 'dinding_bl' in request.session:
                    dinding = request.session['dinding_bl']
                    dinding.append(data_dinding_list)
                    request.session['dinding_bl']=dinding
                else:
                    request.session['dinding_bl'] = [data_dinding_list]
                    dinding.append(data_dinding_list)
                pesan = "data dinding berhasil di set"
                request.session.modified = True
                form_dinding = DindingForm(None)
                context = {
                    'form_dinding':form_dinding,
                    'spek':dinding,
                    'pesan':pesan,
                    'partisi':partisi,
                }
                #return redirect('bebankalor:setbebanluar',context)
                return render(request,'bebankalor/beban_kalor_luar_perbagian.html',context)
            else:
                pesan = "form is not valid"
                context = {
                    'form_dinding': form,
                    'pesan': pesan,
                    'partisi': partisi,
                }
                # return redirect('bebankalor:setbebanluar',context)
                return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)

        else:

            form_dinding = DindingForm(None)
            form_dinding.fields['gedung'].initial = gedung
            pesan = "set dinding belum "
            partisi = True
            context = {
                'form_dinding': form_dinding,
                'partisi': partisi,
                'pesan': pesan,
                'nama':nama,

            }
            return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)
            #return redirect('bebankalor:setbebanluar', context)

def view_spek(request):
    profil =None
    dinding =None
    kaca = None
    dinding = None
    pintu = None
    beton = None
    penghuni = None
    cahayas = None
    status = None
    context = None
    if request.method == 'POST'and 'search_profil_btn'in request.POST:
        form = SearchProfil(request.POST)
        if form.is_valid():
            gedung = form.cleaned_data['gedung']
            lantai = form.cleaned_data['lantai'] #asumsi satu lantai satu ruangan
            try:
                profil = ProfilGedung.objects.filter(nama=gedung.nama).first()
                #lakukan pencarian dinding, kaca, pintu,
                dinding = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
                kaca = BebanLuarKaca.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
                pintu = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
                beton = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
                penghuni = BebanDalamPenghuni.objects.filter(gedung=gedung, level_lantai=lantai).first()
                cahayas = BebanDalamPencahayaan.objects.filter(gedung=gedung, level_lantai=lantai)
                alats = BebanDalamPeralatan.objects.filter(gedung=gedung, level_lantai=lantai)
                status = True
                context ={
                    'status': status,
                    'profil':profil,
                    'dindings': dinding,
                    'kacas': kaca,
                    'pintus': pintu,
                    'betons': beton,
                    'penghuni': penghuni,
                    'cahayas': cahayas,
                    'alats': alats,
                    'form':form,
                }
            except ProfilGedung.DoesNotExist:
                status = False
                context ={
                    'status': status,
                }
            return render(request, 'bebankalor/profil_d_spesifikasi.html', context)
    else:
        search_form = SearchProfil(None)
        context = {
            'status': status,
            'form': search_form,
        }
        return render(request, 'bebankalor/profil_d_spesifikasi.html', context)


def set_beban_luar(request):
    initial_data = { 'dim_panjang': 1, 'dim_lebar': 1, 'dim_tebal': 1 }
    initial_data_pintu = { 'dim_panjang': 1, 'dim_lebar': 1, 'dim_tebal': 1}
    dindings =None
    pintus = None
    kacas = None
    betons = None
    context =None
    gedung = None
    form_dinding = DindingForm(initial=initial_data)
    form_pintu = PintuForm(initial=initial_data_pintu)
    form_kaca = KacaForm(initial=initial_data_pintu)
    form_beton = BetonForm()
    #if 'pesanprofil' in request.session:
    #if 'nama' in request.session and 'alamat' in request.session:
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session\
            and 'bujur' in request.session and 'posisi_bujur' in request.session and request.method =="POST":
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']
        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();

        pesan = f'profil {nama}, {lintang} {posisi_lintang},{bujur} { posisi_bujur} sudah diset'
    else:
        pesan = "profil gedung belum diset"

    if request.method =="POST" and 'add_dinding_btn' in request.POST:
        form_dinding = DindingForm(request.POST)
        if form_dinding.is_valid():
                gedung = form_dinding.cleaned_data['gedung']
                lantai = form_dinding.cleaned_data['level_lantai']
                sisi = form_dinding.cleaned_data['sisi']
                material = form_dinding.cleaned_data['material']
                form_dinding.instance.tahanan_thermal = audit_lib.tahanan_thermal_dinding.get(material)
                form_dinding.save()
                dindings = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai, sisi=sisi).order_by('-sisi')

                pesan = "data dinding berhasil diset"
                context = {
                    'dindings': dindings,
                    'form_dinding': form_dinding,
                    'form_pintu': form_pintu,
                    'form_kaca': form_kaca,
                    'pesan': pesan,
                }
                return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)
        else:
            pesan += "form tidak valid"
            context = {
                'form_dinding': form_dinding,
                'form_pintu': form_pintu,
                'form_kaca': form_kaca,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)
    elif request.method == "POST" and 'add_pintu_btn' in request.POST:
        form_pintu = PintuForm(request.POST)
        if form_pintu.is_valid():
            material = form_pintu.cleaned_data['material']
            lantai = form_pintu.cleaned_data['level_lantai']
            sisi = form_pintu.cleaned_data['sisi']
            form_pintu.instance.tahanan_thermal = audit_lib.tahanan_thermal_pintu.get(material)
            form_pintu.save()
            pesan ='pintu berhasil diset'
            pintus = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai, sisi=sisi).order_by('-sisi')

            context = {
                'form_dinding': form_dinding,
                'form_pintu': form_pintu,
                'form_kaca': form_kaca,
                'pesan_pintu': pesan,
                'pintus': pintus
            }
            return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)
        else:
            pesan += "form tidak valid"
            context = {
                'form_dinding': form_dinding,
                'form_pintu': form_pintu,
                'form_kaca': form_kaca,
                'pesan': pesan,
            }
            return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)
    elif request.method == "POST" and 'add_kaca_btn' in request.POST:
        form_kaca = KacaForm(request.POST)
        if form_kaca.is_valid():
            lantai = form_kaca.cleaned_data['level_lantai']
            sisi = form_kaca.cleaned_data['sisi']
            form_kaca.save()
            pesan = 'kaca berhasil diset'
            kacas = BebanLuarKaca.objects.filter(gedung=gedung, level_lantai=lantai, sisi=sisi).order_by('-sisi')
        else:
            pesan += "form tidak valid"
        context = {
            'form_dinding': form_dinding,
            'form_pintu': form_pintu,
            'form_kaca': form_kaca,
            'pesan': pesan,
            'kacas': kacas,
        }
        return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)

    elif request.method == "POST" and 'add_beton_btn' in request.POST:
        form_beton = BetonForm(request.POST)
        if form_beton.is_valid():
            gedung = form_beton.cleaned_data['gedung']
            level_lantai = form_beton.cleaned_data['level_lantai']
            nama_ruang = form_beton.cleaned_data['nama_ruang']
            sisi = form_beton.cleaned_data['sisi']
            dim_tebal = form_beton.cleaned_data['dim_tebal']
            dim_luas = form_beton.cleaned_data['dim_luas']
            material = form_beton.cleaned_data['material']
            form_beton.save()
            pesan = 'beton berhasil diset'
            betons = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=level_lantai,nama_ruang=nama_ruang, sisi=sisi).order_by('-sisi')
        else:
            pesan += "form beton tidak valid"
        context = {
            'form_dinding': form_dinding,
            'form_pintu': form_pintu,
            'form_kaca': form_kaca,
            'form_beton':form_beton,
            'pesan': pesan,
            'beton': betons,
        }
        return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)
    else:
        context = {
            'form_dinding': form_dinding,
            'form_pintu': form_pintu,
            'form_kaca': form_kaca,
            'form_beton': form_beton,
            'pesan': pesan,
        }
    return render(request, 'bebankalor/beban_kalor_luar_perbagian.html', context)

def set_bl_kaca(request):
    pesan = ''
    context = None
    kacas = None
    edited = True
    add_bl = True
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang, posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();

        initial_data = {'gedung': gedung}
        kacas = BebanLuarKaca.objects.filter(gedung=gedung).order_by('-sisi')
        form_kaca = KacaForm()
        form_kaca.fields['gedung'].initial = gedung
        kat_partisi = [
            ("P", 'Partisi'),
            ('N', 'Non Partisi'),
        ]
        if request.method == "POST" and 'add_kaca_btn' in request.POST:
            form_kaca = KacaForm(request.POST)
            if form_kaca.is_valid():
                gedung = form_kaca.cleaned_data['gedung']
                lantai = form_kaca.cleaned_data['level_lantai']
                ruang = form_kaca.cleaned_data['nama_ruang']
                form_kaca.save()
                pesan = 'kaca berhasil diset'
                kacas = BebanLuarKaca.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang).order_by('-sisi')
            else:
                pesan += "form tidak valid"
            context = {
                'form_kaca': form_kaca,
                'pesan': pesan,
                'kacas': kacas,
                'kat_partisi': kat_partisi,
                'add_bl': add_bl,
            }
            return render(request, 'bebankalor/beban_kalor_luar_kaca.html', context)
        else:
            pesan += nama
            context = {
                'form_kaca': form_kaca,
                'kacas': kacas,
                'nama': nama,
                'kat_partisi': kat_partisi,
                'edited':edited,
                'add_bl': add_bl,

            }
            return render(request, 'bebankalor/beban_kalor_luar_kaca.html', context)

def set_bl_dinding(request):
    edited = True
    add_bl = True
    context = None
    pesan = ''
    dindings = None
    nama = None
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();

        # ambil data dinding
        #dindings = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=gedung.level_lantai, nama_ruang=gedung.nama_ruang).order_by('-sisi')
        dindings = BebanLuarDinding.objects.filter(gedung=gedung).order_by('-sisi')
        #dinding = BebanLuarDinding.objects.filter(gedung=gedung).first()
        #pesan = Count(dindings)
        #initial_data = {'dinding':dinding}
        form_dinding = DindingForm(None)
        form_dinding.fields['gedung'].initial = gedung
        kat_partisi = [
            ("P", 'Partisi'),
            ('N', 'Non Partisi'),
        ]
        if request.method =="POST" and 'add_dinding_btn' in request.POST:
                form_dinding = DindingForm(request.POST)
                if form_dinding.is_valid():
                        gedung = form_dinding.cleaned_data['gedung']
                        lantai = form_dinding.cleaned_data['level_lantai']
                        ruang = form_dinding.cleaned_data['nama_ruang']
                        sisi = form_dinding.cleaned_data['sisi']
                        material = form_dinding.cleaned_data['material']
                        form_dinding.instance.tahanan_thermal = audit_lib.tahanan_thermal_dinding.get(material)
                        form_dinding.save()
                        dindings = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang).order_by('-sisi')
                        request.session['lantai']=lantai
                        request.session['ruang']=ruang
                        pesan = "data dinding berhasil diset"
                        context = {
                            'dindings': dindings,
                            'form_dinding': form_dinding,
                            'pesan': pesan,
                            'kat_partisi': kat_partisi,
                        }
                        return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)
                else:
                    pesan += "form tidak valid"
                    pesan += str(form_dinding.errors)
                    context = {
                        'form_dinding': form_dinding,
                        'kat_partisi': kat_partisi,
                        'pesan': pesan,
                    }
                    return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)

        if 'lantai' in request.session and 'ruang'in request.session:
           lantai = request.session['lantai']
           ruang = request.session['ruang']
           dindings = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang).order_by(
                '-sisi')

        selected_kategori = 'not_spesified'
        context = {
            'form_dinding': form_dinding,
            'dindings':dindings,
            'nama':nama,
            'edited': edited,
            'kat_partisi':kat_partisi,
            'add_bl': add_bl,

        }
        return render(request, 'bebankalor/beban_kalor_luar_dinding.html', context)

def set_bl_pintu(request):
    context =None
    edited = True
    partisi = None
    add_bl = True
    pesan = ''
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();
        """
        if nama is None :
            nama = 'gedung belum diset, nama bertipe null'
        """
        pintu = BebanLuarPintu.objects.filter(gedung=gedung).order_by('-sisi').first()
        initial_data = {'pintu':pintu}
        pintus = BebanLuarPintu.objects.filter(gedung=gedung).order_by('-sisi')
        form_pintu = PintuForm(None)
        form_pintu.fields['gedung'].initial = gedung
        kat_partisi = [
            ("P", 'Partisi'),
            ('N', 'Non Partisi'),
        ]
        if request.method == "POST" and 'add_pintu_btn' in request.POST:
            form_pintu = PintuForm(request.POST)
            if form_pintu.is_valid():
                gedung = form_pintu.cleaned_data['gedung']
                material = form_pintu.cleaned_data['material']
                lantai = form_pintu.cleaned_data['level_lantai']
                sisi = form_pintu.cleaned_data['sisi']
                ruang = form_pintu.cleaned_data['nama_ruang']
                form_pintu.instance.tahanan_thermal = audit_lib.tahanan_thermal_pintu.get(material)
                form_pintu.save()
                pesan = 'pintu berhasil diset'
                pintus = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang).order_by('-sisi')

                context = {
                    'form_pintu': form_pintu,
                    'pintus': pintus,
                    'kat_partisi': kat_partisi,
                }
                return render(request, 'bebankalor/beban_kalor_luar_pintu.html', context)
            else:
                pesan += "form tidak valid"
                context = {
                    'form_pintu': form_pintu,
                    'pintus': pintus,
                    'pesan': pesan,
                    'kat_partisi': kat_partisi,
                }
                return render(request, 'bebankalor/beban_kalor_luar_pintu.html', context)
        else:
            pesan += nama

            context = {
                'form_pintu': form_pintu,
                'kat_partisi': kat_partisi,
                'pesan': pesan,
                'pintus': pintus,
                'nama': nama,
                'add_bl': add_bl,
                'edited': edited,
            }
            return render(request, 'bebankalor/beban_kalor_luar_pintu.html', context)

def cek_profil_aktif(request):
    gedung = None
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();
    return gedung
def set_bl_beton(request):
    pesan = ''
    add_bl = True
    context = None
    betons= None
    edited = True
    form_beton = BetonForm()
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();
        """
        if nama is None :
            nama = 'gedung belum diset, nama bertipe null'
        """
        #beton = BebanLuarBeton.objects.filter(gedung=gedung).order_by('-sisi').first()
        #initial_data = {'beton':beton}
        betons = BebanLuarBeton.objects.filter(gedung=gedung).order_by('-sisi')

        form_beton= BetonForm()
        form_beton.fields['gedung'].initial = gedung
        kat_partisi = [
            ("P", 'Partisi'),
            ('N', 'Non Partisi'),
        ]
        if request.method == "POST" and 'add_beton_btn' in request.POST:
            form_beton = BetonForm(request.POST)
            if form_beton.is_valid():
                gedung = form_beton.cleaned_data['gedung']
                level_lantai = form_beton.cleaned_data['level_lantai']
                nama_ruang = form_beton.cleaned_data['nama_ruang']
                sisi = form_beton.cleaned_data['sisi']
                material = form_beton.cleaned_data['material']
                form_beton.instance.tahanan_thermal = audit_lib.tahanan_thermal_beton.get(material)
                form_beton.save()
                pesan = 'beton berhasil diset'
                betons = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=level_lantai, nama_ruang=nama_ruang).order_by('-sisi')

            context = {
                'form_beton': form_beton,
                'pesan': pesan,
                'betons': betons,
                'kat_partisi': kat_partisi,
            }
            return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)
        else:
            context = {
                'form_beton': form_beton,
                'edited': edited,
                'pesan': pesan,
                'betons': betons,
                'nama': nama,
                'kat_partisi': kat_partisi,
                'add_bl': add_bl,
            }
            return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)


def set_bl_ceiling(request):
    pesan = ''
    context = None
    ceilings= None
    form_ceiling = CeilingForm()
    if request.method == "POST" and 'add_ceiling_btn' in request.POST:
        form_ceiling = BetonForm(request.POST)
        if form_ceiling.is_valid():
            gedung = form_ceiling.cleaned_data['gedung']
            level_lantai = form_ceiling.cleaned_data['level_lantai']
            nama_ruang = form_ceiling.cleaned_data['nama_ruang']
            material = form_ceiling.cleaned_data['material']
            form_ceiling.instance.tahanan_thermal = audit_lib.tahanan_thermal_plafon.get(material)
            form_ceiling.save()
            pesan = 'beton berhasil diset'
            #untuk satu ruangan satu kategori material
            ceilings = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=level_lantai, nama_ruang=nama_ruang).order_by('-sisi')

        context = {
            'form_ceiling': form_ceiling,
            'pesan': pesan,
            'ceilings': ceilings,
        }
        return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)
    else:
        context = {
            'form_ceiling': form_ceiling,
            'pesan': pesan,
            'ceiling': ceilings,
        }
        return render(request, 'bebankalor/beban_kalor_luar_beton.html', context)

def set_beban_dalam(request):
    cahayas =None
    penghunis = None
    alats = None
    pencahayaan_form = PencahayaanForm(None)
    penghuni_form = PenghuniForm(None)
    alat_form = BebanDalamPeralatanForm(None)
    pesan = 'set beban dalam'
    pesan_alat = 'set beban dalam peralatan'
    pesan_penghuni = 'set beban dalam penghuni'
    firtsadd = True
    if request.method =="POST" and 'add_penghuni_btn' in request.POST:
        penghuni_form = PenghuniForm(request.POST)
        if penghuni_form.is_valid():
            #save data penghuni
            penghuni_form.save()
            gedung = penghuni_form.cleaned_data['gedung']
            lantai = penghuni_form.cleaned_data['level_lantai']
            ruang = penghuni_form.cleaned_data['nama_ruang']
            penghunis = BebanDalamPenghuni.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang).order_by('id').first();
            firstadd = False
            context = {
                'firstadd':firstadd,
                'form_penghuni': penghuni_form,
                'form_cahaya': pencahayaan_form,
                'form_alat': alat_form,
                'penghuni': penghunis,
                'cahayas': cahayas,
                'alats': alats,
                'pesan': pesan,
            }
    elif request.method =="POST" and 'add_cahaya_btn' in request.POST:
        pencahayaan_form = PencahayaanForm(request.POST)
        if pencahayaan_form.is_valid():
            #save data pencahayaan
            pencahayaan_form.save()
            gedung = pencahayaan_form.cleaned_data['gedung']
            lantai = pencahayaan_form.cleaned_data['level_lantai']
            ruang = pencahayaan_form.cleaned_data['nama_ruang']
            cahayas = BebanDalamPencahayaan.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang)
            #tambahkan data ke session
            context = {
                'form_penghuni': penghuni_form,
                'form_cahaya': pencahayaan_form,
                'form_alat': alat_form,
                'penghuni': penghunis,
                'cahayas': cahayas,
                'alats': alats,
                'pesan': pesan,
            }
    elif request.method =="POST" and 'add_alat_btn' in request.POST:
        alat_form = BebanDalamPeralatanForm(request.POST)
        if alat_form.is_valid():
            #save data pencahayaan
            alat_form.save()
            gedung = alat_form.cleaned_data['gedung']
            lantai = alat_form.cleaned_data['level_lantai']
            ruang = alat_form.cleaned_data['nama_ruang']
            alats = BebanDalamPeralatan.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang)
            #tambahkan data ke session
            context = {
                'firstadd': firtsadd,
                'form_penghuni': penghuni_form,
                'form_cahaya': pencahayaan_form,
                'form_alat': alat_form,
                'penghunis': penghunis,
                'cahayas': cahayas,
                'alats': alats,
                'pesan': pesan,
            }
    else:
        pesan = "Masukkan data beban dalam"
        context = {
            'firstadd': firtsadd,
            'form_penghuni': penghuni_form,
            'form_cahaya': pencahayaan_form,
            'form_alat': alat_form,
            'penghunis': penghunis,
            'cahayas': cahayas,
            'alats': alats,
            'pesan': pesan,
        }

    return render(request, 'bebankalor/beban_dalam.html',context)

def set_bd_alat(request):
    alats = None
    alat_form = BebanDalamPeralatanForm(None)
    pesan_alat = 'set beban dalam peralatan'
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang, posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();
        alats = BebanDalamPeralatan.objects.filter(gedung=gedung)

        if request.method =="POST" and 'add_alat_btn' in request.POST:
            alat_form = BebanDalamPeralatanForm(request.POST)
            if alat_form.is_valid():
                #save data pencahayaan
                alat_form.save()
                gedung = alat_form.cleaned_data['gedung']
                lantai = alat_form.cleaned_data['level_lantai']
                ruang = alat_form.cleaned_data['nama_ruang']
                alats = BebanDalamPeralatan.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang)
                pesan = 'Peralatan berhasil ditambahkan'
                #tambahkan data ke session
                context = {
                    'form_alat': alat_form,
                    'alats': alats,
                    'pesan': pesan,
                }
                return render(request, 'bebankalor/beban_dalam_alat.html', context)
        else:
            pesan = "Masukkan data beban dalam peralatan"
            context = {
                'form_alat': alat_form,
                'pesan': pesan,
                'alats': alats,
            }

            return render(request, 'bebankalor/beban_dalam_alat.html',context)

def set_bd_cahaya(request):
    cahayas =None
    pencahayaan_form = PencahayaanForm(None)
    pesan = 'set beban dalam pencahayaan'
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();
        cahayas = BebanDalamPencahayaan.objects.filter(gedung=gedung)
        #cahaya = BebanDalamPencahayaan.objects.get(gedung=gedung)
        #initial_data = {'cahaya': cahaya}
        #pencahayaan_form = PencahayaanForm(initial=initial_data)

        if request.method =="POST" and 'add_cahaya_btn' in request.POST:
            pencahayaan_form = PencahayaanForm(request.POST)
            if pencahayaan_form.is_valid():
                #save data pencahayaan
                pencahayaan_form.save()
                gedung = pencahayaan_form.cleaned_data['gedung']
                lantai = pencahayaan_form.cleaned_data['level_lantai']
                ruang = pencahayaan_form.cleaned_data['nama_ruang']
                cahayas = BebanDalamPencahayaan.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang)
                #tambahkan data ke session
                pesan ='Pencahayaan berhasil di set'
                context = {
                    'form_cahaya': pencahayaan_form,
                    'cahayas': cahayas,
                    'pesan': pesan,
                }

        else:
                pesan = "Masukkan data beban dalam pencahayaan"
                context = {
                    'form_cahaya': pencahayaan_form,
                    'cahayas': cahayas,
                    'pesan': pesan,
                }

        return render(request, 'bebankalor/beban_dalam_cahaya.html',context)

def set_bd_penghuni(request):
    penghuni = None
    penghuni_form = PenghuniForm(None)
    pesan_penghuni = 'set beban dalam penghuni'
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();
        try:
            penghuni = BebanDalamPenghuni.objects.get(gedung=gedung)
            initial_data = {'penghuni': penghuni}
            penghuni_form = PenghuniForm(initial=initial_data)
            pesan_penghuni = 'data penghuni sudah ada'
            context = {
                'form_penghuni': penghuni_form,
                'penghuni': penghuni,
                'pesan': pesan_penghuni,
            }
            return render(request, 'bebankalor/beban_dalam_penghuni.html', context)
        except:
            if request.method =="POST" and 'add_penghuni_btn' in request.POST:
                penghuni_form = PenghuniForm(request.POST)
                if penghuni_form.is_valid():
                    #save data penghuni
                    #penghuni_form.save()
                    gedung = penghuni_form.cleaned_data['gedung']
                    lantai = penghuni_form.cleaned_data['level_lantai']
                    ruang = penghuni_form.cleaned_data['nama_ruang']
                    penghuni_form.save()
                    penghuni = BebanDalamPenghuni.objects.get(gedung=gedung, level_lantai=lantai, nama_ruang=ruang)
                    pesan_penghuni = 'data penghuni berhasil diset'
                    context = {
                        'form_penghuni': penghuni_form,
                        'penghuni': penghuni,
                        'pesan': pesan_penghuni,
                    }
                    return render(request, 'bebankalor/beban_dalam_penghuni.html', context)
            else:
                pesan_penghuni = "Masukkan data beban dalam Penghuni"
                context = {
                    'form_penghuni': penghuni_form,
                    'penghuni': penghuni,
                    'pesan': pesan_penghuni,
                }
                return render(request, 'bebankalor/beban_dalam_penghuni.html',context)

def set_infiltrasi_ventilasi(request):
    pesan = None
    beban_inv = None
    if 'nama' in request.session and 'lintang' in request.session and 'posisi_lintang' in request.session and \
            'bujur' in request.session and 'posisi_bujur' in request.session:
        nama = request.session['nama']
        lintang = request.session['lintang']
        posisi_lintang = request.session['posisi_lintang']
        bujur = request.session['bujur']
        posisi_bujur = request.session['posisi_bujur']

        gedung = ProfilGedung.objects.filter(nama=nama, lintang=lintang,posisi_lintang=posisi_lintang,
                                             bujur=bujur, posisi_bujur=posisi_bujur).order_by('id').first();

        # ambil data dinding
        #dindings = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=gedung.level_lantai, nama_ruang=gedung.nama_ruang).order_by('-sisi')
        infvents = BebanInfiltrasiVentilasi.objects.filter(gedung=gedung)
        pesan = Count(infvents)
        beban_inv = BebanInfiltrasiVentilasi.objects.filter(gedung=gedung).first()
        initial_data = {'infvent':beban_inv}
        inv_form = BebanInfiltrasiVentilasiForm(initial=initial_data)
        if request.method =="POST" and 'add_inv_btn' in request.POST:
            inv_form = BebanInfiltrasiVentilasiForm(request.POST)
            if inv_form.is_valid():
                inv_form.save()
                gedung = inv_form.cleaned_data['gedung']
                lantai = inv_form.cleaned_data['level_lantai']
                ruang = inv_form.cleaned_data['nama_ruang']
                beban_inv = BebanInfiltrasiVentilasi.objects.filter(gedung=gedung, level_lantai=lantai, nama_ruang=ruang).first()
                pesan = 'Beban Inv berhasil diset'
                context = {
                    'form_inv': inv_form,
                    'beban_inv': beban_inv,
                    'pesan': pesan,
                }
                return render(request, 'bebankalor/beban_infiltrasi_d_ventilasi.html', context)
            else:
                pesan = 'form tidak valid'
                context = {
                    'form_inv': inv_form,
                    'pesan': pesan,
                }
                return render(request, 'bebankalor/beban_infiltrasi_d_ventilasi.html', context)
        else:
            pesan = 'Input Beban Infiltrasi Ventilasi'
            context = {
                'form_inv': inv_form,
                'pesan':pesan,
                'beban_inv': beban_inv,

            }
            return render(request,'bebankalor/beban_infiltrasi_d_ventilasi.html',context)


def calculate_beban_kalor_total(request):
    beban_kalor_dinding_persisi = None
    beban_kalor_beton_persisi = None
    q_kaca = None
    status_dinding = None
    status_beton = None
    q_lampu = None
    q_alat = None
    q_penghuni = None
    q_pintus = None
    status = False
    pesan = None
    if request.method == 'POST' and 'search_profil_btn' in request.POST:
        form = SearchProfil(request.POST)
        if form.is_valid():
            gedung = form.cleaned_data['gedung']
            lantai = form.cleaned_data['lantai']  # asumsi satu lantai satu ruangan
            # 1 calculate beban kalor luar (dinding, kaca, dinding partisi, kaca partisi, kolom beton)
            try:
                kaca = BebanLuarKaca.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
                if kaca:
                    q_kaca = audit_lib.beban_kalor_kaca(kaca)
                sisi_dinding = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai).values('sisi').annotate(
                    Count('sisi'))
                # sublist_dindings berisi daftar dinding berdasarkan nama sisi
                if sisi_dinding:
                    sublist_dindings = []
                    for i, val in enumerate(sisi_dinding):
                        nama_sisi = val.get('sisi')
                        sublist = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai, sisi=nama_sisi)
                        sublist_dindings.append(sublist)
                    # status = f'jumlah sublist :{len(sublist_dindings)}'
                    beban_kalor_dinding_persisi = audit_lib.beban_kalor_dinding(sublist_dindings)
                    status_dinding = 'bk dinding dihitung'
                sisi_beton = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai).values('sisi').annotate(
                    Count('sisi'))
                # sublist_dindings berisi daftar dinding berdasarkan nama sisi
                if sisi_beton:
                    sublist_betons = []
                    for i, val in enumerate(sisi_beton):
                        nama_sisi = val.get('sisi')
                        sublist = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai, sisi=nama_sisi)
                        sublist_betons.append(sublist)
                    # status = f'jumlah sublist :{len(sublist_dindings)}'
                    beban_kalor_beton_persisi = audit_lib.beban_kalor_beton(sublist_betons)

                #2 calculate beban kalor dalam (penghuni, alat, pencahayaan)
                penghuni = BebanDalamPenghuni.objects.filter(gedung=gedung, level_lantai=lantai).first()
                gedung = penghuni.gedung
                if penghuni:
                    q_penghuni = audit_lib.beban_kalor_penghuni(penghuni, "default")
                    if q_penghuni == None:
                        status = 'nilai q sp atau q lt tidak tersedia'
                alat = BebanDalamPeralatan.objects.filter(gedung=gedung, level_lantai=lantai)
                if alat and penghuni:
                    lama_dlm_ruang = penghuni.lama_aktivitas
                    total_dlm_ruang = penghuni.total_aktivitas
                    q_alat = audit_lib.beban_kalor_alat(alat, lama_dlm_ruang, total_dlm_ruang)
                cahaya = BebanDalamPencahayaan.objects.filter(gedung=gedung, level_lantai=lantai).first()
                if cahaya and penghuni:
                    total_dlm_ruang = penghuni.total_aktivitas
                    q_lampu = audit_lib.beban_kalor_pencahayaan(cahaya, total_dlm_ruang)

                pintus = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
                if pintus and penghuni:
                    q_pintus = audit_lib.beban_kalor_air_exchange(pintus, penghuni)
                # 3 calculate beban kalor infiltrasi
                inv_vent = BebanInfiltrasiVentilasi.objects.filter(gedung=gedung, level_lantai=lantai).first()
                if inv_vent and pintus and penghuni:
                    q_inv_vent = audit_lib.beban_kalor_infiltrasi_ventilasi(inv_vent, pintus, penghuni)
                status = True
                context = {
                    'status': status,
                    'status_beton': status_beton,
                    'status_dinding': status_dinding,
                    'bk_dinding': beban_kalor_dinding_persisi,
                    'bk_beton': beban_kalor_beton_persisi,
                    'bk_kaca': q_kaca,
                    'q_penghuni': q_penghuni,
                    'q_lampu': q_lampu,
                    'q_alat': q_alat,
                    'q_pintus': q_pintus,
                    'q_inv_vent': q_inv_vent,
                }

                return render(request, 'bebankalor/calc_beban_total.html', context)
            except:
                pesan = 'Komponen profil belum lengkap'
                context ={
                    'pesan':pesan,
                    'status': status,
                    'form': form,
                }
                return render(request, 'bebankalor/calc_beban_total.html', context)

    else:
        form = SearchProfil()
        context = {
            'status': status,
            'form': form,
        }
        return render(request, 'bebankalor/calc_beban_total.html', context)


def calculate_beban_kalor_resume(request):
    beban_kalor_dinding_persisi = None
    beban_kalor_beton_persisi = None
    q_kaca = None
    status_dinding = None
    status_beton = None

    q_lampu = None
    q_alat = None
    q_penghuni = None
    q_pintus = None

    if request.method == 'POST' and 'search_profil_btn' in request.POST:
        form = SearchProfil(request.POST)
        if form.is_valid():
            gedung = form.cleaned_data['gedung']
            lantai = form.cleaned_data['lantai']  # asumsi satu lantai satu ruangan
            # 1 calculate beban kalor luar (dinding, kaca, dinding partisi, kaca partisi, kolom beton)
            kaca = BebanLuarKaca.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
            if kaca:
                q_kaca = audit_lib.beban_kalor_kaca(kaca)
            sisi_dinding = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai).values('sisi').annotate(
                Count('sisi'))
            # sublist_dindings berisi daftar dinding berdasarkan nama sisi
            if sisi_dinding:
                sublist_dindings = []
                for i, val in enumerate(sisi_dinding):
                    nama_sisi = val.get('sisi')
                    sublist = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai, sisi=nama_sisi)
                    sublist_dindings.append(sublist)
                # status = f'jumlah sublist :{len(sublist_dindings)}'
                beban_kalor_dinding_persisi = audit_lib.beban_kalor_dinding(sublist_dindings)
                status_dinding = 'bk dinding dihitung'
            sisi_beton = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai).values('sisi').annotate(
                Count('sisi'))
            # sublist_dindings berisi daftar dinding berdasarkan nama sisi
            if sisi_beton:
                sublist_betons = []
                for i, val in enumerate(sisi_beton):
                    nama_sisi = val.get('sisi')
                    sublist = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai, sisi=nama_sisi)
                    sublist_betons.append(sublist)
                # status = f'jumlah sublist :{len(sublist_dindings)}'
                beban_kalor_beton_persisi = audit_lib.beban_kalor_beton(sublist_betons)

            #2 calculate beban kalor dalam (penghuni, alat, pencahayaan)
            penghuni = BebanDalamPenghuni.objects.filter(gedung=gedung, level_lantai=lantai).first()
            if penghuni == None:
                status = 'Data Penghuni belum diinput'
            else:
                #gedung = penghuni.gedung
                q_penghuni = audit_lib.beban_kalor_penghuni(penghuni, "default")
                if q_penghuni == None:
                    status = 'nilai q sp atau q lt tidak tersedia'
                    context = {
                        'status': status,
                    }
                    return render(request, 'bebankalor/calc_beban_resume.html', context)
                alat = BebanDalamPeralatan.objects.filter(gedung=gedung, level_lantai=lantai)
                if alat and penghuni:
                    lama_dlm_ruang = penghuni.lama_aktivitas
                    total_dlm_ruang = penghuni.total_aktivitas
                    q_alat = audit_lib.beban_kalor_alat(alat, lama_dlm_ruang, total_dlm_ruang)
                cahaya = BebanDalamPencahayaan.objects.filter(gedung=gedung, level_lantai=lantai).first()
                if cahaya and penghuni:
                    total_dlm_ruang = penghuni.total_aktivitas
                    q_lampu = audit_lib.beban_kalor_pencahayaan(cahaya, total_dlm_ruang)
                pintus = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
                if pintus and penghuni:
                    q_pintus = audit_lib.beban_kalor_air_exchange(pintus, penghuni)
                # 3 calculate beban kalor infiltrasi
                inv_vent = BebanInfiltrasiVentilasi.objects.filter(gedung=gedung, level_lantai=lantai).first()
                if inv_vent and pintus and penghuni:
                    q_inv_vent = audit_lib.beban_kalor_infiltrasi_ventilasi(inv_vent, pintus, penghuni)
                    #hitung beban kalor sensibel luar ruangan
                    # q dinding, q kaca, q radiasi kaca, q partisi
                if beban_kalor_dinding_persisi and beban_kalor_beton_persisi and q_kaca and q_penghuni and q_lampu and q_alat and q_pintus and q_inv_vent:
                    slrs,bk_dr, bk_in_ven,ersh,erlh = audit_lib.resume_beban_kalor(beban_kalor_dinding_persisi,beban_kalor_beton_persisi,q_kaca, q_penghuni, q_lampu, q_alat,q_pintus, q_inv_vent)
                    context = {
                        'status_beton': status_beton,
                        'status_dinding': status_dinding,
                        'bk_dinding': beban_kalor_dinding_persisi,
                        'bk_beton': beban_kalor_beton_persisi,
                        'bk_kaca': q_kaca,
                        'q_penghuni': q_penghuni,
                        'q_lampu': q_lampu,
                        'q_alat': q_alat,
                        'q_pintus': q_pintus,
                        'bk_inven': bk_in_ven,
                        'slrs': slrs,
                        'bk_dr': bk_dr,
                        'ersh':ersh,
                        'erlh': erlh,
                    }

                else:
                    context ={
                        'status': 'Data belum lengkap silahkan dilengkapi'
                    }
                return render(request, 'bebankalor/calc_beban_resume.html', context)
                # return render(request, 'bebankalor/calc_beban_total.html', context)
        else:
            context ={
                'status':  'Data profil belum lengkap',
                'form': form,
            }
            return render(request, 'bebankalor/calc_beban_resume.html', context)

    else:
        form = SearchProfil()
        status = 'Pilih Profil'
        context = {
            'status': status,
            'form': form,
        }
        return render(request, 'bebankalor/calc_beban_resume.html', context)


def calc_bk_luar(request):
    #hitung per sisi dinding
    beban_kalor_dinding_persisi = None
    beban_kalor_beton_persisi = None
    waktu_kaca= None
    q_kaca=None
    status_dinding = None
    status_beton = None
    if request.method == 'POST'and 'search_profil_btn'in request.POST:
        form = SearchProfil(request.POST)
        if form.is_valid():
            gedung = form.cleaned_data['gedung']
            lantai = form.cleaned_data['lantai'] #asumsi satu lantai satu ruangan
            kaca = BebanLuarKaca.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
            if kaca:
                q_kaca = audit_lib.beban_kalor_kaca(kaca)
            #pintu = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
            sisi_pintu = BebanLuarPintu.objects.values('sisi').annotate(Count('sisi'))
            # sublist_dindings berisi daftar dinding berdasarkan nama sisi
            """
            if sisi_pintu:
                sublist_pintus = []
                for i, val in enumerate(sisi_pintu):
                    nama_sisi = val.get('sisi')
                    sublist = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai, sisi=nama_sisi)
                    sublist_pintus.append(sublist)
                # status = f'jumlah sublist :{len(sublist_dindings)}'
                beban_kalor_pintu_persisi = audit_lib.beban_kalor_pintu(sublist_pintus)
                status_pintu = 'bk pintu dihitung'
            """
            #beton = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')

            sisi_dinding = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai).values('sisi').annotate(Count('sisi'))
            # sublist_dindings berisi daftar dinding berdasarkan nama sisi
            if sisi_dinding:
                sublist_dindings = []
                for i, val in enumerate(sisi_dinding):
                    nama_sisi = val.get('sisi')
                    sublist = BebanLuarDinding.objects.filter(gedung=gedung, level_lantai=lantai, sisi=nama_sisi)
                    sublist_dindings.append(sublist)
                # status = f'jumlah sublist :{len(sublist_dindings)}'
                beban_kalor_dinding_persisi = audit_lib.beban_kalor_dinding(sublist_dindings)
                status_dinding = 'bk dinding dihitung'
            sisi_beton = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai).values('sisi').annotate(Count('sisi'))
            # sublist_dindings berisi daftar dinding berdasarkan nama sisi
            if sisi_beton:
                sublist_betons = []
                for i, val in enumerate(sisi_beton):
                    nama_sisi = val.get('sisi')
                    sublist = BebanLuarBeton.objects.filter(gedung=gedung, level_lantai=lantai, sisi=nama_sisi)
                    sublist_betons.append(sublist)
                # status = f'jumlah sublist :{len(sublist_dindings)}'
                beban_kalor_beton_persisi = audit_lib.beban_kalor_beton(sublist_betons)
                status_beton = 'bk beton dihitung'
            context = {
                'status_beton': status_beton,
                'status_dinding': status_dinding,
                'bk_dinding': beban_kalor_dinding_persisi,
                'bk_beton': beban_kalor_beton_persisi,
                #'bk_pintu': beban_kalor_pintu_persisi,
                'bk_kaca': q_kaca,

                }


            return render(request, 'bebankalor/calc_beban_luar.html', context)
        else:
            status = 'form tidak valid'
            context = {
                'status': status,
            }
            return render(request, 'bebankalor/calc_beban_luar.html', context)
    else:
        form = SearchProfil()
        status ='Pilih Profil'
        context = {
            'status': status,
            'form':form,
        }
        return render(request, 'bebankalor/calc_beban_luar.html', context)
def calc_bk_dalam(request):
    context = None
    status = None
    q_lampu = None
    q_alat = None
    q_penghuni = None
    q_pintus = None
    gedung = None
    lama_dlm_ruang = 0
    if request.method == 'POST'and 'search_profil_btn'in request.POST:
        form = SearchProfil(request.POST)
        if form.is_valid():
            gedung = form.cleaned_data['gedung']
            lantai = form.cleaned_data['lantai'] #asumsi satu lantai satu ruangan
            #ruang = form.cleaned_data['nama_ruang']
            penghuni = BebanDalamPenghuni.objects.filter(gedung=gedung, level_lantai=lantai).first()
            gedung = penghuni.gedung
            if penghuni:
                q_penghuni = audit_lib.beban_kalor_penghuni(penghuni,"default")
                if q_penghuni == None:
                    status = 'nilai q sp atau q lt tidak tersedia'
            alat = BebanDalamPeralatan.objects.filter(gedung=gedung, level_lantai=lantai)
            if alat and penghuni:
                lama_dlm_ruang = penghuni.lama_aktivitas
                total_dlm_ruang = penghuni.total_aktivitas
                q_alat = audit_lib.beban_kalor_alat(alat, lama_dlm_ruang, total_dlm_ruang)
            cahaya = BebanDalamPencahayaan.objects.filter(gedung=gedung, level_lantai=lantai).first()
            if cahaya and penghuni:
                total_dlm_ruang = penghuni.total_aktivitas
                q_lampu = audit_lib.beban_kalor_pencahayaan(cahaya,total_dlm_ruang)

            pintus = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
            if pintus and penghuni:
                q_pintus = audit_lib.beban_kalor_air_exchange(pintus, penghuni)


            context = {
                'profil': gedung,
                'q_penghuni': q_penghuni,
                'q_lampu': q_lampu,
                'q_alat': q_alat,
                'q_pintus': q_pintus,
                'status': status,
            }
            return render(request, 'bebankalor/calc_beban_dalam.html', context)
    else:
        form = SearchProfil()
        status ='Pilih Profil'
        context = {
            'status': status,
            'form':form,
        }
        return render(request, 'bebankalor/calc_beban_dalam.html', context)

def calc_bk_infvent(request):
    context = None
    pesan = None
    q_inv_vent = None
    form = SearchProfil(None)
    if request.method == 'POST' and 'calc_inv_btn' in request.POST:
        form = SearchProfil(request.POST)
        if form.is_valid():
            gedung = form.cleaned_data['gedung']
            lantai = form.cleaned_data['lantai']  # asumsi satu lantai satu ruangan
            inv_vent = BebanInfiltrasiVentilasi.objects.filter(gedung=gedung, level_lantai=lantai).first()
            pintus = BebanLuarPintu.objects.filter(gedung=gedung, level_lantai=lantai).order_by('-sisi')
            penghuni = BebanDalamPenghuni.objects.filter(gedung=gedung, level_lantai=lantai).first()
            if inv_vent and pintus and penghuni:
                q_inv_vent = audit_lib.beban_kalor_infiltrasi_ventilasi(inv_vent,pintus,penghuni)
                context ={
                    'q_inv_vent': q_inv_vent,
                    'profil':inv_vent.gedung,
                }
                return render(request, 'bebankalor/calc_beban_inv.html', context)
            else:
                pesan ='komponen inviltrasi belum didefinisikan'
                context = {
                    'form': form,
                    'pesan':pesan,
                }
                return render(request, 'bebankalor/calc_beban_inv.html', context)
        else:
            pesan = 'form tidak valid'
            context = {
                'form': form,
                'pesan':pesan,
            }
            return render(request, 'bebankalor/calc_beban_inv.html', context)
    else:
        pesan = 'Masukkan parameter input'
        context = {
            'form': form,
            'pesan': pesan,
        }
        return render(request, 'bebankalor/calc_beban_inv.html', context)








