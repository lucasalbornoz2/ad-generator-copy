"""Parses brand book content into a style guide for ad generation."""


# ---------------------------------------------------------------------------
# Visual identity — colors, typography, and style from the Skydropx brandbook
# ---------------------------------------------------------------------------

VISUAL_IDENTITY = {
    # --- Color palette (extracted from 300+ approved ads) ---
    "primary_color": "#6B46C1",          # Deep purple/violet — dominant brand color
    "secondary_color": "#00D9A3",        # Bright cyan/turquoise — accents & CTAs
    "accent_magenta": "#FF4757",         # Magenta/pink — emphasis, discount badges
    "gradient_start": "#6B46C1",         # Purple gradient start
    "gradient_end": "#FF6B9D",           # Pink gradient end
    "background_dark": "#0A1E3F",        # Dark navy — enterprise tier backgrounds
    "background_light": "#F5F5FA",       # Light backgrounds for product focus
    "text_primary": "#FFFFFF",           # White text on colored backgrounds (95%+ of ads)
    "text_dark": "#1A1A2E",              # Dark text on light backgrounds
    "cta_color": "#00D9A3",              # Cyan/turquoise CTA buttons
    "cta_alt_color": "#8B5CF6",          # Purple CTA buttons (enterprise)
    "neon_accent": "#FFB800",            # Orange/gold neon for discounts
    # --- Typography ---
    "font_primary": "Montserrat Bold",   # Clean modern sans-serif
    "font_weight_headline": "Extra Bold",
    "font_weight_body": "Regular",
    # --- Visual style ---
    "style": "Modern gradient + 3D isometric hybrid, tech-forward, vibrant",
    "dominant_visual_elements": [
        "3D isometric cardboard boxes (primary symbol, 70%+ of ads)",
        "Purple-to-pink gradient backgrounds",
        "Floating particles and confetti (purple, pink, gold)",
        "Neon glow effects on text and objects",
        "Dashboard/UI mockups showing the platform",
        "Delivery vans and trucks (purple/pink colored)",
        "Rounded cyan/turquoise CTA pill buttons with cursor icon",
        "Laptops and smartphones showing Skydropx interface",
    ],
    "composition_patterns": [
        "Logo top-left or top-center (small, ~40-60px)",
        "Main headline center-aligned, bold white text, 2-3 lines",
        "Central visual/illustration (30-40% of width)",
        "CTA button at bottom (rounded pill, cyan or purple)",
        "Key benefit words highlighted in cyan color",
        "Floating icons around central image",
    ],
    "enterprise_style": {
        "palette": "Darker, sophisticated purple with dark overlays",
        "imagery": "Team collaborating, manager at computer, warehouse",
        "copy_tone": "Feature-rich, B2B vocabulary, sports metaphors",
        "cta_tone": "Cotiza, Descubre, Centraliza, Evoluciona",
    },
    "avoid_visual": [
        "Flat solid color backgrounds (always use gradients)",
        "Generic stock photography without brand treatment",
        "Cold corporate aesthetic without color/energy",
        "Cluttered compositions without clear hierarchy",
        "Real human faces (use abstract/conceptual instead for AI generation)",
        "Left-aligned headlines (always center or right)",
    ],
}


def build_image_style_prompt(tier):
    """Build visual style context for image prompt generation based on 300+ approved ads."""
    vi = VISUAL_IDENTITY
    tier_data = STYLE_GUIDE["tiers"].get(tier, STYLE_GUIDE["tiers"][2])
    is_enterprise = (tier == 1)

    lines = [
        "[BRAND VISUAL IDENTITY — Skydropx (from 300+ approved creatives)]",
        f"Overall Style: {vi['style']}",
        "",
        "[COLOR PALETTE]",
        f"Primary: {vi['primary_color']} (deep purple/violet — dominant brand color)",
        f"Secondary: {vi['secondary_color']} (bright cyan/turquoise — accents & CTAs)",
        f"Accent: {vi['accent_magenta']} (magenta/pink — emphasis)",
        f"Gradient: {vi['gradient_start']} purple → {vi['gradient_end']} pink (most common background)",
        f"Text: {vi['text_primary']} white on colored backgrounds",
        f"CTA Button: {vi['cta_color']} cyan rounded pill shape",
        f"Neon Accent: {vi['neon_accent']} (orange/gold for promotions)",
        "",
        "[TYPOGRAPHY]",
        f"Font: {vi['font_primary']} (clean modern sans-serif)",
        f"Headline: {vi['font_weight_headline']}, white, center-aligned, 2-3 lines max",
        "Body: Regular weight, white or light gray, short punchy sentences",
        "Key benefit words highlighted in cyan (#00D9A3)",
        "",
        "[DOMINANT VISUAL ELEMENTS]",
    ]
    for elem in vi["dominant_visual_elements"]:
        lines.append(f"- {elem}")

    lines += [
        "",
        "[COMPOSITION RULES]",
    ]
    for pattern in vi["composition_patterns"]:
        lines.append(f"- {pattern}")

    if is_enterprise:
        ent = vi["enterprise_style"]
        lines += [
            "",
            "[ENTERPRISE TIER SPECIFICS]",
            f"Palette: {ent['palette']}",
            f"Imagery: {ent['imagery']}",
            f"Copy Tone: {ent['copy_tone']}",
            f"CTA Tone: {ent['cta_tone']}",
        ]

    lines += [
        "",
        f"[TARGET AUDIENCE — Tier {tier}: {tier_data['name']}]",
        f"{tier_data['description']}",
        f"Tone: {tier_data['tone']}",
        "",
        "[AVOID — CRITICAL]",
    ]
    for item in vi["avoid_visual"]:
        lines.append(f"- {item}")

    return "\n".join(lines)


STYLE_GUIDE = {
    "brand_positioning": "Ayudarte a crecer es nuestro origen y nuestro destino",
    "slogan": "Sea cual sea tu origen, llegamos contigo a tu destino.",
    "taglines": [
        "Gestiona tus envios de forma integral con nuestra tecnologia.",
        "Simplificamos la gestion de tus envios para que puedas enfocarte en tu negocio.",
    ],
    "what_is": (
        "Skydropx es una plataforma de gestion logistica que ayuda a reducir "
        "tiempo, costos y centralizar envios en un mismo sitio. Ofrece "
        "funcionalidades que permiten automatizar procesos y brindar el mejor "
        "servicio al cliente."
    ),
    "countries": ["Mexico", "Colombia", "Brasil"],
    "tone_do": ["Amistoso", "Claro", "Divertido", "Casual", "Respetuoso", "Informado"],
    "tone_dont": ["Apatico", "Serio", "Evadir", "Irreverente", "Anticuado", "Redundante"],
    "voice_attributes": {
        "Formal": "No pierde la forma correcta de hablar. Objetivo: Respetar.",
        "Amigable": "Su forma de expresarse busca que cualquier persona pueda entenderlo. Objetivo: Guiar.",
        "Cercana": "Es una relacion entre dos entidades que se nutren mutuamente, son aliados. Objetivo: Empoderar.",
        "Resolutiva": "Busca dar una solucion, no da vueltas ni es burocratico, juega el rol de aliado. Objetivo: Educar.",
        "Confiable": "Brinda una sensacion de confianza, de comprension. Objetivo: Guiar.",
    },
    "brand_values": {
        "Empatia": "Escuchamos para entender. Nos interesamos genuinamente por los negocios de nuestros clientes.",
        "Creatividad": "El cielo es el limite. Encontramos formas diferentes y eficientes para hacer las cosas.",
        "Experiencia": "La practica hace al maestro. Somos expertos en lo que hacemos y seguimos perfeccionando.",
    },
    "rational_benefits": [
        "Integracion a tu tienda online de manera facil y rapida para automatizar procesos",
        "Seguridad y proteccion en todo el proceso de envio y entrega",
        "Monitoreo constante del envio y entrega",
        "Software en continuo desarrollo y soporte",
        "Informacion util para la toma de decisiones en tu negocio",
    ],
    "emotional_benefits": [
        "Te liberamos de las tareas operativas logisticas para mejorar tus estrategias de venta",
        "Ten el tiempo para centrarte en tus ventas sin perder el control de la logistica",
        "Certeza en todo momento de que todas las operaciones y movimientos estan bajo control",
        "Tranquilidad de que solucionaremos todo para no quitarte el sueno",
        "Te ayudamos a hacer crecer tu negocio, somos un partner de tu rentabilidad",
    ],
    "brand_personality": (
        "Skydropx es un lider innovador, explorador, empatico. "
        "Aporta soluciones a traves de la creatividad, la innovacion y la tecnologia. "
        "Siempre esta en la busqueda de nuevos horizontes, expandiendo sus limites "
        "para el beneficio de todos."
    ),
    "spelling_rules": [
        "Skydropx se escribe con la S en alta inicial siempre; las demas letras van en bajas.",
        "Nunca escribir SKYDROPX todo en mayusculas en copys.",
    ],
    "copy_guidelines": [
        "Mantenerlo simple: faciles de entender rapidamente.",
        "Destacar los beneficios del tema a tratar en la campana.",
        "Incluir llamados a la accion.",
        "Mantener coherencia visual con la marca.",
    ],
    "tiers": {
        1: {
            "name": "Grandes ecommerce",
            "description": (
                "Empleado/a de 35-45 anos, empresa mediana a grande, "
                "8 anos en el mercado, equipo de 7 personas. "
                "Usa Amazon, MercadoLibre, Shopify, WooCommerce."
            ),
            "pillars": [
                "Automatizacion y tecnologia (integraciones)",
                "Atencion al cliente personalizada (KAMs)",
                "Control y Precision",
            ],
            "key_messages": [
                "Encontraras la herramienta necesaria para optimizar y automatizar tus procesos logisticos.",
                "Contaras con un equipo de asesores de cuenta que te brindaran un servicio personalizado.",
                "Administra tus envios desde una sola plataforma incluso si ya tienes negociaciones directas con paqueterias.",
            ],
            "tone": "Mostrar como nuestra plataforma impacta en sus KPIs, respaldar con datos numericos.",
        },
        2: {
            "name": "Ecommerce medianos",
            "description": (
                "Propietario/a de pequena empresa, 4 anos de antiguedad, "
                "equipo de 5 personas. Usa redes sociales, marketplaces "
                "y plataformas de ecommerce."
            ),
            "pillars": [
                "Agilidad en la creacion de envios",
                "Diversidad de paqueterias locales",
                "Servicio de rastreo de envios",
            ],
            "key_messages": [
                "Simplifica tus envios y ahorra tiempo con las funciones de nuestra plataforma.",
                "Compara y elige: amplia variedad de paqueterias locales para tus necesidades y presupuesto.",
                "Controla tus envios en todo momento con nuestro servicio de rastreo.",
            ],
            "tone": "Salta al siguiente nivel, crecer, mas canales de venta.",
        },
        3: {
            "name": "Emprendedor digital",
            "description": (
                "Emprendedor en crecimiento, negocio a tiempo parcial, "
                "equipo de hasta 3 personas, 2 anos en el mercado. "
                "Vende por Instagram y WhatsApp."
            ),
            "pillars": [
                "Acompanamiento y asesoria",
                "Soluciones escalables",
                "Velocidad",
            ],
            "key_messages": [
                "Ofrecemos soluciones de envio escalables para mejorar la eficiencia logistica de tu negocio, sin importar su tamano.",
            ],
            "tone": "Lenguaje cercano y empatico.",
        },
    },
}

PILAR_CONTENT = {
    "skydropx": {
        "caracteristicas": {
            "specs": (
                "Anuncios de texto que destacan las caracteristicas de la plataforma "
                "Skydropx para gestion logistica en Mexico. Finalizar descripciones con CTA."
            ),
            "features": [
                "Plataforma de gestion logistica todo en uno",
                "Integracion facil con tiendas online y marketplaces",
                "Multiples paqueterias en una sola plataforma",
                "Cotizacion y comparacion de tarifas al instante",
                "Rastreo de envios en tiempo real",
                "Automatizacion de procesos logisticos",
                "Interfaz intuitiva y facil de usar",
                "Atencion al cliente por correo y chat",
            ],
        },
        "beneficios": {
            "specs": (
                "Anuncios de texto para destacar los beneficios clave que Skydropx "
                "ofrece a los usuarios. Finalizar descripciones con CTA."
            ),
            "features": [
                "Ahorro significativo en costos de envio",
                "Liberamos de tareas operativas logisticas",
                "Tiempo para centrarte en tus ventas",
                "Certeza y control de todas las operaciones",
                "Tranquilidad de que todo esta bajo control",
                "Te ayudamos a hacer crecer tu negocio",
                "Soporte personalizado para resolver dudas",
                "Optimizacion de logistica y tiempos de entrega",
            ],
        },
        "marca": {
            "specs": (
                "Anuncios de texto enfocados en posicionar la marca Skydropx, "
                "destacando su propuesta de valor y personalidad. "
                "Finalizar descripciones con CTA."
            ),
            "features": [
                "Ayudarte a crecer es nuestro origen y nuestro destino",
                "Plataforma lider en gestion logistica",
                "Presencia en Mexico, Colombia y Brasil",
                "Software en continuo desarrollo",
            ],
        },
    },
}


def build_style_guide_prompt(tier: int, marca: str, pilar: str) -> str:
    """Build a style guide prompt string for the LLM."""
    sg = STYLE_GUIDE
    tier_data = sg["tiers"].get(tier, sg["tiers"][2])
    pilar_data = PILAR_CONTENT.get(marca, {}).get(pilar, {})

    lines = [
        "=== GUIA DE ESTILO SKYDROPX PARA GENERACION DE ADS ===",
        "",
        f"Brand Positioning: {sg['brand_positioning']}",
        f"Slogan: {sg['slogan']}",
        f"Que es: {sg['what_is']}",
        "",
        "--- TONO ---",
        f"SI usar: {', '.join(sg['tone_do'])}",
        f"NO usar: {', '.join(sg['tone_dont'])}",
        "",
        "--- VOZ ---",
    ]
    for attr, desc in sg["voice_attributes"].items():
        lines.append(f"  {attr}: {desc}")

    lines += [
        "",
        "--- VALORES ---",
    ]
    for val, desc in sg["brand_values"].items():
        lines.append(f"  {val}: {desc}")

    lines += [
        "",
        "--- BENEFICIOS RACIONALES ---",
    ]
    for b in sg["rational_benefits"]:
        lines.append(f"  - {b}")

    lines += [
        "",
        "--- BENEFICIOS EMOCIONALES ---",
    ]
    for b in sg["emotional_benefits"]:
        lines.append(f"  - {b}")

    lines += [
        "",
        f"--- TIER {tier}: {tier_data['name']} ---",
        f"Descripcion: {tier_data['description']}",
        f"Pilares: {', '.join(tier_data['pillars'])}",
        f"Tono especifico: {tier_data['tone']}",
        "Mensajes clave:",
    ]
    for msg in tier_data["key_messages"]:
        lines.append(f"  - {msg}")

    if pilar_data:
        lines += [
            "",
            f"--- PILAR: {pilar.upper()} ---",
            f"Specs: {pilar_data.get('specs', '')}",
        ]
        if pilar_data.get("features"):
            lines.append("Caracteristicas/beneficios a incluir:")
            for f in pilar_data["features"]:
                lines.append(f"  - {f}")

    lines += [
        "",
        "--- REGLAS DE ORTOGRAFIA ---",
    ]
    for rule in sg["spelling_rules"]:
        lines.append(f"  - {rule}")

    lines += [
        "",
        "--- LINEAMIENTOS DE COPY ---",
    ]
    for g in sg["copy_guidelines"]:
        lines.append(f"  - {g}")

    return "\n".join(lines)
