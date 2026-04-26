-- ============================================================
-- Skydropx Ad Generator — Supabase Schema
-- Run this ONCE in Supabase SQL Editor (supabase.com > SQL Editor)
-- ============================================================

-- Tables

CREATE TABLE IF NOT EXISTS campaigns (
    id BIGSERIAL PRIMARY KEY,
    canal TEXT NOT NULL,
    formato TEXT NOT NULL,
    objetivo TEXT NOT NULL,
    tier INTEGER NOT NULL,
    pilar TEXT NOT NULL,
    enfoque_narrativo TEXT DEFAULT 'n/a',
    brief TEXT DEFAULT '',
    mensajes_clave JSONB DEFAULT '[]'::jsonb,
    territorios JSONB DEFAULT '[]'::jsonb,
    nota TEXT DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS variants (
    id BIGSERIAL PRIMARY KEY,
    campaign_id BIGINT NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    territorio TEXT DEFAULT '',
    field_name TEXT NOT NULL,
    position INTEGER NOT NULL,
    text_content TEXT NOT NULL,
    char_count INTEGER NOT NULL,
    UNIQUE(campaign_id, territorio, field_name, position)
);

CREATE TABLE IF NOT EXISTS feedback (
    id BIGSERIAL PRIMARY KEY,
    variant_id BIGINT NOT NULL REFERENCES variants(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK(rating IN (-1, 1)),
    comment TEXT DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by TEXT DEFAULT ''
);

-- Indexes

CREATE INDEX IF NOT EXISTS idx_variants_campaign ON variants(campaign_id);
CREATE INDEX IF NOT EXISTS idx_feedback_variant ON feedback(variant_id);
CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback(rating);

-- RLS: allow all access (internal tool, no user auth)

ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all on campaigns" ON campaigns FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on variants" ON variants FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on feedback" ON feedback FOR ALL USING (true) WITH CHECK (true);

-- ============================================================
-- RPC Functions (complex queries used by the learning system)
-- ============================================================

CREATE OR REPLACE FUNCTION get_approved_variants(
    p_formato TEXT,
    p_field_name TEXT,
    p_limit INT DEFAULT 20
)
RETURNS TABLE(text_content TEXT, char_count INT, formato TEXT, tier INT, objetivo TEXT)
LANGUAGE sql STABLE
AS $$
    SELECT sub.text_content, sub.char_count::INT, sub.formato, sub.tier::INT, sub.objetivo
    FROM (
        SELECT DISTINCT ON (v.text_content)
            v.text_content, v.char_count, c.formato, c.tier, c.objetivo, f.created_at
        FROM variants v
        JOIN feedback f ON f.variant_id = v.id
        JOIN campaigns c ON c.id = v.campaign_id
        WHERE f.rating = 1
          AND c.formato = p_formato
          AND v.field_name = p_field_name
        ORDER BY v.text_content, f.created_at DESC
    ) sub
    ORDER BY sub.created_at DESC
    LIMIT p_limit;
$$;


CREATE OR REPLACE FUNCTION get_rejected_patterns(
    p_formato TEXT,
    p_field_name TEXT,
    p_limit INT DEFAULT 10
)
RETURNS TABLE(text_content TEXT, comment TEXT, char_count INT)
LANGUAGE sql STABLE
AS $$
    SELECT v.text_content, f.comment, v.char_count::INT
    FROM variants v
    JOIN feedback f ON f.variant_id = v.id
    JOIN campaigns c ON c.id = v.campaign_id
    WHERE f.rating = -1
      AND f.comment != ''
      AND c.formato = p_formato
      AND v.field_name = p_field_name
    ORDER BY f.created_at DESC
    LIMIT p_limit;
$$;


CREATE OR REPLACE FUNCTION get_campaign_feedback(p_campaign_id BIGINT)
RETURNS TABLE(
    id BIGINT,
    variant_id BIGINT,
    rating INT,
    comment TEXT,
    created_at TIMESTAMPTZ,
    created_by TEXT,
    field_name TEXT,
    "position" INT,
    text_content TEXT,
    territorio TEXT
)
LANGUAGE sql STABLE
AS $$
    SELECT f.id, f.variant_id, f.rating, f.comment, f.created_at, f.created_by,
           v.field_name, v.position::INT, v.text_content, v.territorio
    FROM feedback f
    JOIN variants v ON f.variant_id = v.id
    WHERE v.campaign_id = p_campaign_id
    ORDER BY f.created_at DESC;
$$;
