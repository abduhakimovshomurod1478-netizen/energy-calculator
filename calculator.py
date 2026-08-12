import math

U = float(input("Kuchlanish U (V): "))
I = float(input("Tok I (A): "))
cos_phi = float(input("cos φ: "))

P = math.sqrt(3) * U * I * cos_phi

print(f"Aktiv quvvat: {P / 1000:.2f} kW")
