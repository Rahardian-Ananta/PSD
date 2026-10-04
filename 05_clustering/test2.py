# IF-ELSE Commmand
# nilai = int(input("Masukkan nilai pre-test anda :"))

# if nilai <= 80 :
#     print("Selamat, anda lulus pre-test")
# else:
#     print("Maaf, anda tidak lulus pre-test")

# IF-ELIF-ELSE Command
# roda = int(input("Masukkan jumlah roda kendaraan :"))

# if roda == 2 :
#     print("Kendaraan ini adalah sepeda motor")
# elif roda == 4 :
#     print("Kendaraan ini adalah mobil")
# elif roda == 3 :
#     print("Kendaraan ini adalah bajaj")
# else :
#     print("Kendaraan ini adalah truk")

# NESTED IFS Command
# member = str(input("Apakah anda seorrang member? (y/n): "))

# if member == "y" :
#     belanja = int(input("Masukkan jumlah belanja anda: "))
#     if belanja >= 500:
#         print("Selamat, anda mendapatkan diskon 10%")
#     elif belanja >= 1000:
#         print("Selamat, anda mendapat diskon 20%")

#     else:
#         print("Maaf, anda tidak mendapatkan diskon")
# else:
#     print("Maaf, anda bukan member, tidak mendapatkan diskon")

# IF-TENARY Command
# suhu = float(input("Masukkan suhu tubuh anda (celcius):"))

# status = "PUANAS" if suhu == 39.5 else "Hipotermia"
# print("Status suhu tubuh anda adalah:", status)

nilai = int(input("Masukkan nilai: "))
hasil = "A" if nilai >= 90 else "B" if nilai >= 80 else "C" if nilai >= 70 else "D" if nilai >= 60 else "E" if nilai >= 50 else "tidak ada hasil"
print("Hasil nilai anda adalah:", hasil)