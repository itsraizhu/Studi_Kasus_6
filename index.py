import json
import os
from time import sleep
from prettytable import PrettyTable

FILE_NAME = "inventaris.json"


def muat_data():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Peringatan: Gagal membaca file {FILE_NAME} ({e}). Memulai dengan data kosong.")
        sleep(2)
        return []


def simpan_data(data_inventaris):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(data_inventaris, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saat menyimpan data: {e}")
        sleep(2)


def generate_kode_barang(data_inventaris):
    nomor_tertinggi = 0
    for barang in data_inventaris:
        kode = barang.get("kode", "").strip()
        if kode.upper().startswith("BRG"):
            bagian_angka = kode[3:]
            if bagian_angka.isdigit():
                nomor = int(bagian_angka)
                if nomor > nomor_tertinggi:
                    nomor_tertinggi = nomor

    calon_nomor = nomor_tertinggi + 1
    kode_terpakai = {b["kode"].strip().lower() for b in data_inventaris}
    while f"brg{calon_nomor:03d}" in kode_terpakai:
        calon_nomor += 1

    return f"BRG{calon_nomor:03d}"


def tampilkan_inventaris(data_inventaris):
    os.system("cls")
    print("DAFTAR STOK BARANG")
    if len(data_inventaris) == 0:
        print("Data barang masih kosong.")
        return

    table = PrettyTable()
    table.field_names = ["No", "Kode Barang", "Nama Barang", "Stok", "Harga", "Total"]

    total_semua = 0
    no = 1
    for barang in data_inventaris:
        harga = barang["harga"]
        stok = barang["stok"]
        total_harga = stok * harga
        total_semua += total_harga

        harga_formatted = f"Rp{harga:,}".replace(",", ".")
        total_formatted = f"Rp{total_harga:,}".replace(",", ".")
        table.add_row([no, barang["kode"], barang["nama"], stok, harga_formatted, total_formatted])
        no += 1

    print(table)
    print(f"Total Nilai Keseluruhan: Rp{total_semua:,}".replace(",", "."))


def tambah_barang(data_inventaris):
    os.system("cls")
    print("TAMBAH BARANG BARU")

    kode = generate_kode_barang(data_inventaris)
    print(f"Kode Barang (Otomatis): {kode}")

    while True:
        nama = input("Masukkan Nama Barang: ").strip()
        if not nama:
            print("Nama barang tidak boleh kosong!")
            continue
        break

    while True:
        try:
            stok = int(input("Masukkan Jumlah Stok: "))
            if stok < 0:
                print("Stok tidak boleh bernilai negatif!")
                continue
            break
        except ValueError:
            print("Stok harus berupa angka bulat!")

    while True:
        try:
            harga = int(input("Masukkan Harga Barang: "))
            if harga < 0:
                print("Harga tidak boleh bernilai negatif!")
                continue
            break
        except ValueError:
            print("Harga harus berupa angka bulat!")

    total = stok * harga
    print(f"Total Nilai Barang: Rp{total:,}".replace(",", "."))

    barang_baru = {
        "kode": kode,
        "nama": nama,
        "stok": stok,
        "harga": harga
    }

    data_inventaris.append(barang_baru)
    simpan_data(data_inventaris)
    print("Data barang berhasil disimpan.")


def cari_barang(data_inventaris):
    os.system("cls")
    print("CARI BARANG")
    if len(data_inventaris) == 0:
        print("Data barang masih kosong.")
        return

    kata_kunci = input("Masukkan Kode atau Nama Barang yang dicari: ").strip().lower()
    if not kata_kunci:
        print("Kata kunci pencarian tidak boleh kosong!")
        return

    hasil = []
    total_cari = 0
    no = 1
    for barang in data_inventaris:
        if kata_kunci in barang["kode"].lower() or kata_kunci in barang["nama"].lower():
            harga = barang["harga"]
            stok = barang["stok"]
            total_harga = stok * harga
            total_cari += total_harga

            harga_formatted = f"Rp{harga:,}".replace(",", ".")
            total_formatted = f"Rp{total_harga:,}".replace(",", ".")
            hasil.append([no, barang["kode"], barang["nama"], stok, harga_formatted, total_formatted])
            no += 1

    if hasil:
        table = PrettyTable()
        table.field_names = ["No", "Kode Barang", "Nama Barang", "Stok", "Harga", "Total"]
        for baris in hasil:
            table.add_row(baris)
        print(table)
        print(f"Total Nilai Hasil Pencarian: Rp{total_cari:,}".replace(",", "."))
    else:
        print("Barang tidak ditemukan.")


def ubah_stok(data_inventaris):
    os.system("cls")
    print("UBAH STOK BARANG")
    if len(data_inventaris) == 0:
        print("Data barang masih kosong.")
        return

    kode = input("Masukkan Kode Barang yang ingin diubah stoknya: ").strip().lower()
    ditemukan = False

    for barang in data_inventaris:
        if barang["kode"].strip().lower() == kode:
            total_lama = barang["stok"] * barang["harga"]
            print(f"Barang ditemukan: {barang['nama']} (Stok: {barang['stok']} | Total: Rp{total_lama:,})".replace(",", "."))
            while True:
                try:
                    stok_baru = int(input("Masukkan Stok Baru: "))
                    if stok_baru < 0:
                        print("Stok tidak boleh bernilai negatif!")
                        continue
                    barang["stok"] = stok_baru
                    break
                except ValueError:
                    print("Stok harus berupa angka bulat!")

            simpan_data(data_inventaris)
            total_baru = barang["stok"] * barang["harga"]
            print(f"Stok berhasil diperbarui. Total Nilai Baru: Rp{total_baru:,}".replace(",", "."))
            ditemukan = True
            break

    if not ditemukan:
        print("Kode barang tidak ditemukan.")


def hapus_barang(data_inventaris):
    os.system("cls")
    print("HAPUS BARANG")
    if len(data_inventaris) == 0:
        print("Data barang masih kosong.")
        return

    kode = input("Masukkan Kode Barang yang ingin dihapus: ").strip().lower()
    ditemukan = False

    for barang in data_inventaris:
        if barang["kode"].strip().lower() == kode:
            ditemukan = True
            konfirmasi = input(f"Yakin ingin menghapus '{barang['nama']}' ({barang['kode']})? (y/n): ").strip().lower()
            if konfirmasi == "y":
                data_inventaris.remove(barang)
                simpan_data(data_inventaris)
                print("Barang berhasil dihapus.")
            else:
                print("Penghapusan dibatalkan.")
            break

    if not ditemukan:
        print("Kode barang tidak ditemukan.")


def main():
    data_inventaris = muat_data()

    while True:
        os.system("cls")
        print("MENU INVENTARIS BARANG")
        print("1. Lihat Data Barang")
        print("2. Tambah Data Barang")
        print("3. Cari Data Barang")
        print("4. Ubah Stok Barang")
        print("5. Hapus Data Barang")
        print("6. Keluar")

        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == "1":
            tampilkan_inventaris(data_inventaris)
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "2":
            tambah_barang(data_inventaris)
            sleep(2)
        elif pilihan == "3":
            cari_barang(data_inventaris)
            input("\nTekan Enter untuk kembali ke menu...")
        elif pilihan == "4":
            ubah_stok(data_inventaris)
            sleep(2)
        elif pilihan == "5":
            hapus_barang(data_inventaris)
            sleep(2)
        elif pilihan == "6":
            os.system("cls")
            print("Program selesai.")
            sleep(1)
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1-6.")
            sleep(1.5)


if __name__ == "__main__":
    main()
