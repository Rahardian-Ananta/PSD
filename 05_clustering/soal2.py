# jarak_satu_arah = 100  # dalam km
# konsumsi_bbm = 40       # 1 liter untuk 40 km
sisa_bensin = 1.5       # dalam liter
harga_per_liter = 10000 # dalam Rupiah


# total_jarak = jarak_satu_arah * 2

# total_kebutuhan_bbm = total_jarak / konsumsi_bbm

# bbm_yang_dibeli = total_kebutuhan_bbm - sisa_bensin

# total_biaya = bbm_yang_dibeli * harga_per_liter

# print("=== PERHITUNGAN KEBUTUHAN PERJALANAN DIMAS ===")
# print(f"Total jarak pulang-pergi : {total_jarak} km")
# print(f"Total kebutuhan bensin   : {total_kebutuhan_bbm} liter")
# print(f"Bensin yang harus dibeli : {bbm_yang_dibeli} liter")
# print(f"Total biaya bensin       : {total_biaya}")

sisa_bensin = 1.5       # dalam liter
harga_per_liter = 10000 # dalam Rupiah
total_biaya = sisa_bensin * harga_per_liter
print(f"Total biaya bensin       : {total_biaya}")