// ============================================
// EJEMPLO DE USO DE LA API BCV EN WINDEV
// PCSoft WinDev - WLanguage
// ============================================

// --------------------------------------------
// Método 1: Obtener solo el valor del USD
// --------------------------------------------
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
	Error("Error al obtener el valor del USD", "Código: " + httpRP.StatusCode)
	RESULT 0
END


// --------------------------------------------
// Método 2: Obtener información completa del USD
// --------------------------------------------
PROCEDURE GetCompleteInfo()

// Variables
sURL			is string		= "http://localhost:8000/usd"
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant
sInfo			is string

// Configurar la petición
httpRQ.URL		= sURL
httpRQ.Method	= httpGet

// Ejecutar la petición
httpRP			= HTTPSend(httpRQ)

// Verificar si la petición fue exitosa
IF httpRP.StatusCode = 200 THEN
	// Parsear el JSON
	vJSON		= JSONToVariant(httpRP.Content)
	
	// Verificar si fue exitoso
	IF vJSON.exito = True THEN
		// Construir información completa
		sInfo	= "BANCO CENTRAL DE VENEZUELA" + CR + CR
		sInfo	+= "Moneda: " + vJSON.moneda + CR
		sInfo	+= "Valor: " + NumToString(vJSON.valor, "12.4f") + " Bs" + CR
		sInfo	+= "Fecha: " + vJSON.fecha + CR
		sInfo	+= "Timestamp: " + vJSON.timestamp
		
		Info(sInfo)
		
		RESULT vJSON.valor
	ELSE
		Error("Error en la respuesta de la API")
		RESULT 0
	END
ELSE
	Error("Error al conectar con la API", "Código: " + httpRP.StatusCode)
	RESULT 0
END


// --------------------------------------------
// Método 3: Convertir USD a Bolívares
// --------------------------------------------
PROCEDURE ConvertUSDtoBS(nAmountUSD is numeric)

// Variables
sURL			is string
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant
sResult			is string

// Construir la URL
sURL			= "http://localhost:8000/convert/" + NumToString(nAmountUSD, "12.2f")

// Configurar la petición
httpRQ.URL		= sURL
httpRQ.Method	= httpGet

// Ejecutar la petición
httpRP			= HTTPSend(httpRQ)

// Verificar si la petición fue exitosa
IF httpRP.StatusCode = 200 THEN
	// Parsear el JSON
	vJSON		= JSONToVariant(httpRP.Content)
	
	// Verificar si fue exitoso
	IF vJSON.exito = True THEN
		// Construir resultado
		sResult	= NumToString(vJSON.usd, "12.2f") + " USD = "
		sResult	+= NumToString(vJSON.bolivares, "12.2f") + " Bs" + CR
		sResult	+= "Tasa: " + NumToString(vJSON.tasa, "12.4f") + " Bs/USD"
		
		Info(sResult)
		
		RESULT vJSON.bolivares
	ELSE
		Error("Error en la conversión")
		RESULT 0
	END
ELSE
	Error("Error al conectar con la API", "Código: " + httpRP.StatusCode)
	RESULT 0
END


// --------------------------------------------
// Método 4: Verificar estado del servidor
// --------------------------------------------
PROCEDURE CheckServerStatus()

// Variables
sURL			is string		= "http://localhost:8000/health"
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant

// Configurar la petición
httpRQ.URL		= sURL
httpRQ.Method	= httpGet

// Ejecutar la petición
httpRP			= HTTPSend(httpRQ)

// Verificar si la petición fue exitosa
IF httpRP.StatusCode = 200 THEN
	// Parsear el JSON
	vJSON		= JSONToVariant(httpRP.Content)
	
	IF vJSON.status = "ok" THEN
		Info("Servidor activo", "Timestamp: " + vJSON.timestamp)
		RESULT True
	ELSE
		Error("Servidor no responde correctamente")
		RESULT False
	END
ELSE
	Error("No se puede conectar al servidor", "Código: " + httpRP.StatusCode)
	RESULT False
END


// ============================================
// EJEMPLO DE USO EN UN BOTÓN
// ============================================

// Código del botón BTN_GetUSD
nValue			is numeric
nValue			= GetUSDValue()

IF nValue > 0 THEN
	EDT_USDValue	= NumToString(nValue, "12.4f")
END


// Código del botón BTN_Convert
nAmountUSD		is numeric		= Val(EDT_AmountUSD)
nBolivares		is numeric

nBolivares		= ConvertUSDtoBS(nAmountUSD)

IF nBolivares > 0 THEN
	EDT_ResultBS	= NumToString(nBolivares, "12.2f")
END


// Código del botón BTN_CheckServer
IF CheckServerStatus() THEN
	STC_Status		= "Servidor activo ✓"
	STC_Status..Color	= Green
ELSE
	STC_Status		= "Servidor inactivo ✗"
	STC_Status..Color	= Red
END


// ============================================
// EJEMPLO CON MANEJO DE ERRORES AVANZADO
// ============================================

PROCEDURE GetUSD_Advanced()

// Variables
sURL			is string		= "http://localhost:8000/usd/simple"
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant
nUSDValue		is numeric		= 0

// Usar bloque de excepción
WHEN EXCEPTION IN
	// Configurar timeout
	httpRQ.URL		= sURL
	httpRQ.Method	= httpGet
	httpRQ.Timeout	= 5000  // 5 segundos
	
	// Ejecutar la petición
	httpRP			= HTTPSend(httpRQ)
	
	// Verificar respuesta
	IF httpRP.StatusCode = 200 THEN
		vJSON		= JSONToVariant(httpRP.Content)
		nUSDValue	= vJSON.valor
		
		// Log exitoso
		Trace("USD obtenido correctamente: " + NumToString(nUSDValue, "12.4f"))
	ELSE
		// Log de error
		Trace("Error HTTP: " + httpRP.StatusCode)
		Error("Error al obtener el valor del USD")
	END
	
DO
	// Capturar cualquier excepción
	Error("Excepción al conectar con la API", ExceptionInfo())
	Trace("Excepción: " + ExceptionInfo())
END

RESULT nUSDValue


// ============================================
// EJEMPLO CON TIMER PARA ACTUALIZACIÓN AUTOMÁTICA
// ============================================

// Código de inicialización de la ventana
PROCEDURE WIN_Main_Initialization()

// Iniciar timer para actualizar cada 5 minutos
TimerSys(UpdateUSDValue, 300000, tsEnabled)  // 300000 ms = 5 minutos


// Procedimiento del timer
PROCEDURE UpdateUSDValue()

// Variables
nValue			is numeric

nValue			= GetUSDValue()

IF nValue > 0 THEN
	EDT_USDValue			= NumToString(nValue, "12.4f")
	STC_LastUpdate			= "Última actualización: " + DateTimeToString(DateTimeSys())
END


// ============================================
// EJEMPLO SIMPLIFICADO (UNA SOLA LÍNEA)
// ============================================

PROCEDURE GetUSD_Simple()

// Variables
sResponse		is string
vJSON			is Variant

// Petición directa
sResponse		= HTTPRequest("http://localhost:8000/usd/simple")
vJSON			= JSONToVariant(sResponse)

RESULT vJSON.valor


// ============================================
// EJEMPLO CON CLASE PERSONALIZADA
// ============================================

BCVClient is Class
	m_sBaseURL		is string	= "http://localhost:8000"
	m_nTimeout		is int		= 5000
END

// Constructor
PROCEDURE Constructor()
	m_sBaseURL		= "http://localhost:8000"
	m_nTimeout		= 5000
END

// Método para obtener USD
PROCEDURE GetUSD()

// Variables
sURL			is string
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant

sURL			= m_sBaseURL + "/usd/simple"

httpRQ.URL		= sURL
httpRQ.Method	= httpGet
httpRQ.Timeout	= m_sTimeout

httpRP			= HTTPSend(httpRQ)

IF httpRP.StatusCode = 200 THEN
	vJSON		= JSONToVariant(httpRP.Content)
	RESULT vJSON.valor
ELSE
	RESULT 0
END

// Método para convertir
PROCEDURE Convert(nAmount is numeric)

// Variables
sURL			is string
httpRQ			is httpRequest
httpRP			is httpResponse
vJSON			is Variant

sURL			= m_sBaseURL + "/convert/" + nAmount

httpRQ.URL		= sURL
httpRQ.Method	= httpGet
httpRQ.Timeout	= m_sTimeout

httpRP			= HTTPSend(httpRQ)

IF httpRP.StatusCode = 200 THEN
	vJSON		= JSONToVariant(httpRP.Content)
	RESULT vJSON.bolivares
ELSE
	RESULT 0
END


// ============================================
// USO DE LA CLASE
// ============================================

// Variables globales
goBCVClient		is BCVClient

// Inicialización
goBCVClient		= new BCVClient()

// Uso
nUSD			is numeric
nUSD			= goBCVClient.GetUSD()
Info("USD: " + nUSD)

nBS				is numeric
nBS				= goBCVClient.Convert(100)
Info("100 USD = " + nBS + " Bs")


// ============================================
// NOTAS IMPORTANTES
// ============================================

// 1. Asegúrate de que el servidor API esté corriendo:
//    python api_server.py

// 2. Si el servidor está en otra máquina, cambia localhost por la IP:
//    sURL = "http://192.168.1.100:8000/usd/simple"

// 3. Para usar HTTPS, asegúrate de tener certificado SSL configurado

// 4. Las variables están alineadas con TAB para mejor legibilidad

// 5. Estructuras de control en inglés (IF/THEN/ELSE/END)

// 6. Para depuración, usa Trace() para ver las respuestas:
//    Trace(httpRP.Content)

// 7. Nombres de variables en inglés siguiendo convenciones WinDev:
//    - s = string
//    - n = numeric
//    - b = boolean
//    - v = variant
//    - o = object

