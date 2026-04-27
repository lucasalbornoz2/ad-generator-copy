"""Image generation for Meta Ads using fal.ai GPT Image 2 + Gemini prompt."""

import os

import fal_client
import google.generativeai as genai

from config import FAL_API_KEY, IMAGE_FORMATS, OBJETIVO_PROMPT
from brand_parser import build_image_style_prompt


# ---------------------------------------------------------------------------
# Image size mapping for GPT Image 2
# ---------------------------------------------------------------------------

_SIZE_MAP = {
    "1:1":  "square_hd",       # 1024x1024
    "9:16": "portrait_4_3",    # 768x1024
    "16:9": "landscape_4_3",   # 1024x768
}


# ---------------------------------------------------------------------------
# fal.ai — GPT Image 2 (renders text with 99%+ accuracy)
# ---------------------------------------------------------------------------

def generate_image(prompt, aspect_ratio="1:1"):
    """Generate an image via fal.ai GPT Image 2."""
    if not FAL_API_KEY:
        raise RuntimeError(
            "FAL_API_KEY no configurada. "
            "Agregala en Streamlit Secrets o como variable de entorno."
        )
    os.environ["FAL_KEY"] = FAL_API_KEY

    image_size = _SIZE_MAP.get(aspect_ratio, "square_hd")

    result = fal_client.subscribe("openai/gpt-image-2", arguments={
        "prompt": prompt,
        "num_images": 1,
        "image_size": image_size,
        "quality": "medium",
    })
    return result["images"][0]["url"]


# ---------------------------------------------------------------------------
# Prompt builder — Gemini creates a complete ad prompt WITH exact copy text
# ---------------------------------------------------------------------------

_VISUAL_PROMPT_SYSTEM = """\
You are a senior art director creating Meta ad images for Skydropx, a logistics
management platform. You create prompts for GPT Image 2 which renders text
with 99%+ accuracy, so you MUST include the EXACT ad copy text in Spanish.

REFERENCE STYLE (from 300+ approved Skydropx ads analyzed):

VISUAL STYLE:
- Clean gradient backgrounds: navy-to-purple, lavender-to-pink, or teal-to-blue
- Polished 3D rendered cardboard shipping boxes with realistic tan color and shadows
- 3D icons: location pins, shield icons, circular arrows, shipping labels
- Clean laptop/phone mockups showing abstract dashboard interfaces
- Smooth, minimal composition with lots of negative space
- Professional ad design aesthetic

COLOR PALETTE (strict — these are the real Skydropx brand colors):
- Backgrounds: dark navy (#0A1E3F), deep purple (#4B2F8F), soft lavender, teal-blue
- Accent: bright teal/cyan (#00D9A3)
- CTA buttons: navy, purple (#6B46C1), bright green (#00D964), or teal — rounded pill shape
- Text: bold white on dark backgrounds, navy on light backgrounds
- Cardboard boxes: tan/beige (#D4A574) with realistic shading
- Skydropx logo: teal/cyan colored geometric mark

COMPOSITION LAYOUT (critical — based on real approved ads):
- Top area: small teal Skydropx logo (top-left or top-center)
- Upper section: large bold headline text in white (2-3 lines max)
- Center: ONE main visual element (3D boxes, laptop with UI, shipping icons)
- Lower section: optional subtext in smaller white font
- Bottom: rounded CTA button (pill shape) with contrasting color
- LOTS of negative space — clean, scannable, mobile-first

TEXT RENDERING RULES:
- Include the EXACT Spanish text provided — do not translate or modify
- Headline: large, bold, white, centered or left-aligned
- Subtext: medium, regular weight, white or light gray
- CTA button text: bold, white, inside a colored rounded pill button
- Text must be crisp and readable

ABSOLUTELY AVOID:
- Drones, rockets, spaceships, fantasy vehicles
- Neon city backgrounds, cyberpunk aesthetics
- Complex busy scenes with too many elements
- Human faces or hands (AI renders these poorly)
- Random decorative confetti or particle overload
- Generic stock-photo feel
- Any element that doesn't serve the ad message

Return ONLY the English prompt with embedded Spanish text. No explanations.
"""


def _build_prompt_with_gemini(variant_copy, campaign, aspect_ratio):
    """Use Gemini to build a complete ad image prompt with exact copy text."""
    import re

    style_context = build_image_style_prompt(campaign.get("tier", 2))
    objetivo = campaign.get("objetivo", "conversion")
    objetivo_desc = OBJETIVO_PROMPT.get(objetivo, "")

    # Parse copy_imagen for Titulo / Copy in / CTA
    copy_imagen = variant_copy.get("copy_imagen", "")
    titulo = ""
    copy_in = ""
    cta_text = ""

    if copy_imagen:
        for line in copy_imagen.split("\n"):
            line_stripped = line.strip()
            lower = line_stripped.lower()
            if lower.startswith("título:") or lower.startswith("titulo:"):
                titulo = re.sub(r'^t[ií]tulo:\s*', '', line_stripped, flags=re.IGNORECASE)
            elif lower.startswith("copy in:") or lower.startswith("copy_in:"):
                copy_in = re.sub(r'^copy[_ ]in:\s*', '', line_stripped, flags=re.IGNORECASE)
            elif lower.startswith("cta:"):
                cta_text = re.sub(r'^cta:\s*', '', line_stripped, flags=re.IGNORECASE)

    # Fallbacks
    if not titulo:
        titulo = variant_copy.get("encabezado", "") or "Skydropx"
    if not cta_text:
        cta_text = "Agenda una demo"

    post_copy = variant_copy.get("post_copy", "")

    tier = campaign.get("tier", 2)
    if tier == 1:
        bg_style = "dark navy-to-deep-purple gradient, sophisticated enterprise feel"
    elif tier == 2:
        bg_style = "smooth teal-to-blue or lavender-to-pink gradient, professional modern"
    else:
        bg_style = "bright friendly lavender or soft blue gradient, approachable clean"

    user_prompt = f"""Create a complete ad image prompt for a Skydropx Meta ad.
The image must include the EXACT Spanish text below — GPT Image 2 renders text perfectly.

EXACT TEXT TO RENDER ON THE IMAGE (in Spanish, do NOT translate):
- HEADLINE (large, bold, white, top area): "{titulo}"
- SUBTEXT (medium, white, below headline): "{copy_in}"
- CTA BUTTON TEXT (bold, white, inside rounded pill button at bottom): "{cta_text}"

VISUAL SCENE:
- Background: {bg_style}
- Central visual element: polished 3D rendered cardboard shipping boxes with realistic
  tan color and shadows, OR a clean laptop/phone showing a logistics dashboard UI
- Small teal Skydropx logo at top-left corner
- CTA button: rounded pill shape, teal (#00D9A3) or purple (#6B46C1) background
- Aspect ratio: {aspect_ratio}
- LOTS of negative space — professional ad layout

CAMPAIGN CONTEXT (use to inform the visual mood, NOT the text):
- Brief: {campaign.get('brief', 'N/A')[:200]}
- {objetivo_desc}

{style_context}

CRITICAL RULES:
1. The headline "{titulo}" must appear EXACTLY as written in Spanish
2. The CTA "{cta_text}" must appear EXACTLY as written inside a button
3. NO drones, rockets, neon cities, cyberpunk, human faces, or hands
4. Keep composition clean and minimal with one central visual element
5. The image must look like a professional Meta ad, not generic AI art

Generate ONE cohesive English paragraph that describes the complete ad image
including the exact Spanish text placement."""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        [_VISUAL_PROMPT_SYSTEM, user_prompt],
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=500,
        ),
    )
    return response.text.strip()


def build_image_prompt(campaign, variant_copy, aspect_ratio="1:1"):
    """Build a complete ad prompt from campaign data and variant copy."""
    return _build_prompt_with_gemini(variant_copy, campaign, aspect_ratio)


# ---------------------------------------------------------------------------
# Batch generation
# ---------------------------------------------------------------------------

def generate_variant_images(campaign, variant_copy, formats=None):
    """Generate images in multiple formats for a single variant.

    Pipeline: Gemini prompt → GPT Image 2 (complete ad with text)
    Returns dict: {format_name: {url, prompt}}
    """
    if formats is None:
        formats = ["feed"]

    results = {}
    for fmt_name in formats:
        fmt = IMAGE_FORMATS[fmt_name]
        prompt = build_image_prompt(campaign, variant_copy, fmt["aspect_ratio"])
        url = generate_image(prompt, fmt["aspect_ratio"])
        results[fmt_name] = {"url": url, "prompt": prompt}
    return results
