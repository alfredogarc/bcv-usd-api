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
                  Ejemplo: {'moneda': 'USD', 'valor': 288.4494, 'fecha': '2025-12-23'}
        """
        try:
            # Realizar la petición HTTP (desactivar verificación SSL si hay problemas)
            response = requests.get(self.url, headers=self.headers, timeout=10, verify=False)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            usd_value = None
            fecha = None
            
            # Método 1: Usar el selector específico del BCV oficial (RECOMENDADO)
            # El valor oficial del USD está en div#dolar strong
            dolar_div = soup.find('div', id='dolar')
            if dolar_div:
                strong_tag = dolar_div.find('strong')
                if strong_tag:
                    usd_value = strong_tag.get_text(strip=True)
            
            # Método 2: Buscar en la sección oficial del BCV (fallback)
            if not usd_value:
                # Buscar en la clase específica del tipo de cambio oficial
                oficial_section = soup.find('div', class_='view-tipo-de-cambio-oficial-del-bcv')
                if oficial_section:
                    # Buscar el elemento que contiene "USD"
                    usd_elements = oficial_section.find_all(string=re.compile(r'USD', re.IGNORECASE))
                    for elemento in usd_elements:
                        parent = elemento.parent
                        if parent:
                            # Buscar el valor en el contenedor padre
                            container = parent.find_parent('div', class_='recuadrotsmc')
                            if container:
                                strong_tag = container.find('strong')
                                if strong_tag:
                                    usd_value = strong_tag.get_text(strip=True)
                                    break
            
            # Método 3: Buscar por patrón específico evitando la tabla de bancos (último recurso)
            if not usd_value:
                # Buscar elementos que contengan "USD" pero NO estén en la tabla de bancos
                elementos_usd = soup.find_all(string=re.compile(r'USD', re.IGNORECASE))
                for elemento in elementos_usd:
                    # Verificar que NO esté dentro de una tabla (para evitar Banesco, BBVA, etc.)
                    if elemento.find_parent('table'):
                        continue
                    
                    parent = elemento.parent
                    if parent:
                        # Buscar el strong más cercano
                        strong = parent.find_next('strong')
                        if strong:
                            texto = strong.get_text(strip=True)
                            # Verificar que sea un número válido
                            if re.match(r'\d{2,3}[,\.]\d+', texto):
                                usd_value = texto
                                break
            
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
