"""
API REST para obtener el valor del USD desde el BCV
Servidor FastAPI que expone endpoints para consultar el tipo de cambio

Uso:
    python api_server.py
    
    Luego acceder a:
    - http://localhost:8000/usd - Obtener valor del USD
    - http://localhost:8000/docs - Documentación interactiva
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from bcv_scraper import BCVScraper
import uvicorn
from datetime import datetime

# Crear la aplicación FastAPI
app = FastAPI(
    title="BCV USD API",
    description="API para obtener el tipo de cambio del USD desde el Banco Central de Venezuela",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia del scraper
scraper = BCVScraper()


@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "API del Banco Central de Venezuela",
        "version": "1.0.0",
        "endpoints": {
            "/usd": "Obtener valor del USD",
            "/usd/simple": "Obtener solo el valor numérico",
            "/health": "Estado del servidor",
            "/docs": "Documentación interactiva"
        }
    }


@app.get("/usd")
async def get_usd():
    """
    Obtiene el valor del USD desde el BCV
    
    Returns:
        JSON con el valor del USD, fecha y estado
    """
    try:
        resultado = scraper.obtener_valor_usd()
        
        if resultado['exito']:
            return JSONResponse(
                status_code=200,
                content={
                    "exito": True,
                    "moneda": resultado['moneda'],
                    "valor": resultado['valor'],
                    "valor_formateado": resultado['valor_formateado'],
                    "fecha": resultado['fecha'],
                    "timestamp": datetime.now().isoformat()
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=resultado['error']
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el valor del USD: {str(e)}"
        )


@app.get("/usd/simple")
async def get_usd_simple():
    """
    Obtiene solo el valor numérico del USD
    
    Returns:
        JSON con solo el valor numérico
    """
    try:
        valor = scraper.get_usd_value()
        
        if valor is not None:
            return JSONResponse(
                status_code=200,
                content={
                    "valor": valor
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="No se pudo obtener el valor del USD"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener el valor del USD: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servidor"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/convert/{amount}")
async def convert_usd_to_bs(amount: float):
    """
    Convierte una cantidad de USD a Bolívares
    
    Args:
        amount: Cantidad en USD a convertir
        
    Returns:
        JSON con la conversión
    """
    try:
        resultado = scraper.obtener_valor_usd()
        
        if resultado['exito']:
            bolivares = amount * resultado['valor']
            return JSONResponse(
                status_code=200,
                content={
                    "exito": True,
                    "usd": amount,
                    "bolivares": bolivares,
                    "tasa": resultado['valor'],
                    "fecha": resultado['fecha']
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=resultado['error']
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar la conversión: {str(e)}"
        )


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Iniciando servidor API del BCV")
    print("=" * 60)
    print("📍 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("=" * 60)
    print("\nEndpoints disponibles:")
    print("  GET /usd          - Obtener valor del USD completo")
    print("  GET /usd/simple   - Obtener solo el valor numérico")
    print("  GET /convert/{amount} - Convertir USD a Bs")
    print("  GET /health       - Estado del servidor")
    print("=" * 60)
    
    # Iniciar el servidor
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
