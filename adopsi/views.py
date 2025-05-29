from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def adopsi_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM hewan h
            JOIN adopsi a ON h.id = a.id_hewan
            JOIN adopter ad ON a.id_adopter = ad.id_adopter
            WHERE a.id_adopter = %s
        """, [request.user.id if request.user.is_authenticated else None])
        hewan_list = dictfetchall(cursor)
    return render(request, 'adopsi/halaman_adopsi.html', {'hewan_list': hewan_list})

# with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT *
#             FROM hewan h
#             LEFT JOIN adopsi a ON h.id = a.id_hewan
#             WHERE a.id_adopter = %s
#         """, [request.user.id if request.user.is_authenticated else None])
#         hewan_list = dictfetchall(cursor)
#     return render(request, 'adopsi/halaman_adopsi.html', {'hewan_list': hewan_list})

def adopsi_staff_view(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM hewan h
            LEFT JOIN adopsi a ON h.id = a.id_hewan
            LEFT JOIN adopter ad ON a.id_adopter = ad.id_adopter
        """)
        hewan_list = dictfetchall(cursor)
        print(hewan_list)
    return render(request, 'adopsi/halaman_adopsi_staff.html', {'hewan_list': hewan_list})

def update_adopsi(request, hewan_id):
    if request.method == 'POST':
        status = request.POST.get('status')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE adopsi
                SET status_pembayaran = %s
                WHERE id_hewan = %s
            """, [status, hewan_id])
        
        return HttpResponse(status=200)

def delete_adopsi(request, hewan_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM adopsi
                WHERE id_hewan = %s
            """, [hewan_id])
        
        return HttpResponse(status=200)
    
    return HttpResponse(status=405)  # Method Not Allowed for non-POST requests

def verifikasi_adopter(request, username):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM adopter
            WHERE username_adopter = %s
        """, [username])
        adopter = dictfetchall(cursor)
        if not adopter:
            return HttpResponse("Adopter not found", status=404)
        else:
            return HttpResponse(f"Adopter found: {adopter[0]}", status=200)

def get_all_adopter(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM adopter
        """)
        adopter_list = dictfetchall(cursor)
        return JsonResponse(adopter_list, safe=False)
