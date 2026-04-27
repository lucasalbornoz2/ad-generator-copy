"""Supabase database for campaign history, variants, and feedback."""

from supabase import create_client

from config import SUPABASE_URL, SUPABASE_KEY

_client = None


def _get_client():
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL y SUPABASE_KEY deben estar configurados. "
                "Agregalos en Streamlit Secrets o como variables de entorno."
            )
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

def save_campaign(campaign_dict):
    """Save a campaign config. Returns campaign_id."""
    client = _get_client()
    data = {
        "canal": campaign_dict.get("canal", ""),
        "formato": campaign_dict["formato"],
        "objetivo": campaign_dict["objetivo"],
        "tier": campaign_dict["tier"],
        "pilar": campaign_dict.get("pilar", "caracteristicas"),
        "enfoque_narrativo": campaign_dict.get("enfoque_narrativo", "per-territorio"),
        "brief": campaign_dict.get("brief", ""),
        "mensajes_clave": campaign_dict.get("mensajes_clave", []),
        "territorios": campaign_dict.get("territorios", []),
        "nota": campaign_dict.get("nota", ""),
        "created_by": campaign_dict.get("created_by", ""),
    }
    result = client.table("campaigns").insert(data).execute()
    return result.data[0]["id"]


def get_campaign(campaign_id):
    """Get a single campaign by ID."""
    client = _get_client()
    result = client.table("campaigns").select("*").eq("id", campaign_id).execute()
    return result.data[0] if result.data else None


def list_campaigns(limit=50):
    """List recent campaigns."""
    client = _get_client()
    result = (
        client.table("campaigns")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data


# ---------------------------------------------------------------------------
# Variants
# ---------------------------------------------------------------------------

def save_variants(campaign_id, territorio, ads_dict):
    """Save all generated variants for a campaign/territory.

    Uses upsert with ON CONFLICT to preserve variant IDs
    (and their linked feedback records) when regenerating.
    """
    client = _get_client()
    variant_ids = []
    for field_name, texts in ads_dict.items():
        if not isinstance(texts, list):
            texts = [texts]
        for pos, text in enumerate(texts):
            data = {
                "campaign_id": campaign_id,
                "territorio": territorio,
                "field_name": field_name,
                "position": pos,
                "text_content": text,
                "char_count": len(text),
            }
            result = (
                client.table("variants")
                .upsert(data, on_conflict="campaign_id,territorio,field_name,position")
                .execute()
            )
            variant_ids.append(result.data[0]["id"])
    return variant_ids


def get_variants(campaign_id, territorio=""):
    """Get all variants for a campaign/territory as {field: [{id, text, ...}]}."""
    client = _get_client()
    result = (
        client.table("variants")
        .select("*")
        .eq("campaign_id", campaign_id)
        .eq("territorio", territorio)
        .order("field_name")
        .order("position")
        .execute()
    )
    grouped = {}
    for row in result.data:
        field = row["field_name"]
        if field not in grouped:
            grouped[field] = []
        grouped[field].append({
            "id": row["id"],
            "text": row["text_content"],
            "chars": row["char_count"],
            "position": row["position"],
        })
    return grouped


def get_variant_by_id(variant_id):
    """Get a single variant."""
    client = _get_client()
    result = client.table("variants").select("*").eq("id", variant_id).execute()
    return result.data[0] if result.data else None


def update_variant_text(variant_id, new_text):
    """Update a variant's text (after regeneration)."""
    client = _get_client()
    (
        client.table("variants")
        .update({"text_content": new_text, "char_count": len(new_text)})
        .eq("id", variant_id)
        .execute()
    )


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------

def save_feedback(variant_id, rating, comment="", created_by=""):
    """Save feedback for a variant. rating: 1 (like) or -1 (dislike)."""
    client = _get_client()
    client.table("feedback").insert({
        "variant_id": variant_id,
        "rating": rating,
        "comment": comment,
        "created_by": created_by,
    }).execute()


def get_feedback_for_variant(variant_id):
    """Get all feedback for a variant."""
    client = _get_client()
    result = (
        client.table("feedback")
        .select("*")
        .eq("variant_id", variant_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


def get_feedback_for_campaign(campaign_id):
    """Get all feedback for a campaign's variants (via RPC join)."""
    client = _get_client()
    result = client.rpc(
        "get_campaign_feedback", {"p_campaign_id": campaign_id}
    ).execute()
    return result.data


# ---------------------------------------------------------------------------
# Learning queries
# ---------------------------------------------------------------------------

def get_approved_variants(formato, field_name, limit=20):
    """Get approved variants via RPC (joins feedback + variants + campaigns)."""
    client = _get_client()
    result = client.rpc("get_approved_variants", {
        "p_formato": formato,
        "p_field_name": field_name,
        "p_limit": limit,
    }).execute()
    return result.data


def get_rejected_patterns(formato, field_name, limit=10):
    """Get rejected patterns via RPC (variants with negative feedback + comments)."""
    client = _get_client()
    result = client.rpc("get_rejected_patterns", {
        "p_formato": formato,
        "p_field_name": field_name,
        "p_limit": limit,
    }).execute()
    return result.data


# ---------------------------------------------------------------------------
# Generated Images
# ---------------------------------------------------------------------------

def save_image(variant_id, format_name, aspect_ratio, image_url, prompt_used=""):
    """Save a generated image. Upserts by variant_id + format_name."""
    client = _get_client()
    data = {
        "variant_id": variant_id,
        "format_name": format_name,
        "aspect_ratio": aspect_ratio,
        "image_url": image_url,
        "prompt_used": prompt_used,
    }
    client.table("generated_images").upsert(
        data, on_conflict="variant_id,format_name"
    ).execute()


def get_images_for_variant(variant_id):
    """Get all generated images for a variant."""
    client = _get_client()
    result = (
        client.table("generated_images")
        .select("*")
        .eq("variant_id", variant_id)
        .order("format_name")
        .execute()
    )
    return result.data


def get_images_for_campaign(campaign_id):
    """Get all generated images for a campaign (via variant join)."""
    client = _get_client()
    result = (
        client.table("generated_images")
        .select("*, variants!inner(campaign_id, territorio, field_name, position)")
        .eq("variants.campaign_id", campaign_id)
        .execute()
    )
    return result.data


def get_feedback_stats():
    """Get overall feedback statistics."""
    client = _get_client()
    campaigns = client.table("campaigns").select("id", count="exact").execute()
    variants_r = client.table("variants").select("id", count="exact").execute()
    all_fb = client.table("feedback").select("id", count="exact").execute()
    approved = (
        client.table("feedback").select("id", count="exact").eq("rating", 1).execute()
    )
    rejected = (
        client.table("feedback").select("id", count="exact").eq("rating", -1).execute()
    )
    return {
        "total_campaigns": campaigns.count or 0,
        "total_variants": variants_r.count or 0,
        "total_feedback": all_fb.count or 0,
        "total_approved": approved.count or 0,
        "total_rejected": rejected.count or 0,
    }
