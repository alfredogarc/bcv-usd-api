"""
Ejemplo simple de uso del scraper del BCV
"""

from bcv_scraper import BCVScraper


# Ejemplo 1: Uso básico - Obtener y mostrar el valor
print("=== EJEMPLO 1: Uso básico ===\n")
scraper = BCVScraper()
scraper.mostrar_resultado()

print("\n" + "="*50 + "\n")

# Ejemplo 2: Obtener solo el valor numérico
print("=== EJEMPLO 2: Obtener solo el valor ===\n")
resultado = BCVScraper().obtener_valor_usd()

if resultado['exito']:
    print(f"El valor del USD es: {resultado['valor']} Bs")
    print(f"Fecha: {resultado['fecha']}")
else:
    print(f"Error: {resultado['error']}")

print("\n" + "="*50 + "\n")

# Ejemplo 3: Usar el valor en cálculos
print("=== EJEMPLO 3: Convertir USD a Bs ===\n")
resultado = BCVScraper().obtener_valor_usd()

if resultado['exito']:
    dolares = 100
    bolivares = dolares * resultado['valor']
    print(f"${dolares} USD = {bolivares:,.2f} Bs")
    print(f"Tasa: {resultado['valor']} Bs/USD")
