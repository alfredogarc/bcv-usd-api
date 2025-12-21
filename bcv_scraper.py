"""
Script para obtener el valor del USD desde el Banco Central de Venezuela (BCV)
Autor: Generado para scraping de bcv.org.ve
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import urllib3

# Suprimir advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BCVScraper:
    """Clase para hacer scraping del tipo de cambio del BCV"""
    
    def __init__(self):
        self.url = "https://www.bcv.org.ve"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def obtener_valor_usd(self):
        """
        Obtiene el valor del USD desde la página del BCV
        
        Returns:
            dict: Diccionario con el valor del USD, fecha y moneda
                  Ejemplo: {'moneda': 'USD', 'valor': 583.2838000, 'fecha': '2025-12-22'}
        """
        try:
            # Realizar la petición HTTP (desactivar verificación SSL si hay problemas)
            response = requests.get(self.url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar el valor del USD - Método 1: Por estructura de tabla
            usd_value = None
            fecha = None
            
            # Intentar encontrar el div o sección que contiene los tipos de cambio
            # Buscar por texto que contenga "USD" o "$"
            elementos_usd = soup.find_all(string=re.compile(r'USD|Dólar', re.IGNORECASE))
            
            for elemento in elementos_usd:
                # Buscar el valor numérico cerca del texto USD
                parent = elemento.parent
                if parent:
                    # Buscar hermanos o elementos cercanos que contengan números
                    siblings = parent.find_next_siblings()
                    for sibling in siblings:
                        texto = sibling.get_text(strip=True)
                        # Buscar patrón de número con comas
                        match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', texto)
                        if match:
                            usd_value = match.group(1)
                            break
                
                if usd_value:
                    break
            
            # Método 2: Buscar directamente por patrones numéricos grandes
            if not usd_value:
                # Buscar todos los elementos que contengan números grandes (típicos de tasas de cambio)
                all_text = soup.get_text()
                # Patrón para números grandes con formato venezolano (ej: 583,2838000)
                matches = re.findall(r'\b(\d{2,3}[,\.]\d{2,8})\b', all_text)
                if matches:
                    # Tomar el valor más grande (generalmente el USD es el más alto)
                    valores = []
                    for match in matches:
                        try:
                            valor_limpio = match.replace(',', '.')
                            valores.append((float(valor_limpio), match))
                        except ValueError:
                            continue
                    
                    if valores:
                        # Ordenar por valor y tomar el más grande
                        valores.sort(reverse=True)
                        usd_value = valores[0][1]
            
            # Buscar la fecha
            fecha_elementos = soup.find_all(string=re.compile(r'Fecha|fecha', re.IGNORECASE))
            for elemento in fecha_elementos:
                parent = elemento.parent
                if parent:
                    texto = parent.get_text()
                    # Buscar patrón de fecha
                    match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', texto)
                    if match:
                        fecha = f"{match.group(3)}-{match.group(2).zfill(2)}-{match.group(1).zfill(2)}"
                        break
            
            if not fecha:
                fecha = datetime.now().strftime('%Y-%m-%d')
            
            if usd_value:
                # Limpiar el valor (convertir coma a punto si es necesario)
                valor_limpio = usd_value.replace(',', '.')
                valor_float = float(valor_limpio)
                
                return {
                    'moneda': 'USD',
                    'valor': valor_float,
                    'valor_formateado': usd_value,
                    'fecha': fecha,
                    'exito': True
                }
            else:
                return {
                    'exito': False,
                    'error': 'No se pudo encontrar el valor del USD en la página'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'exito': False,
                'error': f'Error al conectar con el BCV: {str(e)}'
            }
        except Exception as e:
            return {
                'exito': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def get_usd_value(self):
        """
        Método simplificado que devuelve solo el valor numérico del USD
        
        Returns:
            float: Valor del USD, o None si hay error
        """
        resultado = self.obtener_valor_usd()
        if resultado['exito']:
            return resultado['valor']
        return None
    
    def mostrar_resultado(self):
        """Obtiene y muestra el valor del USD de forma formateada"""
        resultado = self.obtener_valor_usd()
        
        if resultado['exito']:
            print("=" * 50)
            print("BANCO CENTRAL DE VENEZUELA")
            print("TIPO DE CAMBIO DE REFERENCIA")
            print("=" * 50)
            print(f"Moneda: {resultado['moneda']}")
            print(f"Valor: {resultado['valor_formateado']}")
            print(f"Valor numérico: {resultado['valor']:.8f}")
            print(f"Fecha: {resultado['fecha']}")
            print("=" * 50)
        else:
            print("ERROR:", resultado['error'])
        
        return resultado


def main():
    """Función principal"""
    scraper = BCVScraper()
    resultado = scraper.mostrar_resultado()
    
    # Retornar solo el valor si fue exitoso
    if resultado['exito']:
        return resultado['valor']
    else:
        return None


if __name__ == "__main__":
    valor_usd = main()
    if valor_usd:
        print(f"\nValor del USD: {valor_usd}")
