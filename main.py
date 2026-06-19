import csv
import os
import sys

# ==========================
# KONFIGURASI
# ==========================

FILE_CSV = "inventaris.csv"

# Struktur Data
inventaris = {}          # Dictionary (Hash Map)
antrian_barang = []      # Queue (FIFO)

# ==========================
# FUNGSI CSV
# ==========================

def muat_data_dari_csv():

    global inventaris

    if not os.path.exists(FILE_CSV):

        inventaris = {

            "BRG001": {
                "nama": "Laptop Asus",
                "stok": 10,
                "harga": 8500000
            },

            "BRG002": {
                "nama": "Mouse Logitech",
                "stok": 50,
                "harga": 150000
            }

        }

        simpan_data_ke_csv()
        return

    try:

        with open(FILE_CSV,
                  mode="r",
                  newline="",
                  encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                inventaris[row["ID_Barang"]] = {

                    "nama": row["Nama_Barang"],
                    "stok": int(row["Stok"]),
                    "harga": int(row["Harga"])

                }

    except Exception as e:

        print("Gagal membaca CSV :", e)


def simpan_data_ke_csv():

    with open(FILE_CSV,
              mode="w",
              newline="",
              encoding="utf-8") as file:

        fieldnames = [
            "ID_Barang",
            "Nama_Barang",
            "Stok",
            "Harga"
        ]

        writer = csv.DictWriter(file,
                                fieldnames=fieldnames)

        writer.writeheader()

        for id_barang, info in inventaris.items():

            writer.writerow({

                "ID_Barang": id_barang,
                "Nama_Barang": info["nama"],
                "Stok": info["stok"],
                "Harga": info["harga"]

            })


# ==========================
# MENU
# ==========================

def tampilkan_menu():

    print("\n")
    print("=" * 45)
    print("      SISTEM MANAJEMEN INVENTARIS")
    print("=" * 45)

    print("1. Lihat Semua Barang")
    print("2. Tambah Barang")
    print("3. Update Barang")
    print("4. Hapus Barang")
    print("5. Cari Barang")
    print("6. Sorting Barang")
    print("7. Tambah Antrian Barang")
    print("8. Lihat Antrian")
    print("9. Proses Antrian")
    print("10. Keluar")

    print("=" * 45)


# ==========================
# READ
# ==========================

def lihat_barang():

    if len(inventaris) == 0:

        print("Inventaris kosong.")
        return

    print("-" * 70)
    print(f"{'ID':<10}{'Nama':<25}{'Stok':<10}{'Harga'}")
    print("-" * 70)

    for id_barang, info in inventaris.items():

        print(
            f"{id_barang:<10}"
            f"{info['nama']:<25}"
            f"{info['stok']:<10}"
            f"Rp {info['harga']:,}"
        )

    print("-" * 70)


# ==========================
# CREATE
# ==========================

def tambah_barang():

    print("\n=== TAMBAH BARANG ===")

    id_barang = input("ID Barang : ").upper().strip()

    if id_barang in inventaris:

        print("ID sudah digunakan.")
        return

    nama = input("Nama Barang : ")

    try:

        stok = int(input("Stok : "))
        harga = int(input("Harga : "))

    except ValueError:

        print("Input harus berupa angka.")
        return

    inventaris[id_barang] = {

        "nama": nama,
        "stok": stok,
        "harga": harga

    }

    simpan_data_ke_csv()

    print("Barang berhasil ditambahkan.")

# ==========================
# UPDATE
# ==========================

def update_barang():

    print("\n=== UPDATE BARANG ===")

    id_barang = input("Masukkan ID Barang : ").upper().strip()

    if id_barang not in inventaris:
        print("Barang tidak ditemukan.")
        return

    print("Nama Barang :", inventaris[id_barang]["nama"])
    print("Stok Lama   :", inventaris[id_barang]["stok"])
    print("Harga Lama  :", inventaris[id_barang]["harga"])

    try:
        stok = int(input("Stok Baru  : "))
        harga = int(input("Harga Baru : "))
    except ValueError:
        print("Input harus berupa angka.")
        return

    inventaris[id_barang]["stok"] = stok
    inventaris[id_barang]["harga"] = harga

    simpan_data_ke_csv()

    print("Data berhasil diperbarui.")


# ==========================
# DELETE
# ==========================

def hapus_barang():

    print("\n=== HAPUS BARANG ===")

    id_barang = input("Masukkan ID Barang : ").upper().strip()

    if id_barang not in inventaris:
        print("Barang tidak ditemukan.")
        return

    konfirmasi = input("Yakin ingin menghapus? (y/n) : ").lower()

    if konfirmasi == "y":

        del inventaris[id_barang]

        simpan_data_ke_csv()

        print("Barang berhasil dihapus.")

    else:

        print("Penghapusan dibatalkan.")


# ==========================
# SEARCHING
# ==========================

def cari_barang():

    print("\n=== CARI BARANG ===")

    keyword = input("Masukkan ID / Nama Barang : ").lower()

    ditemukan = False

    print("-" * 70)
    print(f"{'ID':<10}{'Nama':<25}{'Stok':<10}{'Harga'}")
    print("-" * 70)

    for id_barang, info in inventaris.items():

        if keyword in id_barang.lower() or keyword in info["nama"].lower():

            print(
                f"{id_barang:<10}"
                f"{info['nama']:<25}"
                f"{info['stok']:<10}"
                f"Rp {info['harga']:,}"
            )

            ditemukan = True

    print("-" * 70)

    if not ditemukan:
        print("Barang tidak ditemukan.")


# ==========================
# SORTING (BUBBLE SORT)
# ==========================

def sorting_barang():

    if len(inventaris) == 0:
        print("Inventaris kosong.")
        return

    print("\n=== SORTING ===")
    print("1. Nama")
    print("2. Stok")
    print("3. Harga")

    pilihan = input("Pilih : ")

    data = list(inventaris.items())

    n = len(data)

    for i in range(n):

        for j in range(n - i - 1):

            tukar = False

            if pilihan == "1":

                if data[j][1]["nama"].lower() > data[j+1][1]["nama"].lower():
                    tukar = True

            elif pilihan == "2":

                if data[j][1]["stok"] > data[j+1][1]["stok"]:
                    tukar = True

            elif pilihan == "3":

                if data[j][1]["harga"] > data[j+1][1]["harga"]:
                    tukar = True

            if tukar:
                data[j], data[j+1] = data[j+1], data[j]

    print("-"*70)
    print(f"{'ID':<10}{'Nama':<25}{'Stok':<10}{'Harga'}")
    print("-"*70)

    for id_barang, info in data:

        print(
            f"{id_barang:<10}"
            f"{info['nama']:<25}"
            f"{info['stok']:<10}"
            f"Rp {info['harga']:,}"
        )

    print("-"*70)


# ==========================
# QUEUE (FIFO)
# ==========================

def tambah_antrian():

    print("\n=== TAMBAH ANTRIAN BARANG ===")

    id_barang = input("Masukkan ID Barang : ").upper().strip()

    if id_barang not in inventaris:
        print("Barang tidak ditemukan.")
        return

    try:
        jumlah = int(input("Jumlah Barang Masuk : "))
    except ValueError:
        print("Input harus angka.")
        return

    antrian_barang.append({
        "id": id_barang,
        "jumlah": jumlah
    })

    print("Barang berhasil masuk ke antrian.")


def lihat_antrian():

    print("\n=== DAFTAR ANTRIAN ===")

    if len(antrian_barang) == 0:
        print("Antrian kosong.")
        return

    for i, data in enumerate(antrian_barang, start=1):

        print(
            f"{i}. "
            f"{data['id']} - "
            f"{inventaris[data['id']]['nama']} "
            f"({data['jumlah']} unit)"
        )


def proses_antrian():

    if len(antrian_barang) == 0:
        print("Antrian kosong.")
        return

    data = antrian_barang.pop(0)

    inventaris[data["id"]]["stok"] += data["jumlah"]

    simpan_data_ke_csv()

    print("\nAntrian berhasil diproses.")
    print("Nama Barang :", inventaris[data["id"]]["nama"])
    print("Jumlah Masuk :", data["jumlah"])
    print("Stok Sekarang :", inventaris[data["id"]]["stok"])


# ==========================
# PROGRAM UTAMA
# ==========================

def main():

    muat_data_dari_csv()

    while True:

        tampilkan_menu()

        pilihan = input("Pilih menu (1-10): ")

        if pilihan == "1":
            lihat_barang()

        elif pilihan == "2":
            tambah_barang()

        elif pilihan == "3":
            update_barang()

        elif pilihan == "4":
            hapus_barang()

        elif pilihan == "5":
            cari_barang()

        elif pilihan == "6":
            sorting_barang()

        elif pilihan == "7":
            tambah_antrian()

        elif pilihan == "8":
            lihat_antrian()

        elif pilihan == "9":
            proses_antrian()

        elif pilihan == "10":

            print("\nTerima kasih telah menggunakan Sistem Manajemen Inventaris.")
            sys.exit()

        else:

            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()