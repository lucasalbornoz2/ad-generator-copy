import os

def _get_secret(key, default=""):
    """Read a secret from Streamlit secrets or environment variables."""
    try:
        import streamlit as _st
        val = _st.secrets.get(key)
        if val:
            return val
    except Exception:
        pass
    return os.environ.get(key, default)


GEMINI_API_KEY = _get_secret("GEMINI_API_KEY")
SUPABASE_URL = _get_secret("SUPABASE_URL")
SUPABASE_KEY = _get_secret("SUPABASE_KEY")
FAL_API_KEY = _get_secret("FAL_API_KEY")

BRAND_BOOK_PDF = os.environ.get(
    "BRAND_BOOK_PDF",
    "/Users/lucasalbornoz/Downloads/Brand book Skydropx/Guía de identidad y estándares marcarios (1).pdf",
)
BRANDBOOK_VISUAL_PDF = os.environ.get(
    "BRANDBOOK_VISUAL_PDF",
    "/Users/lucasalbornoz/Downloads/Brand book Skydropx/Brandbook Skydropx 2025.pdf",
)
EXCEL_PATH = os.environ.get(
    "EXCEL_PATH",
    "/Users/lucasalbornoz/Downloads/Textos de Campaña Google Ads AI _ Skydropx 2026.xlsx",
)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

SHEET_MAP = {
    "skydropx": "Ads Media - Solo Envíos ",
}

BRAND_DISPLAY_NAMES = {
    "skydropx": "Skydropx",
}

# ---------------------------------------------------------------------------
# Canal → Formatos disponibles
# ---------------------------------------------------------------------------

CANAL_FORMATS = {
    "google_ads": ["search_rsa", "pmax"],
    "meta": ["meta_imagen", "meta_video", "meta_carousel"],
}

# ---------------------------------------------------------------------------
# AD_SPECS — Google Ads
# ---------------------------------------------------------------------------

AD_SPECS = {
    "search_rsa": {
        "headlines": {"count": 15, "max_chars": 30},
        "descriptions": {"count": 4, "max_chars": 90},
    },
    "pmax": {
        "short_headlines": {"count": 5, "max_chars": 30},
        "long_headlines": {"count": 5, "max_chars": 90},
        "descriptions": {"count": 5, "max_chars": 90},
        "business_name": {"count": 1, "max_chars": 25},
    },
    # ------------------------------------------------------------------
    # Meta Ads — 6 variantes por campo
    # ------------------------------------------------------------------
    "meta_imagen": {
        "post_copy": {"count": 6, "max_chars": 450},
        "copy_imagen": {"count": 6, "max_chars": 280},
        "encabezado": {"count": 6, "max_chars": 25},
        "descripcion": {"count": 6, "max_chars": 30},
    },
    "meta_video": {
        "post_copy": {"count": 6, "max_chars": 450},
        "guion_video": {"count": 6, "max_chars": 1600},
        "encabezado": {"count": 6, "max_chars": 25},
        "descripcion": {"count": 6, "max_chars": 30},
    },
    "meta_carousel": {
        "post_copy": {"count": 6, "max_chars": 450},
        "card_1_copy": {"count": 6, "max_chars": 280},
        "card_2_copy": {"count": 6, "max_chars": 280},
        "card_3_copy": {"count": 6, "max_chars": 280},
        "encabezado": {"count": 6, "max_chars": 25},
        "descripcion": {"count": 6, "max_chars": 30},
    },
}

# ---------------------------------------------------------------------------
# Prompt helpers
# ---------------------------------------------------------------------------

OBJETIVO_PROMPT = {
    "conversion": (
        "OBJETIVO: CONVERSION. Los copys deben impulsar accion inmediata. "
        "Usa CTAs directos y urgentes: '¡Crea tu cuenta gratis!', '¡Agenda tu demo!', '¡Empieza hoy!'. "
        "Enfocate en beneficios tangibles y eliminar fricciones."
    ),
    "awareness": (
        "OBJETIVO: AWARENESS. Los copys deben posicionar la marca y generar reconocimiento. "
        "Usa CTAs suaves: '¡Conoce Skydropx!', '¡Descubre mas!'. "
        "Enfocate en la propuesta de valor general y personalidad de marca."
    ),
    "consideration": (
        "OBJETIVO: CONSIDERATION. Los copys deben educar y generar interes. "
        "Usa CTAs que inviten a explorar: '¡Compara opciones!', '¡Conoce los beneficios!'. "
        "Enfocate en diferenciadores y comparativas con la competencia."
    ),
}

ENFOQUE_NARRATIVO_PROMPT = {
    "plataforma": (
        "ENFOQUE NARRATIVO: PLATAFORMA. Muestra la herramienta en accion. "
        "Usa verbos como 'cotiza', 'rastrea', 'integra', 'automatiza'. "
        "Describe funcionalidades concretas: panel, cotizador, dashboard, guias."
    ),
    "personaje": (
        "ENFOQUE NARRATIVO: PERSONAJE. Habla desde la perspectiva del usuario. "
        "Usa frases como 'Tu negocio merece...', 'Cuando tu operacion crece...'. "
        "Conecta emocionalmente con los pain points del dia a dia logistico."
    ),
    "plataforma+personaje": (
        "ENFOQUE NARRATIVO: PLATAFORMA + PERSONAJE. Combina funcionalidades concretas "
        "con la perspectiva emocional del usuario. Alterna entre mostrar la herramienta "
        "y hablar de como impacta al negocio del usuario."
    ),
    "n/a": "",
}


# ---------------------------------------------------------------------------
# Image generation formats
# ---------------------------------------------------------------------------

IMAGE_FORMATS = {
    "feed":      {"aspect_ratio": "1:1",  "width": 1080, "height": 1080},
    "stories":   {"aspect_ratio": "9:16", "width": 1080, "height": 1920},
    "landscape": {"aspect_ratio": "16:9", "width": 1200, "height": 628},
}


def is_meta_format(formato):
    """Check if a format belongs to Meta."""
    return formato.startswith("meta_")
