"""Validates generated ad copies against brand rules and character limits."""

import re
from difflib import SequenceMatcher
from config import AD_SPECS


FORBIDDEN_TONE_WORDS = [
    "lamentablemente", "desafortunadamente", "problema", "complicado",
    "dificil", "imposible", "error", "fallo", "malo",
]

BRAND_SPELLING = {
    "skydropx": "Skydropx",
    "SKYDROPX": "Skydropx",
    "solo envios": "Solo Envios",
    "solo envíos": "Solo Envíos",
    "envios internacionales": "Envíos Internacionales",
    "envíos internacionales": "Envíos Internacionales",
}


def validate_char_limit(text: str, max_chars: int) -> dict:
    actual = len(text)
    return {
        "text": text,
        "chars": actual,
        "max": max_chars,
        "valid": actual <= max_chars,
        "overflow": max(0, actual - max_chars),
    }


def validate_tone(text: str) -> list[str]:
    warnings = []
    lower = text.lower()
    for word in FORBIDDEN_TONE_WORDS:
        if re.search(rf'\b{re.escape(word)}\b', lower):
            warnings.append(f"Tono prohibido detectado: '{word}' en '{text[:50]}...'")
    return warnings


def validate_spelling(text: str) -> list[str]:
    warnings = []
    for wrong, correct in BRAND_SPELLING.items():
        if wrong in text and correct not in text:
            warnings.append(f"Ortografia: '{wrong}' deberia ser '{correct}'")
    return warnings


def check_duplicates(texts: list[str], threshold: float = 0.85) -> list[str]:
    warnings = []
    for i, a in enumerate(texts):
        for j, b in enumerate(texts):
            if i >= j:
                continue
            ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
            if ratio >= threshold:
                warnings.append(
                    f"Copys muy similares ({ratio:.0%}): [{i+1}] '{a[:40]}...' vs [{j+1}] '{b[:40]}...'"
                )
    return warnings


def validate_ad_set(ad_type: str, ads: dict) -> dict:
    """Validate a complete set of generated ads.

    Args:
        ad_type: 'search_rsa', 'pmax', or 'meta'
        ads: dict with field names as keys and lists of strings as values

    Returns:
        dict with validation results per field
    """
    specs = AD_SPECS.get(ad_type, {})
    results = {"valid": True, "fields": {}, "warnings": []}

    for field_name, field_spec in specs.items():
        max_chars = field_spec["max_chars"]
        expected_count = field_spec["count"]
        texts = ads.get(field_name, [])

        field_results = []
        for text in texts:
            char_result = validate_char_limit(text, max_chars)
            tone_warnings = validate_tone(text)
            spell_warnings = validate_spelling(text)

            if not char_result["valid"]:
                results["valid"] = False
            results["warnings"].extend(tone_warnings)
            results["warnings"].extend(spell_warnings)

            field_results.append({
                **char_result,
                "tone_warnings": tone_warnings,
                "spell_warnings": spell_warnings,
            })

        dup_warnings = check_duplicates(texts)
        results["warnings"].extend(dup_warnings)

        if len(texts) < expected_count:
            results["warnings"].append(
                f"{field_name}: se generaron {len(texts)}/{expected_count} copys"
            )

        results["fields"][field_name] = field_results

    return results


def print_validation_report(results: dict):
    """Print a human-readable validation report."""
    status = "PASS" if results["valid"] else "FAIL"
    print(f"\n{'='*60}")
    print(f"  VALIDACION: {status}")
    print(f"{'='*60}")

    for field_name, field_results in results["fields"].items():
        print(f"\n  {field_name.upper()}:")
        for i, r in enumerate(field_results, 1):
            icon = "OK" if r["valid"] else "XX"
            print(f"    [{icon}] {i}. ({r['chars']}/{r['max']} chars) {r['text']}")
            if not r["valid"]:
                print(f"         ^ Excede por {r['overflow']} caracteres")

    if results["warnings"]:
        print(f"\n  ADVERTENCIAS ({len(results['warnings'])}):")
        for w in results["warnings"]:
            print(f"    ! {w}")

    print(f"\n{'='*60}\n")
