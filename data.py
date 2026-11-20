# data.py
# Isi: data penyakit, data gejala, dan basis kasus (hasil pembulatan: ada angka = 1, kosong = 0)
# Sumber data: Tabel 1, 2, dan 3 jurnal Pratama dkk. (2022), Jurnal Smart Teknologi 4(1), 77-82.

# Tabel 1: Data penyakit
PENYAKIT = {
    "P1": "Busuk Pangkal Batang",
    "P2": "Busuk Bakteri",
    "P3": "Fusarium",
    "P4": "Hama Kutu Daun",
    "P5": "Antraknosa",
    "P6": "Hama Kutu Kebul",
    "P7": "Hama Tungau",
}

# Tabel 2: Data gejala
GEJALA = {
    "G1": "Busuk pada pangkal batang berbatas dengan tanah",
    "G2": "Busuk kering dibagian tepi batang",
    "G3": "Busuk basah batang muncul bercak kuning",
    "G4": "Busuk basah bagian ujung batang",
    "G5": "Terdapat bulu putih bagian pangkal batang",
    "G6": "Tanaman layu",
    "G7": "Tanaman berwarna kuning kusam",
    "G8": "Terdapat lendir putih kekuningan",
    "G9": "Tanaman tampak basah",
    "G10": "Cabang tanaman mengkerut",
    "G11": "Cabang tanaman busuk berwarna coklat",
    "G12": "Cabang tanaman layu",
    "G13": "Buah mengecil",
    "G14": "Pucuk daun mengkerut",
    "G15": "Pucuk daun kering",
    "G16": "Pembusukan bunga",
    "G17": "Buah membusuk",
    "G18": "Terdapat bercak jingga pada buah",
    "G19": "Kusam pada sulur",
    "G20": "Luka konsentris berwarna merah coklat pada batang",
    "G21": "Terdapat bercak nekrotik",
    "G22": "Muncul belang-belang berwarna kuning",
}

# Tabel 3 (sudah dibulatkan): gejala apa saja yang bernilai 1 untuk tiap penyakit.
# Gejala yang tidak ditulis di sini otomatis bernilai 0.
BASIS_KASUS = {
    "P1": ["G1", "G2", "G3", "G4", "G5"],
    "P2": ["G1", "G6", "G7", "G8", "G9"],
    "P3": ["G6", "G7", "G8", "G10", "G11", "G12", "G20"],
    "P4": ["G6", "G13", "G14"],
    "P5": ["G3", "G15", "G16", "G17", "G18"],
    "P6": ["G5", "G21"],
    "P7": ["G7", "G19", "G22"],
}

# Rekomendasi penanganan & pencegahan praktis untuk masing-masing penyakit/hama
SOLUSI_PENANGANAN = {
    "P1": [
        "Potong dan musnahkan bagian pangkal batang yang membusuk agar spora tidak menyebar.",
        "Kurangi kelembapan berlebih di sekitar pangkal batang serta perbaiki drainase tanah.",
        "Oleskan fungisida berbahan aktif tembaga atau mankozeb pada area luka pemangkasan."
    ],
    "P2": [
        "Pangkas jaringan batang yang berlendir dan tampak basah menggunakan alat steril.",
        "Hindari penyiraman langsung ke luka batang dan jaga sirkulasi udara antar tiang panjat.",
        "Aplikasikan bakterisida berbahan aktif streptomisin sulfat atau tembaga hidroksida sesuai dosis."
    ],
    "P3": [
        "Potong cabang yang layu dan berwarna coklat hingga batas jaringan sehat, lalu bakar sisa potongan.",
        "Sterilkan alat potong dengan alkohol 70% setiap berpindah antar tanaman.",
        "Gunakan agen hayati Trichoderma sp. di sekitar perakaran dan fungisida sistemik bila serangan berat."
    ],
    "P4": [
        "Bersihkan gulma di sekitar kebun yang menjadi inang alternatif kutu daun.",
        "Semprotkan insektisida nabati (minyak mimba) atau air sabun lembut pada pucuk tunas muda.",
        "Gunakan insektisida berbahan aktif imidakloprid atau abamektin secara bijak jika populasi tinggi."
    ],
    "P5": [
        "Pangkas sulur, bunga, dan buah yang menunjukkan bercak jingga atau pembusukan.",
        "Jaga kebersihan sanitasi kebun dan kurangi kerimbunan tajuk agar sinar matahari masuk merata.",
        "Semprotkan fungisida berbahan aktif propineb, klorotalonil, atau azoksistrobin."
    ],
    "P6": [
        "Pasang perangkap likat kuning (yellow sticky trap) di beberapa titik kebun.",
        "Manfaatkan musuh alami seperti kumbang koksi (Menochilus sexmaculatus).",
        "Semprot bagian bawah sulur dengan insektisida nabati atau bahan aktif tiametoksam sesuai anjuran."
    ],
    "P7": [
        "Pangkas sulur yang kusam parah dan tingkatkan kelembapan kebun saat musim kemarau.",
        "Semprotkan air bertekanan sedang pada sulur untuk mengurangi populasi tungau.",
        "Gunakan akarisida spesifik berbahan aktif piridaben atau abamektin secara bergilir."
    ],
}
