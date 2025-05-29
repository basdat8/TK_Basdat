# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.http import Http404
from django.contrib import messages 

# utils

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# HEWAN

def list_hewan(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hewan")
        data = dictfetchall(cursor)
    return render(request, 'list_hewan.html', {'data': data})

def tambah_hewan(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        spesies = request.POST['spesies']
        asal = request.POST['asal_hewan']
        tgl = request.POST.get('tanggal_lahir') or None
        status = request.POST['status_kesehatan']
        habitat = request.POST['nama_habitat']
        foto = request.POST['url_foto']

        with connection.cursor() as cursor:
            # Cek apakah satwa duplikat
            cursor.execute("""
                SELECT 1 FROM hewan 
                WHERE nama = %s AND spesies = %s AND asal_hewan = %s
            """, [nama, spesies, asal])
            if cursor.fetchone():
                messages.error(
                    request,
                    f'Data satwa atas nama “{nama}”, spesies “{spesies}”, dan berasal dari “{asal}” sudah terdaftar.'
                )

                # Ambil ulang daftar habitat untuk dropdown
                cursor.execute("SELECT nama FROM habitat")
                habitats = [row[0] for row in cursor.fetchall()]

                # Kembalikan form dengan data yang sudah diisi
                return render(request, 'form_hewan.html', {
                    'habitats': habitats,
                    'data': {
                        'nama': nama,
                        'spesies': spesies,
                        'asal_hewan': asal,
                        'tanggal_lahir': tgl,
                        'status_kesehatan': status,
                        'nama_habitat': habitat,
                        'url_foto': foto
                    }
                })

            # Insert jika tidak duplikat
            cursor.execute("""
                INSERT INTO hewan (id, nama, spesies, asal_hewan, tanggal_lahir, status_kesehatan, nama_habitat, url_foto)
                VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s, %s)
            """, [nama, spesies, asal, tgl, status, habitat, foto])

        return redirect('list_hewan')

    # GET method
    with connection.cursor() as cursor:
        cursor.execute("SELECT nama FROM habitat")
        habitats = [row[0] for row in cursor.fetchall()]
    return render(request, 'form_hewan.html', {'habitats': habitats})

def edit_hewan(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hewan WHERE id = %s", [id])
        data = dictfetchall(cursor)
        if not data:
            raise Http404()
        hewan = data[0]
    if request.method == 'POST':
        nama = request.POST['nama']
        spesies = request.POST['spesies']
        asal = request.POST['asal_hewan']
        tgl = request.POST.get('tanggal_lahir') or None
        status = request.POST['status_kesehatan']
        habitat = request.POST['nama_habitat']
        foto = request.POST['url_foto']
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE hewan SET nama=%s, spesies=%s, asal_hewan=%s, tanggal_lahir=%s, 
                status_kesehatan=%s, nama_habitat=%s, url_foto=%s WHERE id=%s
            """, [nama, spesies, asal, tgl, status, habitat, foto, id])
        return redirect('list_hewan')
    with connection.cursor() as cursor:
        cursor.execute("SELECT nama FROM habitat")
        habitats = [row[0] for row in cursor.fetchall()]
    return render(request, 'form_hewan.html', {'data': hewan, 'habitats': habitats})

def hapus_hewan(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM hewan WHERE id = %s", [id])
    return redirect('list_hewan')

# HABITAT

def list_habitat(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM habitat")
        data = dictfetchall(cursor)
    return render(request, 'list_habitat.html', {'data': data})

def tambah_habitat(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        luas = request.POST['luas_area']
        kapasitas = request.POST['kapasitas']
        status = request.POST['status']
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO habitat (nama, luas_area, kapasitas, status) VALUES (%s, %s, %s, %s)
            """, [nama, luas, kapasitas, status])
        return redirect('list_habitat')
    return render(request, 'form_habitat.html')

def edit_habitat(request, nama):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM habitat WHERE nama = %s", [nama])
        data = dictfetchall(cursor)
        if not data:
            raise Http404()
        habitat = data[0]
    if request.method == 'POST':
        luas = request.POST['luas_area']
        kapasitas = request.POST['kapasitas']
        status = request.POST['status']
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE habitat SET luas_area=%s, kapasitas=%s, status=%s WHERE nama=%s
            """, [luas, kapasitas, status, nama])
        return redirect('list_habitat')
    return render(request, 'form_habitat.html', {'data': habitat})

def hapus_habitat(request, nama):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM habitat WHERE nama = %s", [nama])
    return redirect('list_habitat')

def detail_habitat(request, nama):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM habitat WHERE nama = %s", [nama])
        data = dictfetchall(cursor)
        if not data:
            raise Http404()
        habitat = data[0]
        cursor.execute("SELECT * FROM hewan WHERE nama_habitat = %s", [nama])
        hewan_list = dictfetchall(cursor)
    return render(request, 'detail_habitat.html', {'habitat': habitat, 'hewan_list': hewan_list})
