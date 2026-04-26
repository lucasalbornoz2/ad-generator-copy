"""Streamlit app for Skydropx Ad Generator."""

import json
import streamlit as st

from config import (
    AD_SPECS, CANAL_FORMATS, is_meta_format,
)
from brand_parser import STYLE_GUIDE
from generate_ads import (
    build_generation_prompt, normalize_ads, export_to_excel,
    generate_with_gemini, configure_gemini,
)
from validator import validate_ad_set
from learning import get_learning_prompt_section, build_regen_prompt_addition
from db import (
    save_campaign, save_variants, save_feedback,
    get_variants, get_feedback_for_campaign,
    list_campaigns, get_feedback_stats,
    get_approved_variants, update_variant_text,
)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Skydropx Ad Generator",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------

if "generated" not in st.session_state:
    st.session_state.generated = False
if "ads" not in st.session_state:
    st.session_state.ads = None
if "campaign" not in st.session_state:
    st.session_state.campaign = None
if "campaign_id" not in st.session_state:
    st.session_state.campaign_id = None
if "validation" not in st.session_state:
    st.session_state.validation = None

configure_gemini()


# =========================================================================
# Helper functions (defined BEFORE main flow)
# =========================================================================

def _meta_field_order(formato):
    """Return (field_name, label, max_chars) tuples for Meta formats."""
    if formato == "meta_imagen":
        return [
            ("post_copy", "Post Copy", 450),
            ("copy_imagen", "Copy de la Imagen", 280),
            ("encabezado", "Encabezado", 25),
            ("descripcion", "Descripcion", 30),
        ]
    elif formato == "meta_video":
        return [
            ("post_copy", "Post Copy", 450),
            ("guion_video", "Guion de Video", 1600),
            ("encabezado", "Encabezado", 25),
            ("descripcion", "Descripcion", 30),
        ]
    elif formato == "meta_carousel":
        return [
            ("post_copy", "Post Copy", 450),
            ("card_1_copy", "Card 1", 280),
            ("card_2_copy", "Card 2", 280),
            ("card_3_copy", "Card 3", 280),
            ("encabezado", "Encabezado", 25),
            ("descripcion", "Descripcion", 30),
        ]
    return []


def _regenerate_variant(campaign, territorio, v_idx, current_texts, comment, field_order):
    """Regenerate a single variant using feedback."""
    formato = campaign["formato"]
    campaign_id = st.session_state.campaign_id

    prompt = build_generation_prompt(campaign, territorio)
    main_text = current_texts.get(field_order[0][0], "")
    regen_addition = build_regen_prompt_addition(main_text, comment)
    prompt = prompt + "\n\n" + regen_addition
    prompt += f"\nREGENERA SOLO LA VARIANTE {v_idx + 1} (posicion {v_idx} en cada array del JSON)."
    prompt += "\nManten las otras 5 variantes pero MEJORA esta especifica."

    try:
        raw_ads = generate_with_gemini(prompt, formato)
        new_ads = normalize_ads(raw_ads, formato)

        terr_key = territorio or formato
        current_ads = st.session_state.ads[terr_key][0]
        for field_name, _, _ in field_order:
            new_texts = new_ads.get(field_name, [])
            if v_idx < len(new_texts) and field_name in current_ads:
                current_ads[field_name][v_idx] = new_texts[v_idx]

        new_validation = validate_ad_set(formato, current_ads)
        st.session_state.ads[terr_key] = (current_ads, new_validation)

        db_variants = get_variants(campaign_id, territorio)
        for field_name, _, _ in field_order:
            vdata = db_variants.get(field_name, [])
            if v_idx < len(vdata):
                new_text = current_ads[field_name][v_idx]
                update_variant_text(vdata[v_idx]["id"], new_text)

        st.success(f"V{v_idx + 1} regenerada con feedback.")
        st.rerun()

    except Exception as e:
        st.error(f"Error regenerando: {e}")


def _feedback_controls(db_variants, field_order, v_idx, campaign_id, territorio, formato):
    """Feedback buttons and comment for a Meta variant."""
    st.markdown("---")
    col1, col2, col3 = st.columns([0.15, 0.15, 0.7])

    main_field = field_order[0][0]
    variant_data = db_variants.get(main_field, [])
    vid = variant_data[v_idx]["id"] if v_idx < len(variant_data) else None

    if vid:
        with col1:
            if st.button("👍 Aprobar", key=f"like_v{v_idx}_{territorio}"):
                for field_name, _, _ in field_order:
                    vdata = db_variants.get(field_name, [])
                    if v_idx < len(vdata):
                        save_feedback(vdata[v_idx]["id"], 1)
                st.toast(f"V{v_idx + 1} aprobada")
                st.rerun()

        with col2:
            if st.button("👎 Rechazar", key=f"dislike_v{v_idx}_{territorio}"):
                comment = st.session_state.get(f"comment_v{v_idx}_{territorio}", "")
                for field_name, _, _ in field_order:
                    vdata = db_variants.get(field_name, [])
                    if v_idx < len(vdata):
                        save_feedback(vdata[v_idx]["id"], -1, comment)
                st.toast(f"V{v_idx + 1} rechazada")
                st.rerun()

    with col3:
        st.text_input(
            "Comentario",
            key=f"comment_v{v_idx}_{territorio}",
            placeholder="Feedback: 'el CTA no pega', 'muy generico'...",
            label_visibility="collapsed",
        )

    if vid:
        if st.button(f"🔄 Regenerar V{v_idx + 1}", key=f"regen_v{v_idx}_{territorio}"):
            comment = st.session_state.get(f"comment_v{v_idx}_{territorio}", "")
            campaign = st.session_state.campaign
            current_texts = {}
            for field_name, _, _ in field_order:
                texts = st.session_state.ads[territorio or formato][0].get(field_name, [])
                if v_idx < len(texts):
                    current_texts[field_name] = texts[v_idx]
            with st.spinner(f"Regenerando V{v_idx + 1}..."):
                _regenerate_variant(campaign, territorio, v_idx, current_texts, comment, field_order)


def _display_meta_variants(ads, formato, campaign_id, territorio):
    """Display Meta ad variants with feedback controls."""
    db_variants = get_variants(campaign_id, territorio)
    field_order = _meta_field_order(formato)

    for v_idx in range(6):
        with st.expander(f"Variante V{v_idx + 1}", expanded=(v_idx == 0)):
            for field_name, field_label, max_chars in field_order:
                texts = ads.get(field_name, [])
                text = texts[v_idx] if v_idx < len(texts) else ""
                char_count = len(text)
                is_ok = char_count <= max_chars

                status = f"({char_count}/{max_chars})" if max_chars <= 450 else f"({char_count} chars)"
                color = "green" if is_ok else "red"
                st.markdown(
                    f"**{field_label}** <span style='color:{color}'>{status}</span>",
                    unsafe_allow_html=True,
                )

                if field_name in ("post_copy", "guion_video") or field_name.startswith("card_"):
                    st.text_area(
                        label=field_label,
                        value=text,
                        height=150 if field_name == "guion_video" else 120,
                        key=f"{territorio}_{field_name}_{v_idx}",
                        label_visibility="collapsed",
                        disabled=True,
                    )
                else:
                    st.code(text)

            _feedback_controls(db_variants, field_order, v_idx, campaign_id, territorio, formato)


def _display_google_ads_variants(ads, formato, campaign_id, territorio):
    """Display Google Ads results with feedback controls."""
    db_variants = get_variants(campaign_id, territorio)
    specs = AD_SPECS.get(formato, {})

    for field_name, field_spec in specs.items():
        max_chars = field_spec["max_chars"]
        texts = ads.get(field_name, [])
        label = field_name.replace("_", " ").title()

        st.subheader(label)
        for i, text in enumerate(texts):
            char_count = len(text)
            is_ok = char_count <= max_chars
            color = "green" if is_ok else "red"

            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                st.markdown(
                    f"`{i+1}.` {text} "
                    f"<span style='color:{color}'>({char_count}/{max_chars})</span>",
                    unsafe_allow_html=True,
                )

            variant_data = db_variants.get(field_name, [])
            if i < len(variant_data):
                vid = variant_data[i]["id"]
                with col2:
                    if st.button("👍", key=f"like_{territorio}_{field_name}_{i}"):
                        save_feedback(vid, 1)
                        st.toast(f"Aprobado: {label} #{i+1}")
                with col3:
                    if st.button("👎", key=f"dislike_{territorio}_{field_name}_{i}"):
                        comment = st.session_state.get(f"comment_{territorio}_{field_name}_{i}", "")
                        save_feedback(vid, -1, comment)
                        st.toast(f"Rechazado: {label} #{i+1}")

            st.text_input(
                "Comentario",
                key=f"comment_{territorio}_{field_name}_{i}",
                placeholder="Feedback opcional...",
                label_visibility="collapsed",
            )


def _show_history_page():
    """Display campaign history."""
    st.header("Historial de campanas")

    campaigns = list_campaigns(limit=30)
    if not campaigns:
        st.info("No hay campanas generadas todavia.")
        return

    for c in campaigns:
        canal_label = "Google Ads" if c["canal"] == "google_ads" else "Meta"
        formato_label = c["formato"].replace("_", " ").upper()
        with st.expander(
            f"#{c['id']} | {canal_label} / {formato_label} | "
            f"Tier {c['tier']} | {c['objetivo']} | {c['created_at']}"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Pilar:** {c['pilar']}")
                st.markdown(f"**Enfoque:** {c['enfoque_narrativo']}")
                if c.get("brief"):
                    st.markdown(f"**Brief:** {c['brief'][:150]}...")
            with col2:
                if c.get("mensajes_clave"):
                    st.markdown("**Mensajes clave:**")
                    for msg in c["mensajes_clave"]:
                        st.markdown(f"- {msg}")
                if c.get("territorios"):
                    st.markdown(f"**Territorios:** {', '.join(c['territorios'])}")

            feedback = get_feedback_for_campaign(c["id"])
            if feedback:
                approved = sum(1 for f in feedback if f["rating"] == 1)
                rejected = sum(1 for f in feedback if f["rating"] == -1)
                st.markdown(f"**Feedback:** 👍 {approved} aprobadas | 👎 {rejected} rechazadas")

                comments = [f for f in feedback if f.get("comment")]
                if comments:
                    st.markdown("**Comentarios del equipo:**")
                    for f in comments[:5]:
                        icon = "👍" if f["rating"] == 1 else "👎"
                        st.markdown(f"  {icon} _{f['comment']}_")


def _show_learning_page():
    """Display learning/feedback stats."""
    st.header("Aprendizaje del equipo")

    stats = get_feedback_stats()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Campanas", stats["total_campaigns"])
    col2.metric("Variantes", stats["total_variants"])
    col3.metric("Aprobadas", stats["total_approved"])
    col4.metric("Rechazadas", stats["total_rejected"])

    st.markdown("---")

    if stats["total_approved"] < 5:
        st.info(
            f"Se necesitan al menos 5 variantes aprobadas para activar el aprendizaje. "
            f"Actualmente: {stats['total_approved']}. Sigue generando y dando feedback."
        )
    else:
        st.success(
            "El aprendizaje esta ACTIVO. Los copys aprobados por el equipo se usan "
            "como ejemplos para mejorar futuras generaciones."
        )

    for formato_key, formato_label in [
        ("search_rsa", "Google Ads - Search RSA"),
        ("pmax", "Google Ads - Performance Max"),
        ("meta_imagen", "Meta - Imagen"),
        ("meta_video", "Meta - Video"),
        ("meta_carousel", "Meta - Carousel"),
    ]:
        specs = AD_SPECS.get(formato_key, {})
        has_data = False
        for field_name in specs.keys():
            approved = get_approved_variants(formato_key, field_name, limit=5)
            if approved:
                has_data = True
                break

        if has_data:
            with st.expander(f"{formato_label}"):
                for field_name in specs.keys():
                    approved = get_approved_variants(formato_key, field_name, limit=5)
                    if approved:
                        label = field_name.replace("_", " ").title()
                        st.markdown(f"**{label}** — {len(approved)} ejemplos aprobados:")
                        for item in approved:
                            text = item["text_content"]
                            preview = f"{text[:80]}..." if len(text) > 80 else text
                            st.markdown(f"  ✅ _{preview}_")

                learning_text = get_learning_prompt_section(formato_key)
                if learning_text:
                    st.markdown("---")
                    st.markdown("**Lo que ve el modelo (preview del prompt):**")
                    preview = f"{learning_text[:500]}..." if len(learning_text) > 500 else learning_text
                    st.code(preview)


# =========================================================================
# MAIN FLOW
# =========================================================================

# ---------------------------------------------------------------------------
# Sidebar — Campaign config
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("Skydropx Ad Generator")
    st.markdown("---")

    page = st.radio(
        "Navegacion",
        ["Generar", "Historial", "Aprendizaje"],
        label_visibility="collapsed",
    )

    if page == "Generar":
        st.header("Configurar campana")

        canal = st.selectbox(
            "1. Canal",
            options=["google_ads", "meta"],
            format_func=lambda x: "Google Ads" if x == "google_ads" else "Meta Ads",
            help="Plataforma donde se publicaran los anuncios.",
        )

        formato_options = CANAL_FORMATS[canal]
        formato_labels = {
            "search_rsa": "Search RSA (15 titulares + 4 desc)",
            "pmax": "Performance Max (5 short + 5 long + 5 desc)",
            "meta_imagen": "Imagen - Feed/Stories (6 variantes)",
            "meta_video": "Video (6 variantes con guion)",
            "meta_carousel": "Carousel (6 variantes, 3 cards)",
        }
        formato = st.selectbox(
            "2. Formato",
            options=formato_options,
            format_func=lambda x: formato_labels.get(x, x),
        )

        objetivo = st.selectbox(
            "3. Objetivo",
            options=["conversion", "awareness", "consideration"],
            format_func=lambda x: x.capitalize(),
            help="Conversion: CTAs directos. Awareness: CTAs suaves. Consideration: CTAs exploratorios.",
        )

        tier = st.selectbox(
            "4. Tier / Audiencia",
            options=[1, 2, 3],
            index=1,
            format_func=lambda x: f"Tier {x} - {STYLE_GUIDE['tiers'][x]['name']}",
        )

        brief = st.text_area(
            "5. Brief de campana",
            placeholder="Describe el concepto, que comunicar, que evitar, contexto...",
            height=100,
        )

        mensajes_raw = st.text_area(
            "6. Mensajes clave (uno por linea)",
            placeholder="Centraliza tus envios\nReduce tu carga operativa\nDecide con informacion clara",
            height=80,
        )
        mensajes_clave = [m.strip() for m in mensajes_raw.split("\n") if m.strip()]

        territorios_raw = st.text_input(
            "7. Territorios creativos (separados por coma)",
            placeholder="Decidir todo el tiempo, Crecer es emocionante",
        )
        territorios = [t.strip() for t in territorios_raw.split(",") if t.strip()]

        enfoque = st.selectbox(
            "8. Enfoque narrativo",
            options=["plataforma", "personaje", "plataforma+personaje", "n/a"],
            index=3,
            format_func=lambda x: {
                "plataforma": "Plataforma (funcionalidades)",
                "personaje": "Personaje (perspectiva usuario)",
                "plataforma+personaje": "Plataforma + Personaje",
                "n/a": "Sin enfoque especifico",
            }.get(x, x),
        )

        pilar = st.selectbox(
            "9. Pilar de comunicacion",
            options=["caracteristicas", "beneficios", "marca"],
            format_func=lambda x: x.capitalize(),
        )

        nota = st.text_input(
            "10. Nota adicional",
            placeholder="Evitar cliches del Dia de las Madres",
        )

        st.markdown("---")

        generate_btn = st.button(
            "Generar copys",
            type="primary",
            use_container_width=True,
        )

# ---------------------------------------------------------------------------
# Main area — page routing
# ---------------------------------------------------------------------------

if page == "Generar":
    st.header("Generador de copys")

    # Handle generation
    if generate_btn:
        campaign = {
            "canal": canal,
            "formato": formato,
            "objetivo": objetivo,
            "tier": tier,
            "pilar": pilar,
            "brief": brief,
            "mensajes_clave": mensajes_clave,
            "territorios": territorios,
            "enfoque_narrativo": enfoque,
            "nota": nota,
        }

        st.session_state.campaign = campaign
        st.session_state.generated = False
        st.session_state.ads = None

        campaign_id = save_campaign(campaign)
        st.session_state.campaign_id = campaign_id

        terrs = territorios if territorios else [""]
        all_results = {}

        for territorio in terrs:
            label = territorio if territorio else formato
            with st.spinner(f"Generando: {label}..."):
                best_ads = None
                best_validation = None

                for attempt in range(3):
                    try:
                        prompt = build_generation_prompt(campaign, territorio)
                        raw_ads = generate_with_gemini(prompt, formato)
                        ads = normalize_ads(raw_ads, formato)
                        validation = validate_ad_set(formato, ads)

                        if validation["valid"]:
                            best_ads = ads
                            best_validation = validation
                            break

                        if best_ads is None or len(validation["warnings"]) < len(best_validation["warnings"]):
                            best_ads = ads
                            best_validation = validation

                    except json.JSONDecodeError:
                        st.warning(f"Intento {attempt + 1}: Error parseando respuesta. Reintentando...")
                    except Exception as e:
                        st.warning(f"Intento {attempt + 1}: {e}")

                if best_ads:
                    key = territorio or formato
                    all_results[key] = (best_ads, best_validation)
                    save_variants(campaign_id, territorio, best_ads)

        if all_results:
            st.session_state.ads = all_results
            st.session_state.validation = {k: v[1] for k, v in all_results.items()}
            st.session_state.generated = True
            st.success(f"Generados {len(all_results)} sets de copys.")
        else:
            st.error("No se pudieron generar copys. Intenta de nuevo.")

    # Show results
    if st.session_state.generated and st.session_state.ads:
        campaign = st.session_state.campaign
        campaign_id = st.session_state.campaign_id
        formato = campaign["formato"]

        territory_keys = list(st.session_state.ads.keys())
        if len(territory_keys) > 1:
            tabs = st.tabs(territory_keys)
        else:
            tabs = [st.container()]

        for tab, terr_key in zip(tabs, territory_keys):
            with tab:
                ads, validation = st.session_state.ads[terr_key]
                territorio = terr_key if terr_key != formato else ""

                if validation and validation["valid"]:
                    st.success("Validacion: PASS")
                elif validation:
                    st.warning(f"Validacion: {len(validation['warnings'])} advertencias")

                if is_meta_format(formato):
                    _display_meta_variants(ads, formato, campaign_id, territorio)
                else:
                    _display_google_ads_variants(ads, formato, campaign_id, territorio)

                if validation and validation.get("warnings"):
                    with st.expander(f"Advertencias ({len(validation['warnings'])})"):
                        for w in validation["warnings"]:
                            st.warning(w)

        # Download
        st.markdown("---")
        valid_results = {k: v for k, v in st.session_state.ads.items() if v[0]}
        if valid_results:
            filepath = export_to_excel(valid_results, campaign)
            with open(filepath, "rb") as f:
                st.download_button(
                    label="Descargar Excel",
                    data=f.read(),
                    file_name=filepath.split("/")[-1],
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                )

elif page == "Historial":
    _show_history_page()

elif page == "Aprendizaje":
    _show_learning_page()
