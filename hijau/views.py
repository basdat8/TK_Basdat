from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


from kuning.views import dictfetchall


# Create your views here.

def list_catatan_medis(request, id_hewan):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM catatan_medis CM LEFT JOIN pengguna P ON CM.username_dh = P.username WHERE id_hewan = %s", [id_hewan])
        data = dictfetchall(cursor)
        print(data)
    return render(request, 'catatanmedis_list.html', {'data': data, 'id_hewan': id_hewan})

@login_required
@require_POST
def add_catatan_medis(request, id_hewan):
    if request.method == 'POST':
        try:
            tanggal = request.POST['tanggal_pemeriksaan']
            status = request.POST['status_kesehatan']
            diagnosis = request.POST['diagnosis']
            pengobatan = request.POST['pengobatan']
            catatatan = request.POST['catatan_tindak_lanjut']
            username_dh = request.user.username

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO catatan_medis (id_hewan, username_dh, tanggal_pemeriksaan, diagnosis, pengobatan, status_kesehatan, catatan_tindak_lanjut)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [id_hewan, username_dh, tanggal, diagnosis, pengobatan, status, catatatan])
            return JsonResponse({'status': 'success', 'message': 'Catatan medis berhasil ditambahkan!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return redirect(request.META.get('HTTP_REFERER', '/'))

# TODO: ADD DATE
@login_required
def delete_catatan_medis(request, id_hewan):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM catatan_medis WHERE id_hewan = %s", [id_hewan])
    return redirect('list_catatan_medis')

@login_required
@require_POST
def edit_catatan_medis(request, id_hewan):
    username_dh = request.user.username
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM catatan_medis WHERE id_hewan = %s AND username_dh = %s", [id_hewan, username_dh])
        data = dictfetchall(cursor)
        if not data:
            raise Http404()
        catatan_medis = data[0]
        try:
            if request.method == 'POST':
                catatatan = request.POST.get('catatan_tindak_lanjut') or None
                diagnosa = request.POST['diagnosa_baru']
                pengobatan = request.POST['pengobatan_baru']
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE catatan_medis SET catatan_tindak_lanjut = %s, diagnosis = %s, pengobatan = %s"
                                   "WHERE id_hewan = %s AND username_dh = %s", [catatatan, diagnosa, pengobatan, id_hewan, username_dh])
                return JsonResponse({'status': 'success', 'message': 'Catatan medis berhasil ditambahkan!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return redirect(request.META.get('HTTP_REFERER', '/'))


def list_jadwal_pemeriksaan(request, id_hewan):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jadwal_pemeriksaan_kesehatan WHERE id_hewan = %s", [id_hewan])
        data = dictfetchall(cursor)
    return render(request, 'jadwalpemeriksaan_list.html', {'data': data, 'id_hewan': id_hewan})

@login_required
@require_POST
def add_jadwal_pemeriksaan(request, id_hewan):
    if request.method == 'POST':
        try:
            tanggal = request.POST['tanggal_pemeriksaan']
            frequency = request.POST['freqInput']

            with connection.cursor() as cursor:
                cursor.execute("""
                               INSERT INTO jadwal_pemeriksaan_kesehatan (id_hewan, tgl_pemeriksaan_selanjutnya, freq_pemeriksaan_rutin)
                               VALUES (%s, %s, %s)
                               """, [id_hewan, tanggal, frequency])
                return JsonResponse({'status': 'success', 'message': 'Jadwal pemeriksaan berhasil ditambahkan!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delete_jadwal_pemeriksaan(request, id_hewan):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM jadwal_pemeriksaan_kesehatan WHERE id_hewan = %s", [id_hewan])
    return redirect('list_jadwal_pemeriksaan')

@login_required
@require_POST
def edit_jadwal_pemeriksaan(request, id_hewan):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM jadwal_pemeriksaan_kesehatan WHERE id_hewan = %s ", [id_hewan])
        data = dictfetchall(cursor)
        if not data:
            raise Http404()
        jadwal_pemeriksaan = data[0]
        try:
            if request.method == 'POST':
                new_tanggal = request.POST['tanggal_pemeriksaan']
                frequency = request.POST['freqInput']
                tanggal = request.POST['currentDate']
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE jadwal_pemeriksaan_kesehatan SET tgl_pemeriksaan_selanjutnya = %s, freq_pemeriksaan_rutin = %s WHERE id_hewan = %s AND tgl_pemeriksaan_selanjutnya = %s", [new_tanggal, frequency, id_hewan, tanggal])
                return JsonResponse({'status': 'success', 'message': 'Jadwal pemeriksaan berhasil ditambahkan!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return redirect(request.META.get('HTTP_REFERER', '/'))


def list_pemberian_pakan(request, id_hewan):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM pemeriksaan_hewan_kesehatan WHERE id_hewan = %s", [id_hewan])
        data = dictfetchall(cursor)
    return render(request, "")