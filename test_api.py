"""
Cliente de ejemplo para probar la API del BCV
Ejecuta este script después de iniciar el servidor API
"""

import requests
import time

API_URL = "http://localhost:8000"

def test_api():
    """Prueba todos los endpoints de la API"""
    
    print("=" * 60)
    print("🧪 PROBANDO API DEL BCV")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1️⃣ Test: Health Check")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("\n⚠️  Asegúrate de que el servidor esté corriendo:")
        print("   python api_server.py")
        return
    
    # Test 2: Root endpoint
    print("\n2️⃣ Test: Root Endpoint")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Endpoints disponibles: {list(data['endpoints'].keys())}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Get USD value (completo)
    print("\n3️⃣ Test: Obtener USD (completo)")
    try:
        response = requests.get(f"{API_URL}/usd")
        print(f"   Status: {response.status_code}")
        data = response.json()
        if data.get('exito'):
            print(f"   ✅ Valor: {data['valor']} Bs")
            print(f"   📅 Fecha: {data['fecha']}")
        else:
            print(f"   ❌ Error en respuesta")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Get USD value (simple)
    print("\n4️⃣ Test: Obtener USD (simple)")
    try:
        response = requests.get(f"{API_URL}/usd/simple")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   ✅ Valor: {data['valor']} Bs")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Convert USD to Bs
    print("\n5️⃣ Test: Convertir 100 USD a Bs")
    try:
        response = requests.get(f"{API_URL}/convert/100")
        print(f"   Status: {response.status_code}")
        data = response.json()
        if data.get('exito'):
            print(f"   ✅ {data['usd']} USD = {data['bolivares']:,.2f} Bs")
            print(f"   📊 Tasa: {data['tasa']} Bs/USD")
        else:
            print(f"   ❌ Error en respuesta")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("=" * 60)
    print(f"\n📚 Documentación interactiva: {API_URL}/docs")
    print("=" * 60)


if __name__ == "__main__":
    test_api()
