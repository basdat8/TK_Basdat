from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.http import require_POST

from kuning.views import dictfetchall


# Create your views here.

def list_catatan_medis(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM catatan_medis CM LEFT JOIN pengguna P ON CM.username_dh = P.username WHERE id_hewan = %s", [id])
        data = dictfetchall(cursor)
        print(data)
    return render(request, 'catatanmedis_list.html', {'data': data, 'id': id})

@require_POST
def add_catatan_medis(request, id, username_dh):
    if request.method == 'POST':
        tanggal = request.POST['tanggal_pemeriksaan']
        status = request.POST['status_kesehatan']
        diagnosis = request.POST['diagnosis']
        pengobatan = request.POST['pengobatan']
        catatatan = request.POST['catatan_tindak_lanjut']
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO catatan_medis (id_hewan, username_dh, tanggal_pemeriksaan, diagnosis, pengobatan, status_kesehatan, catatan_tindak_lanjut)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [id, username_dh, tanggal, diagnosis, pengobatan, status, catatatan])
        return redirect('list_catatan_medis')
    return render(request, 'catatanmedis_form.html', {})

def delete_catatan_medis(request, id, username_dh):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM catatan_medis WHERE id_hewan = %s AND username_dh = %s", [id, username_dh])
    return redirect('list_catatan_medis')

# TODO: ADD DATE
def edit_catatan_medis(request, id, username_dh):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM catatan_medis WHERE id_hewan = %s AND username_dh = %s", [id, username_dh])
        data = dictfetchall(cursor)
        if not data:
            raise Http404()
        catatan_medis = data[0]
        if request.method == 'POST':
            catatatan = request.POST.get('catatan_tindak_lanjut') or None
            diagnosa = request.POST['diagnosa_baru']
            pengobatan = request.POST['pengobatan_baru']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE catatan_medis SET catatan_tindak_lanjut = %s, diagnosis = %s, pengobatan = %s"
                               "WHERE id_hewan = %s AND username_dh = %s", [catatatan, diagnosa, pengobatan, id, username_dh])
            return redirect('list_catatan_medis')

    return render(request, 'catatanmedis_edit.html', {})


