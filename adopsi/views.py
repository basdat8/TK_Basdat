from django.shortcuts import render

def adopsi_view(request):
    hewan_list = [
        {
            'id': 1,
            'foto': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Minni',
            'jenis': 'Kucing',
            'kondisi': 'Sehat',
            'habitat': 'Hutan dan pemukiman',
            'tanggal_mulai': '15 Januari 2023',
            'tanggal_akhir': '15 Juli 2023',
            'nama_adopter': 'Yayasan Cinta Satwa'
        },
        {
            'id': 2,
            'foto': 'https://images.unsplash.com/photo-1586671267731-da2cf3ceeb80?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Budi',
            'jenis': 'Anjing',
            'kondisi': 'Perlu perhatian',
            'habitat': 'Pemukiman manusia',
            'tanggal_mulai': '1 Februari 2023',
            'tanggal_akhir': '1 Agustus 2023',
            'nama_adopter': 'Andi Saputra'
        },
{
            'id': 3,
            'foto': 'https://images.unsplash.com/photo-1556838803-cc94986cb631?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Ciko',
            'jenis': 'Kelinci',
            'kondisi': 'Sehat, aktif',
            'habitat': 'Padang rumput',
            'tanggal_mulai': '10 Maret 2023',
            'tanggal_akhir': '10 September 2023',
            'nama_adopter': 'Bobon Santoso'
        },
        {
            'id': 4,
            'foto': 'https://images.unsplash.com/photo-1555169062-013468b47731?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Kiki',
            'jenis': 'Burung Beo',
            'kondisi': 'Sehat, bisa bicara',
            'habitat': 'Hutan tropis',
            'tanggal_mulai': '5 April 2023',
            'tanggal_akhir': '5 Oktober 2023',
            'nama_adopter': 'Yayasan Peduli Kiki'
        },
        {
            'id': 5,
            'foto': 'https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Moli',
            'jenis': 'Panda',
            'kondisi': 'Stabil',
            'habitat': 'Sungai dan rawa',
            'tanggal_mulai': '20 Mei 2023',
            'tanggal_akhir': '20 November 2023',
            'nama_adopter': 'Santoso Bobon'
        }
    ]
    return render(request, 'adopsi/halaman_adopsi.html', {'hewan_list': hewan_list})
from django.shortcuts import render

def adopsi_staff_view(request):
    hewan_list = [
        {
            'id': 1,
            'foto': 'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Minni',
            'jenis': 'Kucing',
            'kondisi': 'Sehat',
            'diadopsi': True,
            'nama_adopter': 'John Doe',
            'tanggal_mulai': '15 Januari 2023',
            'tanggal_akhir': '15 Juli 2023',
            'kontribusi': 500000,
            'status_pembayaran': 'lunas'
        },
        {
            'id': 2,
            'foto': 'https://images.unsplash.com/photo-1586671267731-da2cf3ceeb80?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Budi',
            'jenis': 'Anjing',
            'kondisi': 'Perlu perhatian',
            'diadopsi': False,
            'nama_adopter': None,
            'tanggal_mulai': None,
            'tanggal_akhir': None,
            'kontribusi': None,
            'status_pembayaran': None
        },
        {
            'id': 3,
            'foto': 'https://images.unsplash.com/photo-1556838803-cc94986cb631?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Ciko',
            'jenis': 'Kelinci',
            'kondisi': 'Sehat, aktif',
            'diadopsi': True,
            'nama_adopter': 'Jane Smith',
            'tanggal_mulai': '10 Maret 2023',
            'tanggal_akhir': '10 September 2023',
            'kontribusi': 300000,
            'status_pembayaran': 'tertunda'
        },
        {
            'id': 4,
            'foto': 'https://images.unsplash.com/photo-1555169062-013468b47731?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Kiki',
            'jenis': 'Burung Beo',
            'kondisi': 'Sehat, bisa bicara',
            'diadopsi': False,
            'nama_adopter': None,
            'tanggal_mulai': None,
            'tanggal_akhir': None,
            'kontribusi': None,
            'status_pembayaran': None
        },
        {
            'id': 5,
            'foto': 'https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
            'nama': 'Moli',
            'jenis': 'Kura-kura',
            'kondisi': 'Stabil',
            'diadopsi': True,
            'nama_adopter': 'Sinta',
            'tanggal_mulai': '20 Mei 2023',
            'tanggal_akhir': '20 November 2023',
            'kontribusi': 1000000,
            'status_pembayaran': 'lunas'
        }
    ]
    return render(request, 'adopsi/halaman_adopsi_staff.html', {'hewan_list': hewan_list})