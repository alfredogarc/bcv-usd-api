# 💱 API del Banco Central de Venezuela (BCV)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Scraper web y API REST para obtener el tipo de cambio del USD desde el [Banco Central de Venezuela](https://www.bcv.org.ve) en tiempo real.

## ✨ Características

- 🔄 Scraping automático del tipo de cambio USD/Bs
- 🚀 API REST con FastAPI
- 📊 Conversión automática USD ↔ Bs
- 📚 Documentación interactiva (Swagger UI)
- 🌐 CORS habilitado
- ⚡ Respuestas rápidas y confiables

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 💡 Uso del Scraper

### Uso básico
```python
from bcv_scraper import BCVScraper

# Obtener solo el valor numérico
valor = BCVScraper().get_usd_value()
print(f"USD: {valor} Bs")

# O con información completa
scraper = BCVScraper()
resultado = scraper.obtener_valor_usd()

if resultado['exito']:
    print(f"Valor: {resultado['valor']} Bs")
    print(f"Fecha: {resultado['fecha']}")
```

## 🌐 API REST

### Iniciar el servidor
```bash
python api_server.py
```

El servidor estará disponible en: `http://localhost:8000`

### Endpoints disponibles

#### 1. Obtener valor del USD completo
```
GET http://localhost:8000/usd
```

**Respuesta:**
```json
{
  "exito": true,
  "moneda": "USD",
  "valor": 285.059,
  "valor_formateado": "285,059",
  "fecha": "2025-12-21",
  "timestamp": "2025-12-21T13:30:00"
}
```

#### 2. Obtener solo el valor numérico
```
GET http://localhost:8000/usd/simple
```

**Respuesta:**
```json
{
  "valor": 285.059
}
```

#### 3. Convertir USD a Bolívares
```
GET http://localhost:8000/convert/100
```

**Respuesta:**
```json
{
  "exito": true,
  "usd": 100,
  "bolivares": 28505.9,
  "tasa": 285.059,
  "fecha": "2025-12-21"
}
```

#### 4. Estado del servidor
```
GET http://localhost:8000/health
```

#### 5. Documentación interactiva
```
http://localhost:8000/docs
```

## 📝 Ejemplos de Uso

### 🐍 Python

#### Opción 1: Usar el Scraper Directamente
```python
from bcv_scraper import BCVScraper

# Forma simple - Solo el valor
valor = BCVScraper().get_usd_value()
print(f"USD: {valor} Bs")

# Forma completa - Con toda la información
scraper = BCVScraper()
resultado = scraper.obtener_valor_usd()

if resultado['exito']:
    print(f"Moneda: {resultado['moneda']}")
    print(f"Valor: {resultado['valor']} Bs")
    print(f"Fecha: {resultado['fecha']}")
```

#### Opción 2: Consumir la API REST
```python
import requests

# Obtener valor del USD
response = requests.get("http://localhost:8000/usd/simple")
data = response.json()
print(f"USD: {data['valor']} Bs")

# Obtener información completa
response = requests.get("http://localhost:8000/usd")
data = response.json()
if data['exito']:
    print(f"Valor: {data['valor']} Bs")
    print(f"Fecha: {data['fecha']}")

# Convertir 100 USD a Bs
response = requests.get("http://localhost:8000/convert/100")
data = response.json()
print(f"100 USD = {data['bolivares']:,.2f} Bs")
print(f"Tasa: {data['tasa']} Bs/USD")
```

---

### 🔷 WinDev (PCSoft)

#### Ejemplo Básico - Obtener Valor del USD
```wlanguage
PROCEDURE GetUSDValue()

// Variables
sURL			is string		= "http://localhost:8000/usd/simple"
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant
nUSDValue		is numeric

// Configurar la petición
httpRQ.URL		= sURL
httpRQ.Method	= httpGet

// Ejecutar la petición
httpRP			= HTTPSend(httpRQ)

// Verificar si la petición fue exitosa
IF httpRP.StatusCode = 200 THEN
	// Parsear el JSON
	vJSON		= JSONToVariant(httpRP.Content)
	
	// Obtener el valor
	nUSDValue	= vJSON.valor
	
	// Mostrar el resultado
	Info("Valor del USD: " + NumToString(nUSDValue, "12.4f") + " Bs")
	
	RESULT nUSDValue
ELSE
	Error("Error al obtener el valor del USD")
	RESULT 0
END
```

#### Ejemplo en un Botón
```wlanguage
// Código del botón BTN_GetUSD
nValue			is numeric
nValue			= GetUSDValue()

IF nValue > 0 THEN
	EDT_USDValue	= NumToString(nValue, "12.4f")
END
```

#### Convertir USD a Bolívares
```wlanguage
PROCEDURE ConvertUSDtoBS(nAmountUSD is numeric)

// Variables
sURL			is string
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant

// Construir la URL
sURL			= "http://localhost:8000/convert/" + NumToString(nAmountUSD, "12.2f")

// Configurar y ejecutar la petición
httpRQ.URL		= sURL
httpRQ.Method	= httpGet
httpRP			= HTTPSend(httpRQ)

// Procesar respuesta
IF httpRP.StatusCode = 200 THEN
	vJSON		= JSONToVariant(httpRP.Content)
	
	IF vJSON.exito = True THEN
		Info(NumToString(vJSON.usd, "12.2f") + " USD = " + 
		     NumToString(vJSON.bolivares, "12.2f") + " Bs")
		RESULT vJSON.bolivares
	END
END

RESULT 0
```

#### Ejemplo Simplificado (Una Línea)
```wlanguage
PROCEDURE GetUSD_Simple()

// Variables
sResponse		is string
vJSON			is Variant

// Petición directa
sResponse		= HTTPRequest("http://localhost:8000/usd/simple")
vJSON			= JSONToVariant(sResponse)

RESULT vJSON.valor
```

**📄 Ver ejemplo completo:** [`ejemplo_windev.wl`](ejemplo_windev.wl)

---

### 🌐 JavaScript
```javascript
// Obtener valor del USD
fetch('http://localhost:8000/usd')
  .then(response => response.json())
  .then(data => console.log(`USD: ${data.valor} Bs`));

// Convertir USD a Bs
fetch('http://localhost:8000/convert/100')
  .then(response => response.json())
  .then(data => console.log(`100 USD = ${data.bolivares} Bs`));
```

## 🔧 Características

- ✅ Scraping robusto con múltiples métodos de extracción
- ✅ API REST con FastAPI
- ✅ Documentación automática (Swagger UI)
- ✅ CORS habilitado para peticiones desde cualquier origen
- ✅ Manejo de errores SSL
- ✅ Conversión automática de USD a Bolívares
- ✅ Endpoints simples y completos

## 📦 Dependencias

- `requests`: Para hacer peticiones HTTP
- `beautifulsoup4`: Para parsear HTML
- `lxml`: Parser HTML rápido
- `fastapi`: Framework para la API REST
- `uvicorn`: Servidor ASGI para FastAPI

## ⚠️ Notas

- El scraper desactiva la verificación SSL debido a problemas con el certificado del BCV
- Los valores se extraen directamente de la página web oficial del BCV
- La API puede ser accedida desde cualquier origen (CORS habilitado)
