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

## 📋 Archivos del Proyecto

- **`bcv_scraper.py`**: Scraper principal que extrae el valor del USD desde bcv.org.ve
- **`api_server.py`**: Servidor API REST con FastAPI
- **`ejemplo_uso.py`**: Ejemplos completos de uso del scraper
- **`ejemplo_uso_simple.py`**: Forma más simple de obtener el valor
- **`requirements.txt`**: Dependencias del proyecto

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 💡 Uso del Scraper

### Forma más simple (solo el valor)
```python
from bcv_scraper import BCVScraper

# Obtener solo el valor numérico
valor = BCVScraper().get_usd_value()
print(f"USD: {valor} Bs")
```

### Forma completa (con detalles)
```python
from bcv_scraper import BCVScraper

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

## 📝 Ejemplos de uso

### Ejecutar ejemplos
```bash
# Ejemplo simple
python ejemplo_uso_simple.py

# Ejemplos completos
python ejemplo_uso.py
```

### Usar la API desde Python
```python
import requests

# Obtener valor del USD
response = requests.get("http://localhost:8000/usd")
data = response.json()
print(f"USD: {data['valor']} Bs")

# Convertir 100 USD a Bs
response = requests.get("http://localhost:8000/convert/100")
data = response.json()
print(f"100 USD = {data['bolivares']} Bs")
```

### Usar la API desde JavaScript
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
