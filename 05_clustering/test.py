# Menghitung volume kerucut
jari_jari = float(input("Masukkan jari-jari alas kerucut (dalam cm): "))
tinggi = float(input("Masukkan tinggi kerucut (dalam cm): "))
phi = 22/7
volume = (1/3) * phi * jari_jari * jari_jari * tinggi
print("Volume kerucut adalah: ", volume, "cm^3")