"""Dynamic learning system: builds prompt sections from team feedback."""

from db import get_approved_variants, get_rejected_patterns, get_feedback_stats
from config import is_meta_format

# Minimum approved variants before using them as exemplars
MIN_APPROVED_FOR_LEARNING = 5


def get_learning_prompt_section(formato, fields=None):
    """Build a prompt section from historical feedback.

    Returns a string to inject into the generation prompt, or empty string
    if not enough feedback data exists yet.

    Args:
        formato: ad format (e.g. 'meta_imagen', 'search_rsa')
        fields: list of field names to query. If None, uses defaults per format.
    """
    if fields is None:
        fields = _default_fields(formato)

    stats = get_feedback_stats()
    if stats["total_approved"] < MIN_APPROVED_FOR_LEARNING:
        return ""

    sections = []
    sections.append("=== APRENDIZAJE DEL EQUIPO ===")
    sections.append(
        f"El equipo ha evaluado {stats['total_feedback']} variantes "
        f"({stats['total_approved']} aprobadas, {stats['total_rejected']} rechazadas)."
    )
    sections.append("")

    # Approved exemplars
    approved_section = _build_approved_section(formato, fields)
    if approved_section:
        sections.append(approved_section)

    # Rejection patterns
    rejected_section = _build_rejected_section(formato, fields)
    if rejected_section:
        sections.append(rejected_section)

    if len(sections) <= 3:
        return ""

    return "\n".join(sections)


def _build_approved_section(formato, fields):
    """Build the approved exemplars section."""
    lines = ["COPYS APROBADOS POR EL EQUIPO (imita estos estilos):"]
    found_any = False

    for field in fields:
        approved = get_approved_variants(formato, field, limit=8)
        if not approved:
            continue
        found_any = True
        label = _field_label(field)
        lines.append(f"\n  {label}:")
        for item in approved:
            lines.append(f"    ({item['char_count']} chars) \"{item['text_content']}\"")

    if not found_any:
        return ""
    return "\n".join(lines)


def _build_rejected_section(formato, fields):
    """Build the rejection patterns section."""
    lines = ["PATRONES RECHAZADOS POR EL EQUIPO (evitar estos):"]
    found_any = False

    for field in fields:
        rejected = get_rejected_patterns(formato, field, limit=5)
        if not rejected:
            continue
        found_any = True
        label = _field_label(field)
        lines.append(f"\n  {label} - Evitar:")
        for item in rejected:
            reason = item["comment"]
            text_preview = item["text_content"][:50]
            lines.append(f"    - \"{text_preview}...\" → Razon: {reason}")

    if not found_any:
        return ""
    lines.append("")
    return "\n".join(lines)


def build_regen_prompt_addition(variant_text, feedback_comment):
    """Build additional prompt instructions when regenerating a specific variant.

    Args:
        variant_text: the rejected variant text
        feedback_comment: the team's feedback on why it was rejected
    """
    lines = [
        "=== REGENERACION CON FEEDBACK ===",
        "El equipo rechazo esta variante:",
        f'  "{variant_text}"',
    ]
    if feedback_comment:
        lines.append(f"Razon del rechazo: {feedback_comment}")
    lines.extend([
        "",
        "Genera una NUEVA variante que corrija este problema.",
        "Mantén el mismo formato y limites de caracteres.",
        "",
    ])
    return "\n".join(lines)


def _default_fields(formato):
    """Return default field names to query per format."""
    if formato == "search_rsa":
        return ["headlines", "descriptions"]
    elif formato == "pmax":
        return ["short_headlines", "long_headlines", "descriptions"]
    elif formato == "meta_imagen":
        return ["post_copy", "copy_imagen", "encabezado", "descripcion"]
    elif formato == "meta_video":
        return ["post_copy", "guion_video", "encabezado", "descripcion"]
    elif formato == "meta_carousel":
        return ["post_copy", "card_1_copy", "card_2_copy", "card_3_copy", "encabezado", "descripcion"]
    return []


def _field_label(field):
    """Human-readable label for a field name."""
    labels = {
        "headlines": "Headlines",
        "descriptions": "Descripciones",
        "short_headlines": "Headlines cortos",
        "long_headlines": "Headlines largos",
        "post_copy": "Post Copy",
        "copy_imagen": "Copy de Imagen",
        "encabezado": "Encabezado",
        "descripcion": "Descripción",
        "guion_video": "Guión de Video",
        "card_1_copy": "Card 1",
        "card_2_copy": "Card 2",
        "card_3_copy": "Card 3",
        "business_name": "Business Name",
    }
    return labels.get(field, field.replace("_", " ").title())
