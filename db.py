"""SQLite database for campaign history, variants, and feedback."""

import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "skydropx_ads.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            canal TEXT NOT NULL,
            formato TEXT NOT NULL,
            objetivo TEXT NOT NULL,
            tier INTEGER NOT NULL,
            pilar TEXT NOT NULL,
            enfoque_narrativo TEXT DEFAULT 'n/a',
            brief TEXT DEFAULT '',
            mensajes_clave TEXT DEFAULT '[]',
            territorios TEXT DEFAULT '[]',
            nota TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            created_by TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL REFERENCES campaigns(id),
            territorio TEXT DEFAULT '',
            field_name TEXT NOT NULL,
            position INTEGER NOT NULL,
            text_content TEXT NOT NULL,
            char_count INTEGER NOT NULL,
            UNIQUE(campaign_id, territorio, field_name, position)
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            variant_id INTEGER NOT NULL REFERENCES variants(id),
            rating INTEGER NOT NULL CHECK(rating IN (-1, 1)),
            comment TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            created_by TEXT DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_variants_campaign ON variants(campaign_id);
        CREATE INDEX IF NOT EXISTS idx_feedback_variant ON feedback(variant_id);
        CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback(rating);
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

def save_campaign(campaign_dict):
    """Save a campaign config. Returns campaign_id."""
    conn = get_connection()
    cur = conn.execute("""
        INSERT INTO campaigns (canal, formato, objetivo, tier, pilar,
            enfoque_narrativo, brief, mensajes_clave, territorios, nota, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        campaign_dict.get("canal", ""),
        campaign_dict["formato"],
        campaign_dict["objetivo"],
        campaign_dict["tier"],
        campaign_dict.get("pilar", "caracteristicas"),
        campaign_dict.get("enfoque_narrativo", "n/a"),
        campaign_dict.get("brief", ""),
        json.dumps(campaign_dict.get("mensajes_clave", []), ensure_ascii=False),
        json.dumps(campaign_dict.get("territorios", []), ensure_ascii=False),
        campaign_dict.get("nota", ""),
        campaign_dict.get("created_by", ""),
    ))
    campaign_id = cur.lastrowid
    conn.commit()
    conn.close()
    return campaign_id


def get_campaign(campaign_id):
    """Get a single campaign by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return _row_to_campaign(row)


def list_campaigns(limit=50):
    """List recent campaigns."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM campaigns ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [_row_to_campaign(r) for r in rows]


def _row_to_campaign(row):
    d = dict(row)
    d["mensajes_clave"] = json.loads(d["mensajes_clave"])
    d["territorios"] = json.loads(d["territorios"])
    return d


# ---------------------------------------------------------------------------
# Variants
# ---------------------------------------------------------------------------

def save_variants(campaign_id, territorio, ads_dict):
    """Save all generated variants for a campaign/territory.
    ads_dict = {"post_copy": ["v1", "v2", ...], "encabezado": [...], ...}
    Returns list of variant IDs.
    """
    conn = get_connection()
    variant_ids = []
    for field_name, texts in ads_dict.items():
        if not isinstance(texts, list):
            texts = [texts]
        for pos, text in enumerate(texts):
            cur = conn.execute("""
                INSERT OR REPLACE INTO variants
                    (campaign_id, territorio, field_name, position, text_content, char_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (campaign_id, territorio, field_name, pos, text, len(text)))
            variant_ids.append(cur.lastrowid)
    conn.commit()
    conn.close()
    return variant_ids


def get_variants(campaign_id, territorio=""):
    """Get all variants for a campaign/territory as {field: [texts]}."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM variants
        WHERE campaign_id = ? AND territorio = ?
        ORDER BY field_name, position
    """, (campaign_id, territorio)).fetchall()
    conn.close()

    result = {}
    for row in rows:
        field = row["field_name"]
        if field not in result:
            result[field] = []
        result[field].append({
            "id": row["id"],
            "text": row["text_content"],
            "chars": row["char_count"],
            "position": row["position"],
        })
    return result


def get_variant_by_id(variant_id):
    """Get a single variant."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM variants WHERE id = ?", (variant_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_variant_text(variant_id, new_text):
    """Update a variant's text (after regeneration)."""
    conn = get_connection()
    conn.execute("""
        UPDATE variants SET text_content = ?, char_count = ? WHERE id = ?
    """, (new_text, len(new_text), variant_id))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------

def save_feedback(variant_id, rating, comment="", created_by=""):
    """Save feedback for a variant. rating: 1 (like) or -1 (dislike)."""
    conn = get_connection()
    conn.execute("""
        INSERT INTO feedback (variant_id, rating, comment, created_by)
        VALUES (?, ?, ?, ?)
    """, (variant_id, rating, comment, created_by))
    conn.commit()
    conn.close()


def get_feedback_for_variant(variant_id):
    """Get all feedback for a variant."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM feedback WHERE variant_id = ? ORDER BY created_at DESC
    """, (variant_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_feedback_for_campaign(campaign_id):
    """Get all feedback for a campaign's variants."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT f.*, v.field_name, v.position, v.text_content, v.territorio
        FROM feedback f
        JOIN variants v ON f.variant_id = v.id
        WHERE v.campaign_id = ?
        ORDER BY f.created_at DESC
    """, (campaign_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Learning queries
# ---------------------------------------------------------------------------

def get_approved_variants(formato, field_name, limit=20):
    """Get variants that received positive feedback for a specific format/field.
    Returns the most recent approved variants.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT DISTINCT v.text_content, v.char_count, c.formato, c.tier, c.objetivo
        FROM variants v
        JOIN feedback f ON f.variant_id = v.id
        JOIN campaigns c ON c.id = v.campaign_id
        WHERE f.rating = 1
          AND c.formato = ?
          AND v.field_name = ?
        ORDER BY f.created_at DESC
        LIMIT ?
    """, (formato, field_name, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_rejected_patterns(formato, field_name, limit=10):
    """Get variants with negative feedback + comments (rejection reasons).
    These become 'avoid this' instructions.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT v.text_content, f.comment, v.char_count
        FROM variants v
        JOIN feedback f ON f.variant_id = v.id
        JOIN campaigns c ON c.id = v.campaign_id
        WHERE f.rating = -1
          AND f.comment != ''
          AND c.formato = ?
          AND v.field_name = ?
        ORDER BY f.created_at DESC
        LIMIT ?
    """, (formato, field_name, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_feedback_stats():
    """Get overall feedback statistics."""
    conn = get_connection()
    stats = {}
    stats["total_campaigns"] = conn.execute("SELECT COUNT(*) FROM campaigns").fetchone()[0]
    stats["total_variants"] = conn.execute("SELECT COUNT(*) FROM variants").fetchone()[0]
    stats["total_feedback"] = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
    stats["total_approved"] = conn.execute("SELECT COUNT(*) FROM feedback WHERE rating = 1").fetchone()[0]
    stats["total_rejected"] = conn.execute("SELECT COUNT(*) FROM feedback WHERE rating = -1").fetchone()[0]
    conn.close()
    return stats


# Initialize on import
init_db()
