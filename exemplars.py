"""Curated exemplar ads extracted from Skydropx campaigns 2025.

Google Ads source: ~90 sheets, 760 headlines, 351 descriptions, 244 campaign copies.
Meta source: ~63 sheets, 184 post copies, 183 encabezados, 189 copy de imagen.

These exemplars teach the LLM the real voice, structure, and patterns
used in Skydropx campaigns across both platforms.
"""

# =========================================================================
# GOOGLE ADS EXEMPLARS
# =========================================================================

# --- RSA HEADLINES (max 30 chars) organized by copy technique ---

HEADLINE_EXEMPLARS = {
    "action": [
        "Envía a todo México",
        "Cotiza envíos al instante",
        "Conecta tu tienda hoy mismo",
        "Integra tu ecommerce y envía",
        "Rastrea envíos en tiempo real",
        "Activa tu cuenta y envía ya",
        "Crea guías en segundos",
        "Protege tus envíos en Skydropx",
        "Descubre tarifas increíbles",
        "Prueba Fulfillment de Skydropx",
        "Elige tu paquetería ideal",
        "Cotiza con más paqueterías",
    ],
    "benefit": [
        "Agiliza tus envíos",
        "Reduce costos fácilmente",
        "Simplifica tus envíos hoy",
        "Optimiza tu gestión de envíos",
        "Ahorra tiempo en tus envíos",
        "Mejora tu logística hoy",
        "Reduce tiempo y costos",
        "Menos esfuerzo, más envíos",
        "Más alcance con menos costo",
        "Ahorra en cada envío fácil",
        "Optimiza tus envíos fácilmente",
        "Simplifica tu logística hoy",
    ],
    "brand_first": [
        "Skydropx: todo en envíos",
        "Skydropx tu aliado logístico",
        "Skydropx compara paqueterías",
        "Skydropx: envios automáticos",
        "Skydropx: Envíos sin estrés",
        "Skydropx optimiza tu logística",
        "Skydropx: logística cercana",
        "Skydropx: Envíos para todos",
        "Skydropx gestiona tus envíos",
        "Skydropx mejora tu logística",
    ],
    "question": [
        "¿Tus envíos son un caos?",
        "¿Sigues creando envíos a mano?",
        "¿Pierdes horas en envíos?",
        "¿Tu envío llegó a otro lado?",
        "¿Y si automatizas tus envíos?",
        "¿Errores en tus envíos?",
        "¿Tu logística es un caos?",
        "¿Realizas muchos envíos?",
        "¿Problemas con envios?",
        "¿Aún te da miedo hacer envios?",
    ],
    "promo": [
        "Cotiza envíos gratis",
        "Cashback en tu primer envío",
        "Envía aquí y gana cashback",
        "Gana desde el primer envío",
        "Usa el cupón IMPULSO50",
        "Recibe hasta 50% cashback",
        "Envíos prepagados e inmediatos",
        "Compra guías por adelantado",
    ],
    "feature_specific": [
        "Procesa envíos en lote",
        "Genera guías al instante",
        "Notificaciones al instante",
        "Envía nacional e internacional",
        "Control total de tus envíos",
        "Múltiples paqueterías aquí",
        "Logística sin complicaciones",
        "Tecnología para tus envíos",
        "Envíos masivos para empresas",
        "Paqueterías al instante",
        "Tu plataforma de logística",
        "Más cobertura, menos límites",
    ],
}

# --- RSA DESCRIPTIONS (max 90 chars) ---

DESCRIPTION_EXEMPLARS = [
    "Crea, cotiza, rastrea y sincroniza tus pedidos desde una sola plataforma. ¡Envía ahora!",
    "Ahorra tiempo al enviar con las mejores tarifas y paqueterías. ¡Agenda tu demo!",
    "Rastrea tus paquetes y programa recolecciones según necesites. ¡Crea tu cuenta ya!",
    "Gestiona tus envíos fácil, rápido y con tarifas competitivas. ¡Agenda una demo!",
    "Conecta tu tienda y automatiza cada envío en segundos. Empieza con Skydropx hoy.",
    "Reduce errores manuales y automatiza toda tu logística en Skydropx. ¡Prueba gratis!",
    "Compara transportadoras, ahorra tiempo y optimiza tus envíos. ¡Pruébalo ahora!",
    "Integra tu ecommerce y gestiona pedidos sin errores. Activa tu integración hoy.",
    "Centraliza y automatiza tu logística en un solo lugar con Skydropx. ¡Empieza hoy!",
    "Cotiza en Skydropx y elige la mejor opción para entregas rápidas en todo México.",
    "Tus envíos protegidos ante robo, daños y extravíos. ¡Protégelos ahora!",
    "Centraliza envíos y compara paqueterías. Crea tu cuenta hoy.",
    "Deja lo manual. Automatiza tus envíos y ahorra tiempo con Skydropx.",
    "Carga tus envíos en Excel y genera guías automáticas. Centraliza todo en Skydropx.",
    "Envía desde México al mundo con tarifas competitivas. Cotiza hoy y crea tu cuenta.",
    "Tecnología para tu negocio. Cotiza, envía y rastrea en un solo lugar. ¡Empieza ya!",
    "La logística de tu negocio en un solo lugar. ¡Envía ahora fácil con Skydropx!",
    "Selecciona la paquetería perfecta en cada envío según lo que necesites. ¡Pruébalo!",
    "Optimiza tu logística y recibe cashback en tu primer envío. ¡Regístrate ya!",
    "Decide mejor con datos y visibilidad total. Empieza gratis ahora.",
]

# --- CAMPAIGN / IMAGE AD COPIES (Título + Descripción for display ads) ---

CAMPAIGN_EXEMPLARS = [
    {
        "titulo": "Optimiza tu logística desde hoy",
        "descripcion": "Centraliza, automatiza y reduce errores en tus envíos SIN COSTO solo con regístrarte ahora en Skydropx.",
    },
    {
        "titulo": "Conecta tu tienda online facilmente",
        "descripcion": "Automatiza tus envíos y accede hoy a mejores tarifas al hablar con un asesor de Skydropx.",
    },
    {
        "titulo": "¿Tienes convenios con las paqueterías?",
        "descripcion": "Conectálos en un par de clics y comienza a enviar sin costo desde hoy con Skydropx.",
    },
    {
        "titulo": "¿Tardas mucho creando tus envíos?",
        "descripcion": "Crea plantillas de dirección y empaque para agilizar tu logística, ¡inicia hoy mismo!",
    },
    {
        "titulo": "¿La logística de tu negocio es un caos?",
        "descripcion": "Habla con nuestros asesores y descubre como optimizar tu logística en segundos con Skydropx.",
    },
    {
        "titulo": "Cotiza y descubre la mejor opción para tus envíos",
        "descripcion": "Conecta tus paqueterías favoritas y administra todos tus convenios en un solo lugar.",
    },
    {
        "titulo": "Automatiza tus envíos y ahorra tiempo",
        "descripcion": "Crea hoy tu cuenta Skydropx y personaliza las notificaciones que recibirán tus clientes.",
    },
    {
        "titulo": "¿Creció tu negocio pero no tu logística?",
        "descripcion": "Escala sin límites con Skydropx: integra, automatiza y rastrea en un solo lugar.",
    },
    {
        "titulo": "Reduce el tiempo de tus operaciones logísticas",
        "descripcion": "Integra tus paqueterías favoritas y haz envíos a un clic sin procesos complicados.",
    },
    {
        "titulo": "El control de tu negocio a un solo clic",
        "descripcion": "Contacta a un asesor y empieza a centralizar tus envíos desde una plataforma más fácil.",
    },
]

# --- TOP CTAs used in real Google Ads campaigns ---

CTA_EXEMPLARS = [
    "¡Agenda tu demo!",
    "¡Prueba gratis!",
    "¡Empieza hoy!",
    "¡Crea tu cuenta gratis!",
    "¡Envía ya!",
    "¡Pruébalo ahora!",
    "¡Comienza ya!",
    "¡Crea tu cuenta!",
    "¡Regístrate ya!",
    "¡Activa tu cuenta hoy!",
]

# --- COPY PATTERNS ANALYSIS (for prompt context) ---

COPY_PATTERNS = """
PATRONES DE COPY REALES DE SKYDROPX (extraídos de 760+ headlines y 350+ descriptions):

ESTRUCTURA DE HEADLINES (max 30 chars):
- 63% de headlines usan 26-30 chars (aprovechan el espacio)
- 32% usan 21-25 chars
- Promedio: 26 chars
- 0% excede 30 chars

TECNICAS DE HEADLINE MAS USADAS (en orden de frecuencia):
1. ACCION/IMPERATIVO (24%): Verbos directos - "Envía", "Cotiza", "Conecta", "Integra", "Rastrea", "Activa", "Crea"
2. URGENCIA/PROMO (13%): "hoy", "ahora", "ya", "gratis", cupones, cashback
3. BENEFICIO (8%): "Ahorra", "Reduce", "Simplifica", "Optimiza", "Mejora"
4. FEATURE (55%): Funcionalidades específicas como paqueterías, rastreo, cotizador, masivos
5. BRAND-FIRST (3%): Comienzan con "Skydropx:" o "Skydropx"
6. PREGUNTA (2%): "¿Tus envíos son un caos?", "¿Sigues creando envíos a mano?"

FEATURES MAS PROMOCIONADAS:
1. Cotizador/comparar tarifas (más mencionado)
2. Múltiples paqueterías en un solo lugar
3. Automatización de envíos
4. Rastreo en tiempo real
5. Creación de guías
6. Integración con ecommerce
7. Carga masiva de envíos
8. Envíos internacionales
9. Notificaciones a clientes
10. Facturación automática

ESTRUCTURA DE DESCRIPTIONS (max 90 chars):
- 61% usan 81-90 chars (aprovechan al máximo)
- Promedio: 81 chars
- Siempre terminan con CTA: "¡Agenda tu demo!", "¡Prueba gratis!", "¡Envía ya!"
- Estructura: [Beneficio/acción] + [contexto] + [CTA con ¡!]

PAQUETERIAS MENCIONADAS FRECUENTEMENTE:
México: DHL, FedEx, Estafeta, Redpack, Paquetexpress, 99minutos, AMPM, Quality Post, Estrella Blanca
Colombia: Servientrega, TCC, Coordinadora, Deprisa, InterRapidísimo
"""


# =========================================================================
# META ADS EXEMPLARS
# =========================================================================

# --- POST COPY (250-450 chars, SIEMPRE con emojis como bullets) ---

META_POST_COPY_EXEMPLARS = [
    # Promo / Cashback
    (
        "¡Cámbiate a Skydropx y gana más!\n\n"
        "Únete hoy y recibe 50 % extra del valor de tu primera recarga al realizarla.\n\n"
        "⏰ Cotiza en segundos\n"
        "🚛 Compara transportadoras\n"
        "🗺️ Rastrea tus paquetes\n\n"
        "¡Cambia la forma en la que haces tus envíos!\n"
        "¡Revoluciona tu logística hoy con Skydropx y gana más!\n"
        "¡Pide tu demo hoy!"
    ),
    (
        "¡Únete y obtén hasta 30% de cashback para tus primeros envíos!\n\n"
        "Skydropx te permite:\n"
        "🔥 Integrar múltiples opciones de ecommerce\n"
        "🔥 Programar recolecciones GRATIS\n"
        "🔥 Crear lotes de envíos desde CSV y Excel.\n\n"
        "Anímate y descubre lo fácil que es optimizar tus envíos.\n"
        "¡Solicita tu demo! 👇"
    ),
    # Enterprise
    (
        "Si tu operación ya superó los 300 envíos al mes, no tiene sentido seguir "
        "pagando como si estuvieras empezando.\n\n"
        "🚀 Con la tarifa Enterprise de Skydropx ahorras mientras cumples con tus entregas.\n"
        "💼 Condiciones pensadas para alto volumen.\n"
        "📊 Visibilidad clara de tus costos por paquetería.\n"
        "🖥️ Gestión centralizada de todos tus envíos.\n\n"
        "🚀 Activa tu cuenta Skydropx hoy y deja de pagar de más."
    ),
    # Integración ecommerce
    (
        "¿Todavía creas tus envíos uno por uno?\n\n"
        "Con Skydropx conectas tu tienda online y automatizas todo:\n"
        "📦 Importación automática de pedidos\n"
        "🚛 Cotización y comparación de paqueterías\n"
        "✅ Generación de guías con un clic\n\n"
        "Tu tiempo vale más que los procesos manuales.\n"
        "¡Agenda tu demo gratuita!"
    ),
    # Plataforma general
    (
        "¡No pierdas más tiempo buscando mil opciones para tus envíos!\n\n"
        "Con Skydropx puedes:\n"
        "📦 Cotizar con múltiples paqueterías\n"
        "🚛 Comparar precios y tiempos de entrega\n"
        "✅ Generar guías en segundos\n\n"
        "Todo desde una sola plataforma.\n"
        "¡Solicita tu prueba gratuita hoy!"
    ),
    # MyShipHub
    (
        "Tus envíos no pueden esperar a que abras cinco portales distintos.\n\n"
        "Con MyShipHub ves, en una sola interfaz, lo que ofrece cada plataforma "
        "logística para tu pedido:\n"
        "⚡ Resultados en tiempo real.\n"
        "📊 Comparación clara de precio, servicio y tiempo estimado.\n"
        "🖥️ Interfaz amigable e intuitiva.\n\n"
        "✅ Prueba MyShipHub y resuelve tus envíos en minutos."
    ),
    # Protección
    (
        "Protege cada uno de tus envíos con la cobertura de Skydropx.\n\n"
        "📦 Asegura tus paquetes ante robo, daño o extravío\n"
        "🛡️ Cobertura desde el momento de la recolección\n"
        "✅ Proceso de reclamación simple y rápido\n\n"
        "Tu tranquilidad no tiene precio.\n"
        "¡Activa tu protección hoy!"
    ),
    # Skydropx Pro
    (
        "Automatiza tus envíos y tu facturación con solo un par de clics.\n\n"
        "Skydropx Pro es una plataforma que te permite:\n"
        "💻 Centralizar tu logística\n"
        "📦 Cotizar, comparar y enviar\n"
        "📄 Facturar automáticamente.\n\n"
        "Todo esto y más, sin procesos complicados y desde un solo lugar.\n"
        "¿Qué estás esperando para probar Skydropx Pro?\n"
        "¡Agenda ahora una sesión de prueba sin costo!"
    ),
    # Estafeta Recovery
    (
        "¿Tu proveedor dejó de operar? ¡No detengas tu logística!\n\n"
        "Con Skydropx continúas tus envíos sin interrupciones:\n"
        "🚀 Integración inmediata con Estafeta y +30 paqueterías.\n"
        "🖥️ Plataforma lista para uso en minutos.\n"
        "📊 Seguimiento y métricas en tiempo real.\n"
        "✅ Sin papeleos ni pasos adicionales.\n\n"
        "📦 Actívalo hoy y mantén tu operación en movimiento."
    ),
    # COD
    (
        "¿Tus clientes prefieren pagar contra entrega?\n\n"
        "Con Skydropx activas el servicio de cobro contra entrega (COD) "
        "para tus envíos nacionales:\n"
        "💰 Cobra en efectivo o con terminal\n"
        "📦 Compatible con múltiples paqueterías\n"
        "📊 Visibilidad del estatus de cobro en tiempo real\n\n"
        "¡Solicita tu demo y actívalo hoy!"
    ),
]

# --- ENCABEZADOS / HEADLINES META (max 25 chars) ---
# 63% usan emoji al FINAL, 37% sin emoji

META_ENCABEZADO_EXEMPLARS = {
    "con_emoji": [
        "Cambia, gana y crece 🔝",
        "Gestiona y envía fácil 📦",
        "Cotiza tus envíos rápido ⚡",
        "Envíos nacionales para ti 📦",
        "Ahorra en cada envío 💰",
        "Envía fácil con Skydropx 📦",
        "Optimiza tu logística 🚛",
        "Envíos masivos ágiles 📦",
        "Reactiva tu logística 🚀",
        "Protege tus envíos 🛡️",
        "Tu logística, más simple 📦",
        "Compara y ahorra hoy 💸",
    ],
    "sin_emoji": [
        "Haz tus envíos fácilmente",
        "Envíos nacionales para ti",
        "Centraliza tu operación",
        "Automatiza tus envíos hoy",
        "Compara envíos al instante",
        "Tu logística en un clic",
        "Factura envíos rápido",
        "Simplifica tu operación",
    ],
}

# --- DESCRIPCIONES META (max 30 chars) ---
# 52% usan emoji al FINAL, 48% sin emoji

META_DESCRIPCION_EXEMPLARS = {
    "con_emoji": [
        "Gana más con tus envíos 🚛",
        "Optimiza tu logística 🚛📦",
        "Automatiza envíos desde ya ⚡",
        "Tu logística en un solo lugar 📦",
        "¡Cashback al unirte! 💸💸",
        "Compara envíos al instante 📊",
        "Factura y envía en automático ⚡",
        "Envía más, paga menos 💰",
        "Protege cada paquete 🛡️",
        "Ahorra con cada envío 💸",
    ],
    "sin_emoji": [
        "Activa tu cuenta Skydropx hoy",
        "Compara envíos al instante",
        "Simplifica tu logística hoy",
        "Gestiona envíos desde un lugar",
        "Tu logística en un solo lugar",
        "Envíos sin complicaciones",
        "Automatiza tus envíos desde ya",
        "Optimiza tu operación logística",
    ],
}

# --- COPY DE LA IMAGEN (texto sobre la imagen, SIN emojis) ---
# Estructura: Título + Copy in/Característica + CTA

META_COPY_IMAGEN_EXEMPLARS = [
    {
        "titulo": "Optimiza tu logística desde hoy",
        "copy_in": "Centraliza, automatiza y reduce errores en tus envíos SIN COSTO",
        "cta": "Agenda una demo",
    },
    {
        "titulo": "Conecta tu tienda online fácilmente",
        "copy_in": "Automatiza tus envíos y accede hoy a mejores tarifas",
        "cta": "Agenda tu demo",
    },
    {
        "titulo": "¿Tienes convenios con las paqueterías?",
        "copy_in": "Conectálos en un par de clics y comienza a enviar sin costo",
        "cta": "Solicita tu demo",
    },
    {
        "titulo": "¿Tardas mucho creando tus envíos?",
        "copy_in": "Crea plantillas de dirección y empaque para agilizar tu logística",
        "cta": "Agenda una demo",
    },
    {
        "titulo": "¿La logística de tu negocio es un caos?",
        "copy_in": "Descubre como optimizar tu logística en segundos con Skydropx",
        "cta": "Agenda tu demo",
    },
    {
        "titulo": "Tu logística necesita escalar",
        "copy_in": "Más paqueterías, mejor precio, menos esfuerzo operativo",
        "cta": "Pruébalo gratis",
    },
    {
        "titulo": "Cotiza y descubre la mejor opción para tus envíos",
        "copy_in": "Conecta tus paqueterías favoritas y administra todos tus convenios en un solo lugar",
        "cta": "Agenda una demo",
    },
    {
        "titulo": "¿Creció tu negocio pero no tu logística?",
        "copy_in": "Escala sin límites: integra, automatiza y rastrea en un solo lugar",
        "cta": "Agenda tu demo",
    },
    {
        "titulo": "Reduce el tiempo de tus operaciones logísticas",
        "copy_in": "Integra tus paqueterías favoritas y haz envíos a un clic",
        "cta": "Registrate gratis",
    },
    {
        "titulo": "Automatiza tus envíos y tu facturación",
        "copy_in": "Skydropx Pro: centraliza, cotiza, compara y factura desde un solo lugar",
        "cta": "Agenda una demo",
    },
]

# --- CTAs META (sobre la imagen, SIN emojis, SIN signos de exclamación) ---

META_CTA_EXEMPLARS = [
    "Agenda una demo",
    "Agenda tu demo",
    "Solicita tu demo",
    "Pruébalo gratis",
    "Regístrate gratis",
    "Agendar demo",
    "Activa tu cuenta",
    "Crea tu cuenta",
    "Comienza ahora",
    "Solicita tu prueba gratuita",
]

# --- VIDEO SCRIPT STRUCTURE ---

META_VIDEO_SCRIPT_EXEMPLARS = [
    (
        "Escena 1:\n"
        "[Visual: Persona frente a computadora, frustrada con múltiples pestañas abiertas]\n"
        "Voz en off: ¿Sigues entrando portal por portal para cotizar tus envíos?\n"
        "Crédito: ¿Cuánto tiempo pierdes cotizando?\n\n"
        "Escena 2:\n"
        "[Visual: Pantalla de Skydropx mostrando cotizador con múltiples paqueterías]\n"
        "Voz en off: Con Skydropx, compara precios y tiempos de entrega en segundos.\n"
        "Crédito: +30 paqueterías en un solo lugar\n\n"
        "Escena 3:\n"
        "[Visual: Click en generar guía, animación de guía creada]\n"
        "Voz en off: Genera guías, programa recolecciones y rastrea todo desde un solo panel.\n"
        "Crédito: Cotiza, envía y rastrea\n\n"
        "Escena 4:\n"
        "[Visual: Logo Skydropx + CTA]\n"
        "Voz en off: Skydropx. Tu logística, simplificada.\n"
        "Crédito: Agenda tu demo gratis"
    ),
    (
        "Escena 1:\n"
        "[Visual: Emprendedor empacando pedidos, se acumulan cajas]\n"
        "Voz en off: Tu negocio creció, pero tu logística se quedó atrás.\n"
        "Crédito: ¿Tu operación ya no da abasto?\n\n"
        "Escena 2:\n"
        "[Visual: Dashboard de Skydropx con métricas en tiempo real]\n"
        "Voz en off: Con Skydropx centralizas toda tu operación logística.\n"
        "Crédito: Centraliza envíos desde un solo lugar\n\n"
        "Escena 3:\n"
        "[Visual: Integración con Shopify/WooCommerce, pedidos importándose]\n"
        "Voz en off: Conecta tu tienda, automatiza tus envíos y enfócate en vender.\n"
        "Crédito: Integra tu ecommerce en minutos\n\n"
        "Escena 4:\n"
        "[Visual: Logo Skydropx + CTA]\n"
        "Voz en off: Skydropx. Crece sin límites.\n"
        "Crédito: Solicita tu demo hoy"
    ),
]

# --- META COPY PATTERNS ANALYSIS ---

META_COPY_PATTERNS = """
PATRONES DE COPY REALES DE SKYDROPX META ADS (extraídos de 184 post copies, 183 encabezados, 189 copy de imagen):

=== POST COPY (250-450 chars) ===
ESTRUCTURA OBLIGATORIA:
1. HOOK (linea de apertura) - Statement (72%), Exclamacion (21%), Pregunta (7%)
2. LINEA EN BLANCO
3. PUENTE (frase introductoria): "Con Skydropx puedes:", "Skydropx te permite:", "Skydropx te ofrece:"
4. 3 BULLETS CON EMOJI (beneficios/features concretos)
5. LINEA EN BLANCO
6. REFUERZO/TRANSICION (linea de cierre pre-CTA)
7. CTA FINAL con signos de exclamacion

USO DE EMOJIS EN POST COPY:
- 100% de los post copies usan emojis
- Se usan SOLO como marcadores de bullet points (al inicio de cada linea de feature)
- Emojis mas comunes: ✅ (97x), 📦 (88x), 🚀 (36x), 🚛 (33x), 💻 (27x), 📊 (26x), 💰 (25x)
- NUNCA se ponen emojis sueltos al inicio del post copy ni como decoracion aleatoria
- Los emojis son FUNCIONALES (marcan items), no decorativos

CTAs DE CIERRE MAS USADOS EN POST COPY:
1. "¡Agenda tu demo!" / "¡Agenda tu demo gratis!" (29%)
2. "¡Solicita tu demo!" / "¡Solicita tu prueba gratuita!" (22%)
3. "¡Pruébalo ahora!" / "¡Prueba gratis!" (14%)
4. "¡Comienza hoy!" / "¡Empieza ahora!" (9%)
5. "¡Activa tu cuenta!" (5%)

HOOKS DE APERTURA MAS EFECTIVOS:
- Pregunta pain-point: "¿Todavía creas tus envíos uno por uno?"
- Exclamacion bold: "¡Cámbiate a Skydropx y gana más!"
- Statement directo: "Tu tiempo vale más que los procesos manuales."

=== ENCABEZADO / HEADLINE (max 25 chars) ===
- 63% usan UN emoji al FINAL como decoracion
- Emojis mas comunes al final: 📦, 🚛, 🔝, ⚡, 💰, 💸
- Promedio: 22 chars (sin contar emoji)
- NUNCA emoji al inicio o en medio
- Estructura: frase corta de accion/beneficio + emoji opcional

=== DESCRIPCION (max 30 chars) ===
- 52% usan UN emoji al FINAL
- Emojis mas comunes: 📦, 🚛, 💸, ⚡, 🛡️
- Promedio: 27 chars
- NUNCA emoji al inicio o en medio
- Estructura: frase complementaria + emoji opcional

=== COPY DE LA IMAGEN (texto sobre la imagen/video) ===
- 99.5% NO usan emojis (zona libre de emojis)
- Estructura con etiquetas:
  Título: [headline principal, ~40 chars]
  Copy in: [linea de soporte, ~60 chars] O Característica: [feature callout, ~54 chars]
  CTA: [call to action, ~20 chars]
- Tono mas formal que el post copy, sin signos de exclamacion excesivos

CTAs MAS USADOS EN IMAGEN:
1. "Agenda una demo" (23%)
2. "Agenda tu demo" (19%)
3. "Solicita tu demo" (3%)
4. "Pruébalo gratis" (3%)
5. "Regístrate gratis" (3%)

=== GUION DE VIDEO (4 escenas, 938-1561 chars) ===
ESTRUCTURA POR ESCENA:
  [Visual: descripcion de lo que se ve]
  Voz en off: narración
  Crédito: texto en pantalla

- Escena 1: PROBLEMA/HOOK (pain point del usuario)
- Escena 2: SOLUCION (presentacion de Skydropx)
- Escena 3: FEATURES (funcionalidades concretas)
- Escena 4: CIERRE (logo + CTA)
- SIN emojis en guiones de video
- Arco narrativo: problema → agitacion → solucion → CTA
"""


# =========================================================================
# Helper functions
# =========================================================================

def get_headline_exemplars_for_prompt(max_per_category: int = 5) -> str:
    """Build a formatted string of headline exemplars for the LLM prompt."""
    lines = ["EJEMPLOS REALES DE HEADLINES DE SKYDROPX (referencia de estilo y largo):"]
    for category, headlines in HEADLINE_EXEMPLARS.items():
        label = {
            "action": "Acción/Imperativo",
            "benefit": "Beneficio",
            "brand_first": "Marca primero",
            "question": "Pregunta",
            "promo": "Promo/Urgencia",
            "feature_specific": "Feature específico",
        }.get(category, category)
        lines.append(f"\n  {label}:")
        for h in headlines[:max_per_category]:
            lines.append(f"    ({len(h)} chars) \"{h}\"")
    return "\n".join(lines)


def get_description_exemplars_for_prompt(max_items: int = 10) -> str:
    """Build a formatted string of description exemplars for the LLM prompt."""
    lines = ["EJEMPLOS REALES DE DESCRIPTIONS DE SKYDROPX (referencia de estilo y largo):"]
    for d in DESCRIPTION_EXEMPLARS[:max_items]:
        lines.append(f"  ({len(d)} chars) \"{d}\"")
    return "\n".join(lines)


def get_campaign_exemplars_for_prompt(max_items: int = 5) -> str:
    """Build a formatted string of campaign copy exemplars."""
    lines = ["EJEMPLOS REALES DE COPYS DE CAMPAÑA SKYDROPX:"]
    for c in CAMPAIGN_EXEMPLARS[:max_items]:
        lines.append(f"  Título: {c['titulo']}")
        lines.append(f"  Descripción: {c['descripcion']}")
        lines.append("")
    return "\n".join(lines)


def get_meta_post_copy_exemplars_for_prompt(max_items: int = 5) -> str:
    """Build formatted string of Meta post copy exemplars."""
    lines = ["EJEMPLOS REALES DE POST COPY DE SKYDROPX META ADS:"]
    for pc in META_POST_COPY_EXEMPLARS[:max_items]:
        lines.append(f"\n  ({len(pc)} chars):")
        lines.append(f'  """{pc}"""')
    return "\n".join(lines)


def get_meta_encabezado_exemplars_for_prompt() -> str:
    """Build formatted string of Meta headline exemplars."""
    lines = ["EJEMPLOS REALES DE ENCABEZADOS DE SKYDROPX META ADS (max 25 chars):"]
    lines.append("\n  Con emoji al final (63% de los reales):")
    for h in META_ENCABEZADO_EXEMPLARS["con_emoji"][:6]:
        lines.append(f"    ({len(h)} chars) \"{h}\"")
    lines.append("\n  Sin emoji (37% de los reales):")
    for h in META_ENCABEZADO_EXEMPLARS["sin_emoji"][:5]:
        lines.append(f"    ({len(h)} chars) \"{h}\"")
    return "\n".join(lines)


def get_meta_descripcion_exemplars_for_prompt() -> str:
    """Build formatted string of Meta description exemplars."""
    lines = ["EJEMPLOS REALES DE DESCRIPCIONES DE SKYDROPX META ADS (max 30 chars):"]
    lines.append("\n  Con emoji al final (52% de los reales):")
    for d in META_DESCRIPCION_EXEMPLARS["con_emoji"][:6]:
        lines.append(f"    ({len(d)} chars) \"{d}\"")
    lines.append("\n  Sin emoji (48% de los reales):")
    for d in META_DESCRIPCION_EXEMPLARS["sin_emoji"][:5]:
        lines.append(f"    ({len(d)} chars) \"{d}\"")
    return "\n".join(lines)


def get_meta_copy_imagen_exemplars_for_prompt(max_items: int = 5) -> str:
    """Build formatted string of Meta image copy exemplars."""
    lines = ["EJEMPLOS REALES DE COPY DE IMAGEN DE SKYDROPX META ADS (SIN emojis):"]
    for ci in META_COPY_IMAGEN_EXEMPLARS[:max_items]:
        lines.append(f"\n  Título: {ci['titulo']}")
        lines.append(f"  Copy in: {ci['copy_in']}")
        lines.append(f"  CTA: {ci['cta']}")
    return "\n".join(lines)


def get_meta_video_exemplars_for_prompt(max_items: int = 1) -> str:
    """Build formatted string of Meta video script exemplars."""
    lines = ["EJEMPLO REAL DE GUION DE VIDEO DE SKYDROPX META ADS:"]
    for script in META_VIDEO_SCRIPT_EXEMPLARS[:max_items]:
        lines.append(f"\n{script}")
    return "\n".join(lines)
