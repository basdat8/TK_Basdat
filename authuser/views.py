# Updated views.py with real database queries

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import logout,login,authenticate
from datetime import date, timedelta
import logging
from django.http import JsonResponse
import json

logger = logging.getLogger(__name__)

@csrf_protect
def show_login(request):
    """
    Login view for Sizopi system
    """
    context = {}
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Email dan password harus diisi')
            return render(request, 'login.html', context)
        
        try:
            # Use raw SQL to check credentials in pengguna table
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT username, email, password, nama_depan, nama_tengah, nama_belakang, no_telepon 
                    FROM pengguna 
                    WHERE email = %s
                    """,
                    [email]
                )
                user_data = cursor.fetchone()
            
            if user_data and user_data[2] == password:  # password is at index 2
                username = user_data[0]
                
                # Create basic session data
                request.session['username'] = username
                request.session['email'] = email
                request.session['nama_lengkap'] = f"{user_data[3]} {user_data[4] or ''} {user_data[5]}".strip()
                request.session['no_telepon'] = user_data[6]
                
                # Determine user role and redirect accordingly
                user_role = determine_user_role(username)
                
                if user_role:
                    request.session['user_role'] = user_role['role']
                    request.session['user_id'] = user_role.get('id', username)
                    
                    # Redirect based on role
                    redirect_url = get_redirect_url(user_role['role'])
                    logger.info(f"User {email} logged in successfully as {user_role['role']}")
                    return redirect(redirect_url)
                else:
                    messages.error(request, 'Role pengguna tidak ditemukan. Hubungi administrator.')
                    logger.warning(f"User {email} has no assigned role")
                    
            else:
                # Invalid credentials
                messages.error(request, 'Email atau password salah')
                logger.warning(f"Failed login attempt for email: {email}")
                
        except Exception as e:
            messages.error(request, 'Terjadi kesalahan sistem. Silakan coba lagi.')
            logger.error(f"Login error for {email}: {str(e)}")
    
    return render(request, 'login.html', context)


def determine_user_role(username):
    """
    Determine user role by checking role-specific tables
    """
    try:
        with connection.cursor() as cursor:
            # Check if user is a pengunjung (visitor)
            cursor.execute(
                "SELECT username_P FROM pengunjung WHERE username_P = %s",
                [username]
            )
            if cursor.fetchone():
                return {'role': 'pengunjung', 'id': username}
            
            # Check if user is a dokter_hewan (veterinarian)  
            cursor.execute(
                "SELECT username_DH, no_STR FROM dokter_hewan WHERE username_DH = %s",
                [username]
            )
            dokter_data = cursor.fetchone()
            if dokter_data:
                return {'role': 'dokter_hewan', 'id': username, 'no_str': dokter_data[1]}
            
            # Check if user is a penjaga_hewan (animal caretaker)
            cursor.execute(
                "SELECT username_jh, id_staf FROM penjaga_hewan WHERE username_jh = %s",
                [username]
            )
            penjaga_data = cursor.fetchone()
            if penjaga_data:
                return {'role': 'penjaga_hewan', 'id': username, 'id_staf': str(penjaga_data[1])}
            
            # Check if user is a pelatih_hewan (animal trainer)
            cursor.execute(
                "SELECT username_lh, id_staf FROM pelatih_hewan WHERE username_lh = %s",
                [username]
            )
            pelatih_data = cursor.fetchone()
            if pelatih_data:
                return {'role': 'pelatih_hewan', 'id': username, 'id_staf': str(pelatih_data[1])}
            
            # Check if user is a staf_admin (administrative staff)
            cursor.execute(
                "SELECT username_sa, id_staf FROM staf_admin WHERE username_sa = %s",
                [username]
            )
            admin_data = cursor.fetchone()
            if admin_data:
                return {'role': 'staf_admin', 'id': username, 'id_staf': str(admin_data[1])}
                
    except Exception as e:
        logger.error(f"Error determining user role for {username}: {str(e)}")
        
    return None


def get_redirect_url(role):
    """
    Get appropriate redirect URL based on user role
    """
    role_redirects = {
        'pengunjung': 'wajib:dashboard_pengunjung',
        'dokter_hewan': 'wajib:dashboard_dokter_hewan', 
        'penjaga_hewan': 'wajib:dashboard_penjaga_hewan',
        'pelatih_hewan': 'wajib:dashboard_pelatih_hewan',
        'staf_admin': 'wajib:dashboard_staf_admin'
    }
    
    return role_redirects.get(role, 'wajib:home')


def logout_view(request):
    """
    Logout view to clear session and redirect to login
    """
    request.session.flush()  # Clear all session data
    messages.success(request, 'Anda telah berhasil logout')
    return redirect('wajib:login')


def get_user_dashboard_data(request):
    """
    Helper function to get user-specific dashboard data
    """
    if not request.session.get('username'):
        return None
        
    username = request.session.get('username')
    role = request.session.get('user_role')
    
    try:
        with connection.cursor() as cursor:
            # Get basic user info
            cursor.execute(
                """
                SELECT username, email, nama_depan, nama_tengah, nama_belakang, no_telepon
                FROM pengguna 
                WHERE username = %s
                """,
                [username]
            )
            user_data = cursor.fetchone()
            
            if not user_data:
                return None
                
            dashboard_data = {
                'username': user_data[0],
                'email': user_data[1], 
                'nama_lengkap': f"{user_data[2]} {user_data[3] or ''} {user_data[4]}".strip(),
                'no_telepon': user_data[5],
                'role': role
            }
            
            # Add role-specific data
            if role == 'pengunjung':
                cursor.execute(
                    "SELECT alamat, tgl_lahir FROM pengunjung WHERE username_P = %s",
                    [username]
                )
                pengunjung_data = cursor.fetchone()
                if pengunjung_data:
                    dashboard_data.update({
                        'alamat': pengunjung_data[0],
                        'tgl_lahir': pengunjung_data[1]
                    })
                    
            elif role == 'dokter_hewan':
                cursor.execute(
                    "SELECT no_STR FROM dokter_hewan WHERE username_DH = %s",
                    [username]
                )
                dokter_data = cursor.fetchone()
                if dokter_data:
                    dashboard_data['no_str'] = dokter_data[0]
                    
                # Get specializations
                cursor.execute(
                    "SELECT nama_spesialisasi FROM spesialisasi WHERE username_SH = %s",
                    [username]
                )
                spesialisasi = [row[0] for row in cursor.fetchall()]
                dashboard_data['spesialisasi'] = spesialisasi
                
            elif role in ['penjaga_hewan', 'pelatih_hewan', 'staf_admin']:
                table_map = {
                    'penjaga_hewan': ('penjaga_hewan', 'username_jh'),
                    'pelatih_hewan': ('pelatih_hewan', 'username_lh'), 
                    'staf_admin': ('staf_admin', 'username_sa')
                }
                table_name, username_field = table_map[role]
                
                cursor.execute(
                    f"SELECT id_staf FROM {table_name} WHERE {username_field} = %s",
                    [username]
                )
                staf_data = cursor.fetchone()
                if staf_data:
                    dashboard_data['id_staf'] = str(staf_data[0])
            
            return dashboard_data
            
    except Exception as e:
        logger.error(f"Error getting dashboard data for {username}: {str(e)}")
        return None


def get_pengunjung_data(username):
    """
    Get additional data for pengunjung from adoption records
    """
    riwayat_kunjungan = []
    tiket_data = []
    
    try:
        with connection.cursor() as cursor:
            # Get adoption history as visit history
            cursor.execute("""
                SELECT h.nama, h.spesies, a.tgl_mulai_adopsi, a.kontribusi_finansial, a.status_pembayaran
                FROM adopsi a
                JOIN hewan h ON a.id_hewan = h.id  
                JOIN adopter ad ON a.id_adopter = ad.id_adopter
                WHERE ad.username_adopter = %s
                ORDER BY a.tgl_mulai_adopsi DESC
                LIMIT 10
            """, [username])
            
            adoption_data = cursor.fetchall()
            
            for adoption in adoption_data:
                riwayat_kunjungan.append({
                    'lokasi': f'Adopsi {adoption[0]} ({adoption[1]})',
                    'tanggal': adoption[2],
                    'alamat_lokasi': 'Sizopi Zoo',
                    'jenis': 'Adopsi Hewan'
                })
                
                tiket_data.append({
                    'tanggal': adoption[2],
                    'lokasi': f'Adopsi {adoption[0]}',
                    'jenis_tiket': 'Program Adopsi',
                    'status': 'Lunas' if adoption[4] == 'LUNAS' else 'Pending'
                })
            
            # Get facilities that could be "visited"
            cursor.execute("""
                SELECT f.nama, a.lokasi, f.jadwal
                FROM fasilitas f
                LEFT JOIN atraksi a ON f.nama = a.nama_atraksi
                ORDER BY f.jadwal DESC
                LIMIT 5
            """)
            
            facility_data = cursor.fetchall()
            
            for facility in facility_data:
                if len(riwayat_kunjungan) < 10:  # Don't exceed reasonable amount
                    riwayat_kunjungan.append({
                        'lokasi': facility[0],
                        'tanggal': facility[2].date() if facility[2] else date.today(),
                        'alamat_lokasi': facility[1] if facility[1] else 'Sizopi Zoo',
                        'jenis': 'Kunjungan Fasilitas'
                    })
                    
    except Exception as e:
        logger.error(f"Error getting pengunjung data for {username}: {str(e)}")
    
    return {'riwayat_kunjungan': riwayat_kunjungan, 'tiket_data': tiket_data}


def get_dokter_hewan_data(username):
    """
    Get medical statistics for dokter hewan
    """
    stats = {
        'bulan_ini': 0,
        'bulan_lalu': 0,
        'total_tahun': 0,
        'by_species': {}
    }
    
    try:
        with connection.cursor() as cursor:
            today = date.today()
            current_month = today.replace(day=1)
            last_month = (current_month - timedelta(days=1)).replace(day=1)
            year_start = today.replace(month=1, day=1)
            
            # Count animals treated this month
            cursor.execute("""
                SELECT COUNT(DISTINCT id_hewan)
                FROM catatan_medis 
                WHERE username_dh = %s 
                AND tanggal_pemeriksaan >= %s
                AND tanggal_pemeriksaan < %s
            """, [username, current_month, today])
            
            result = cursor.fetchone()
            stats['bulan_ini'] = result[0] if result else 0
            
            # Count animals treated last month
            cursor.execute("""
                SELECT COUNT(DISTINCT id_hewan)
                FROM catatan_medis 
                WHERE username_dh = %s 
                AND tanggal_pemeriksaan >= %s
                AND tanggal_pemeriksaan < %s
            """, [username, last_month, current_month])
            
            result = cursor.fetchone()
            stats['bulan_lalu'] = result[0] if result else 0
            
            # Count animals treated this year
            cursor.execute("""
                SELECT COUNT(DISTINCT id_hewan)
                FROM catatan_medis 
                WHERE username_dh = %s 
                AND tanggal_pemeriksaan >= %s
            """, [username, year_start])
            
            result = cursor.fetchone()
            stats['total_tahun'] = result[0] if result else 0
            
            # Get animals by species
            cursor.execute("""
                SELECT h.spesies, COUNT(DISTINCT cm.id_hewan) as jumlah
                FROM catatan_medis cm
                JOIN hewan h ON cm.id_hewan = h.id
                WHERE cm.username_dh = %s
                AND cm.tanggal_pemeriksaan >= %s
                GROUP BY h.spesies
                ORDER BY jumlah DESC
            """, [username, year_start])
            
            species_data = cursor.fetchall()
            for species, count in species_data:
                stats['by_species'][species] = count
                
    except Exception as e:
        logger.error(f"Error getting dokter hewan data for {username}: {str(e)}")
    
    return stats


def get_penjaga_hewan_data(username):
    """
    Get feeding data for penjaga hewan
    """
    feeding_data = []
    stats = {'total_hari_ini': 0, 'sedang_berlangsung': 0, 'belum_diberi_pakan': 0}
    
    try:
        with connection.cursor() as cursor:
            today = date.today()
            
            # Get feeding records for today
            cursor.execute("""
                SELECT p.jadwal, h.spesies, COUNT(*) as jumlah, p.status, p.jenis
                FROM pakan p
                JOIN hewan h ON p.id_hewan = h.id
                WHERE DATE(p.jadwal) = %s
                GROUP BY p.jadwal, h.spesies, p.status, p.jenis
                ORDER BY p.jadwal
            """, [today])
            
            feeding_records = cursor.fetchall()
            
            total_fed = 0
            ongoing = 0
            
            for record in feeding_records:
                feeding_data.append({
                    'waktu': record[0].strftime('%H:%M'),
                    'jenis_hewan': record[1],
                    'jumlah': record[2],
                    'status': 'Selesai' if record[3] == 'Diberikan' else 'Berlangsung',
                    'jenis_pakan': record[4]
                })
                
                if record[3] == 'Diberikan':
                    total_fed += record[2]
                else:
                    ongoing += record[2]
            
            # Get total animals that need feeding
            cursor.execute("SELECT COUNT(*) FROM hewan")
            total_animals = cursor.fetchone()[0]
            
            stats['total_hari_ini'] = total_fed
            stats['sedang_berlangsung'] = ongoing
            stats['belum_diberi_pakan'] = max(0, total_animals - total_fed - ongoing)
            
    except Exception as e:
        logger.error(f"Error getting penjaga hewan data for {username}: {str(e)}")
    
    return {'feeding_data': feeding_data, 'stats': stats}


def get_pelatih_hewan_data(username):
    """
    Get show schedule and animal training data for pelatih hewan
    """
    jadwal_pertunjukan = []
    daftar_hewan = []
    status_latihan = []
    
    try:
        with connection.cursor() as cursor:
            today = date.today()
            
            # Get today's show schedule
            cursor.execute("""
                SELECT jp.tgl_penugasan, a.nama_atraksi, a.lokasi
                FROM jadwal_penugasan jp
                JOIN atraksi a ON jp.nama_atraksi = a.nama_atraksi
                WHERE jp.username_lh = %s
                AND DATE(jp.tgl_penugasan) = %s
                ORDER BY jp.tgl_penugasan
            """, [username, today])
            
            shows = cursor.fetchall()
            
            for show in shows:
                jadwal_pertunjukan.append({
                    'waktu': show[0].strftime('%H:%M'),
                    'nama_atraksi': show[1],
                    'lokasi': show[2],
                    'status': 'Terjadwal'
                })
            
            # Get animals participating in facilities
            cursor.execute("""
                SELECT h.nama, h.spesies, h.tanggal_lahir, h.status_kesehatan, b.nama_fasilitas
                FROM hewan h
                JOIN berpartisipasi b ON h.id = b.id_hewan
                JOIN fasilitas f ON b.nama_fasilitas = f.nama
                JOIN atraksi a ON f.nama = a.nama_atraksi
                JOIN jadwal_penugasan jp ON a.nama_atraksi = jp.nama_atraksi
                WHERE jp.username_lh = %s
                ORDER BY h.nama
            """, [username])
            
            animals = cursor.fetchall()
            
            for animal in animals:
                age = (date.today() - animal[2]).days // 365 if animal[2] else 0
                daftar_hewan.append({
                    'nama': animal[0],
                    'spesies': animal[1],
                    'umur': f'{age} tahun',
                    'status': 'Siap Show' if animal[3] == 'Sehat' else 'Perlu Perawatan'
                })
                
                status_latihan.append({
                    'nama_hewan': animal[0],
                    'aktivitas': f'Latihan {animal[4]}',
                    'tanggal': date.today(),
                    'status': 'Berhasil' if animal[3] == 'Sehat' else 'Perlu Latihan'
                })
            
    except Exception as e:
        logger.error(f"Error getting pelatih hewan data for {username}: {str(e)}")
    
    return {
        'jadwal_pertunjukan': jadwal_pertunjukan,
        'daftar_hewan': daftar_hewan,
        'status_latihan': status_latihan
    }


def get_staf_admin_data():
    """
    Get administrative statistics
    """
    tiket_stats = {
        'reguler': {'count': 0, 'revenue': 0},
        'vip': {'count': 0, 'revenue': 0},
        'grup': {'count': 0, 'revenue': 0},
        'total': {'count': 0, 'revenue': 0}
    }
    
    pengunjung_stats = {
        'dewasa': 0,
        'anak': 0,
        'total': 0
    }
    
    try:
        with connection.cursor() as cursor:
            # Get adoption statistics as ticket sales proxy
            cursor.execute("""
                SELECT status_pembayaran, COUNT(*) as count, SUM(kontribusi_finansial) as revenue
                FROM adopsi
                WHERE DATE(tgl_mulai_adopsi) = %s
                GROUP BY status_pembayaran
            """, [date.today()])
            
            adoption_stats = cursor.fetchall()
            
            # Map adoption data to ticket categories
            for status, count, revenue in adoption_stats:
                if status == 'LUNAS':
                    tiket_stats['reguler']['count'] += count
                    tiket_stats['reguler']['revenue'] += revenue or 0
                else:
                    tiket_stats['vip']['count'] += count
                    tiket_stats['vip']['revenue'] += revenue or 0
            
            # Calculate totals
            tiket_stats['total']['count'] = (tiket_stats['reguler']['count'] + 
                                           tiket_stats['vip']['count'])
            tiket_stats['total']['revenue'] = (tiket_stats['reguler']['revenue'] + 
                                             tiket_stats['vip']['revenue'])
            
            # Get visitor statistics from pengunjung count
            cursor.execute("SELECT COUNT(*) FROM pengunjung")
            total_registered = cursor.fetchone()[0]
            
            pengunjung_stats['dewasa'] = int(total_registered * 0.7)  # Estimate
            pengunjung_stats['anak'] = int(total_registered * 0.3)   # Estimate  
            pengunjung_stats['total'] = total_registered
            
    except Exception as e:
        logger.error(f"Error getting staf admin data: {str(e)}")
    
    return {'tiket_stats': tiket_stats, 'pengunjung_stats': pengunjung_stats}


# Updated Dashboard views for each role
def dashboard_pengunjung(request):
    """Dashboard for Pengunjung (Visitor)"""
    dashboard_data = get_user_dashboard_data(request)
    if not dashboard_data:
        return redirect('wajib:login')
    
    additional_data = get_pengunjung_data(request.session.get('username'))
    
    context = {
        'user_data': dashboard_data,
        'riwayat_kunjungan': additional_data['riwayat_kunjungan'],
        'tiket_data': additional_data['tiket_data'],
    }
    return render(request, 'dashboard/pengunjung.html', context)


def dashboard_dokter_hewan(request):
    """Dashboard for Dokter Hewan (Veterinarian)"""
    dashboard_data = get_user_dashboard_data(request)
    if not dashboard_data:
        return redirect('wajib:login')
    
    medical_stats = get_dokter_hewan_data(request.session.get('username'))
    
    context = {
        'user_data': dashboard_data,
        'medical_stats': medical_stats
    }
    return render(request, 'dashboard/dokter_hewan.html', context)


def dashboard_penjaga_hewan(request):
    """Dashboard for Penjaga Hewan (Animal Caretaker)"""
    dashboard_data = get_user_dashboard_data(request)
    if not dashboard_data:
        return redirect('wajib:login')
    
    feeding_info = get_penjaga_hewan_data(request.session.get('username'))
    
    context = {
        'user_data': dashboard_data,
        'feeding_data': feeding_info['feeding_data'],
        'feeding_stats': feeding_info['stats']
    }
    return render(request, 'dashboard/penjaga_hewan.html', context)


def dashboard_pelatih_hewan(request):
    """Dashboard for Pelatih Hewan (Animal Trainer)"""
    dashboard_data = get_user_dashboard_data(request)
    if not dashboard_data:
        return redirect('wajib:login')
    
    training_info = get_pelatih_hewan_data(request.session.get('username'))
    
    context = {
        'user_data': dashboard_data,
        'jadwal_pertunjukan': training_info['jadwal_pertunjukan'],
        'daftar_hewan': training_info['daftar_hewan'],
        'status_latihan': training_info['status_latihan']
    }
    return render(request, 'dashboard/pelatih_hewan.html', context)


def dashboard_staf_admin(request):
    """Dashboard for Staf Admin (Administrative Staff)"""
    dashboard_data = get_user_dashboard_data(request)
    if not dashboard_data:
        return redirect('wajib:login')
    
    admin_stats = get_staf_admin_data()
    
    context = {
        'user_data': dashboard_data,
        'tiket_stats': admin_stats['tiket_stats'],
        'pengunjung_stats': admin_stats['pengunjung_stats']
    }
    return render(request, 'dashboard/staf_admin.html', context)


# def login_view(request):
#     if request.method == 'POST':
#         email : str = request.POST.get('email')
#         password : str = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Email atau password salah.')
#     return render(request, 'login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')


@csrf_protect
def pilih_role_view(request):
    return render(request, 'pilih_role.html')

@csrf_protect
def form_pengguna_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        nama_depan = request.POST.get('nama_depan')
        nama_tengah = request.POST.get('nama_tengah') or None
        nama_belakang = request.POST.get('nama_belakang')
        email = request.POST.get('email')
        no_telepon = request.POST.get('no_telepon')
        alamat = request.POST.get('alamat')
        tgl_lahir = request.POST.get('tgl_lahir')

        if password != confirm_password:
            messages.error(request, "❌ Password dan konfirmasi tidak cocok.")
            return redirect('wajib:form_pengguna')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pengguna (username, password, nama_depan, nama_tengah, nama_belakang, email, no_telepon)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [username, password, nama_depan, nama_tengah, nama_belakang, email, no_telepon])

                cursor.execute("""
                    INSERT INTO pengunjung (username_p, alamat, tgl_lahir)
                    VALUES (%s, %s, %s)
                """, [username, alamat, tgl_lahir])

            messages.success(request, "✅ Akun pengunjung berhasil dibuat.")
            return redirect('wajib:login')

        except Exception as e:
            if "Username" in str(e):
                messages.error(request, f"❌ ERROR: Username “{username}” sudah digunakan, silakan pilih username lain.")
            else:
                messages.error(request, f"❌ Gagal mendaftar: {str(e)}")
            return redirect('wajib:form_pengguna')

    return render(request, 'form_pengguna.html')


@csrf_protect
def form_dokterhewan_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        nama_depan = request.POST.get('nama_depan')
        nama_tengah = request.POST.get('nama_tengah') or None
        nama_belakang = request.POST.get('nama_belakang')
        email = request.POST.get('email')
        no_telepon = request.POST.get('no_telepon')
        no_str = request.POST.get('no_str')
        spesialisasi = request.POST.getlist('spesialisasi')

        if password != confirm_password:
            messages.error(request, "❌ Password dan konfirmasi tidak cocok.")
            return redirect('wajib:form_dokterhewan')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pengguna (username, password, nama_depan, nama_tengah, nama_belakang, email, no_telepon)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [username, password, nama_depan, nama_tengah, nama_belakang, email, no_telepon])

                cursor.execute("""
                    INSERT INTO dokter_hewan (username_dh, no_str)
                    VALUES (%s, %s)
                """, [username, no_str])

                for item in spesialisasi:
                    cursor.execute("""
                        INSERT INTO spesialisasi (username_sh, nama_spesialisasi)
                        VALUES (%s, %s)
                    """, [username, item])

            messages.success(request, "✅ Akun dokter hewan berhasil dibuat.")
            return redirect('wajib:login')

        except Exception as e:
            if "Username" in str(e):
                messages.error(request, f"❌ ERROR: Username “{username}” sudah digunakan, silakan pilih username lain.")
            else:
                messages.error(request, f"❌ Gagal mendaftar: {str(e)}")
            return redirect('wajib:form_dokterhewan')

    return render(request, 'form_dokterhewan.html')


@csrf_protect
def form_staff_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        nama_depan = request.POST.get('nama_depan')
        nama_tengah = request.POST.get('nama_tengah') or None
        nama_belakang = request.POST.get('nama_belakang')
        email = request.POST.get('email')
        no_telepon = request.POST.get('no_telepon')
        peran = request.POST.get('peran')  # penjaga_hewan / staf_admin / pelatih_hewan

        if password != confirm_password:
            messages.error(request, "❌ Password dan konfirmasi tidak cocok.")
            return redirect('wajib:form_staff')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pengguna (username, password, nama_depan, nama_tengah, nama_belakang, email, no_telepon)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [username, password, nama_depan, nama_tengah, nama_belakang, email, no_telepon])

                if peran == 'penjaga_hewan':
                    cursor.execute("""
                        INSERT INTO penjaga_hewan (username_jh, id_staf)
                        VALUES (%s, gen_random_uuid())
                    """, [username])
                elif peran == 'staf_admin':
                    cursor.execute("""
                        INSERT INTO staf_admin (username_sa, id_staf)
                        VALUES (%s, gen_random_uuid())
                    """, [username])
                elif peran == 'pelatih_hewan':
                    cursor.execute("""
                        INSERT INTO pelatih_hewan (username_lh, id_staf)
                        VALUES (%s, gen_random_uuid())
                    """, [username])
                else:
                    messages.error(request, "❌ Peran tidak dikenali.")
                    return redirect('wajib:form_staff')

            messages.success(request, "✅ Akun staff berhasil dibuat.")
            return redirect('wajib:login')

        except Exception as e:
            if "Username" in str(e):
                messages.error(request, f"❌ ERROR: Username “{username}” sudah digunakan, silakan pilih username lain.")
            else:
                messages.error(request, f"❌ Gagal mendaftar: {str(e)}")
            return redirect('wajib:form_staff')

    return render(request, 'form_staff.html')
