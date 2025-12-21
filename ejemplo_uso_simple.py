"""
Ejemplo de uso simple - Solo obtener el valor del USD
"""

from bcv_scraper import BCVScraper

# Forma 1: Obtener solo el valor numérico (más simple)
print("=== Forma más simple ===")
valor = BCVScraper().get_usd_value()
if valor:
    print(f"USD: {valor} Bs")
else:
    print("Error al obtener el valor")

print("\n" + "="*50 + "\n")

# Forma 2: Una línea
print("=== En una sola línea ===")
print(f"USD: {BCVScraper().get_usd_value()} Bs")
