import time
import threading

import streamlit as st

from utils.prompt_builder import validate_prompt_data, build_optimized_prompt
from services.service_dalle import generate_image_from_text
from services.service_openai_text import generate_pedagogical_content_from_prompt
from services.service_pdf import generate_schema_pdf


TEXT_INPUT_KEYS = [
    "text_to_image_niveau_selectbox",
    "text_to_image_theme_input",
    "text_to_image_language_selectbox",
    "text_to_image_niveau_detail_selectbox",
    "text_to_image_presence_annotations",
    "text_to_image_prompt_text_area",
]


def clear_text_to_image_page():
    keys_to_delete = [
        "last_text_generation",
        "generation_cache",
        "text_to_image_saved_inputs",
        "text_final_prompt_display",
        *TEXT_INPUT_KEYS,
    ]

    for key in keys_to_delete:
        st.session_state.pop(key, None)

    st.rerun()


def save_text_inputs():
    st.session_state["text_to_image_saved_inputs"] = {
        "niveau": st.session_state.get("text_to_image_niveau_selectbox", "Collège"),
        "theme": st.session_state.get("text_to_image_theme_input", ""),
        "language": st.session_state.get("text_to_image_language_selectbox", "Français"),
        "niveau_detail": st.session_state.get("text_to_image_niveau_detail_selectbox", "Simple"),
        "presence_annotations": st.session_state.get("text_to_image_presence_annotations", True),
        "prompt": st.session_state.get("text_to_image_prompt_text_area", ""),
    }


def load_text_inputs():
    saved = st.session_state.get("text_to_image_saved_inputs", {})

    defaults = {
        "text_to_image_niveau_selectbox": saved.get("niveau", "Collège"),
        "text_to_image_theme_input": saved.get("theme", ""),
        "text_to_image_language_selectbox": saved.get("language", "Français"),
        "text_to_image_niveau_detail_selectbox": saved.get("niveau_detail", "Simple"),
        "text_to_image_presence_annotations": saved.get("presence_annotations", True),
        "text_to_image_prompt_text_area": saved.get("prompt", ""),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_prompt_box():
    load_text_inputs()

    st.markdown("### ✍️ Description du schéma")

    niveau = st.selectbox(
        "Niveau scolaire",
        ["Collège", "Lycée"],
        key="text_to_image_niveau_selectbox",
        on_change=save_text_inputs,
    )

    theme = st.text_input(
        "Thème du schéma",
        placeholder="Exemple : appareil respiratoire humain",
        key="text_to_image_theme_input",
        on_change=save_text_inputs,
    )

    language = st.selectbox(
        "Langue",
        ["Français", "Anglais"],
        key="text_to_image_language_selectbox",
        on_change=save_text_inputs,
    )

    niveau_detail = st.selectbox(
        "Niveau de détail",
        ["Simple", "Moyen", "Détaillé"],
        key="text_to_image_niveau_detail_selectbox",
        on_change=save_text_inputs,
    )

    presence_annotations = st.checkbox(
        "Inclure des annotations",
        key="text_to_image_presence_annotations",
        on_change=save_text_inputs,
    )

    prompt = st.text_area(
        "Décrivez le schéma souhaité",
        height=180,
        placeholder="Exemple : schéma pédagogique en couleurs avec annotations...",
        key="text_to_image_prompt_text_area",
        on_change=save_text_inputs,
    )

    data = {
        "niveau": niveau,
        "theme": theme,
        "language": language,
        "niveau_detail": niveau_detail,
        "presence_annotations": presence_annotations,
        "prompt": prompt,
    }

    st.session_state["text_to_image_saved_inputs"] = data.copy()

    return data


def render_text_to_image():
    st.title("📝 Texte vers schéma")

    st.write("""
    Décrivez le schéma souhaité afin de générer
    un support pédagogique adapté.
    """)

    if "generation_cache" not in st.session_state:
        st.session_state["generation_cache"] = {}

    if "last_text_generation" not in st.session_state:
        st.session_state["last_text_generation"] = None

    data = render_prompt_box()

    def render_saved_text_generation(saved, elapsed_time=None):
        optimized_prompt = saved["optimized_prompt"]
        input_data = saved["input_data"]
        image_bytes = saved["bytes"]
        pedagogical_content = saved["pedagogical_content"]

        pdf_bytes = generate_schema_pdf(
            image_bytes=image_bytes,
            input_data=input_data,
            optimized_prompt=optimized_prompt,
            pedagogical_content=pedagogical_content
        )

        col1, col_arrow, col2 = st.columns([5, 1, 5])

        with col1:
            st.markdown("---")
            st.markdown("### 📝 Informations saisies")

            st.write(f"**Niveau :** {input_data['niveau']}")
            st.write(f"**Thème :** {input_data['theme']}")
            st.write(f"**Langue :** {input_data['language']}")
            st.write(f"**Niveau de détail :** {input_data['niveau_detail']}")
            st.write(
                f"**Inclure des annotations :** "
                f"{'Oui' if input_data['presence_annotations'] else 'Non'}"
            )

            st.markdown("---")
            st.markdown("### 📨 Prompt envoyé au modèle DALL·E")

            st.text_area(
                "Prompt final",
                value=optimized_prompt,
                height=500,
                key="text_final_prompt_display",
            )

        with col_arrow:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown(
                """
                <div style="
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    height:600px;
                    font-size:90px;
                    font-weight:bold;
                    color:#4A90E2;
                ">
                    ➜
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown("---")
            st.markdown("### ✅ Image générée")

            st.image(
                image_bytes,
                caption="Schéma généré par DALL·E",
                width="stretch"
            )

            st.success("Image générée avec succès.")

            if elapsed_time is not None:
                st.info(f"⏱️ Temps de génération : {elapsed_time:.1f}s")

            st.caption("🧠 Modèle : DALL·E")
            st.caption("📐 Résolution : 1024x1024")
            st.caption("⚡ Qualité : low")

            st.download_button(
                label="📥 Télécharger l'image",
                data=image_bytes,
                file_name=f"Image générée - {input_data['theme']}.png",
                mime="image/png",
                key="download_text_to_image_png",
            )

            st.download_button(
                label="📄 Télécharger le contenu pédagogique",
                data=pdf_bytes,
                file_name=f"Contenu pédagogique - {input_data['theme']}.pdf",
                mime="application/pdf",
                key="download_text_to_image_pdf",
            )

        if pedagogical_content:
            st.markdown("---")
            st.markdown("### 📚 Contenu pédagogique associé")

            tab1, tab2, tab3, tab4 = st.tabs([
                "📖 Explication",
                "🎯 Objectifs et compétences",
                "🔑 Notions clés",
                "❓ Questions et réponses"
            ])

            with tab1:
                st.markdown("### 📖 Explication détaillée")
                st.write(pedagogical_content.get("explication", ""))

                st.markdown("### 🧒 Résumé simplifié")
                st.info(pedagogical_content.get("resume", ""))

            with tab2:
                st.markdown("### 🎯 Objectifs pédagogiques")
                for objectif in pedagogical_content.get("objectifs_pedagogiques", []):
                    st.write(f"• {objectif}")

                st.markdown("---")
                st.markdown("### 🧩 Compétences visées")
                for competence in pedagogical_content.get("competences_visees", []):
                    st.write(f"• {competence}")

            with tab3:
                st.markdown("### 🔑 Notions clés")
                for notion in pedagogical_content.get("notions_cles", []):
                    st.write(f"• {notion}")

            with tab4:
                st.markdown("### ❓ Questions pédagogiques")

                questions = pedagogical_content.get("questions", [])
                reponses = pedagogical_content.get("reponses", [])

                for i, question in enumerate(questions):
                    st.markdown(f"**Q{i + 1}.** {question}")

                    if i < len(reponses):
                        with st.expander("Voir la réponse attendue"):
                            st.write(reponses[i])

    rendered_result = False
    elapsed = None

    col_generate, col_clear, _ = st.columns([1, 1, 5])

    with col_generate:
        generate_clicked = st.button(
            "Générer le schéma",
            key="generate_text_to_image_button"
        )

    with col_clear:
        clear_clicked = st.button(
            "🧹 Nettoyer",
            key="clear_text_to_image_button"
        )

    if clear_clicked:
        clear_text_to_image_page()

    if generate_clicked:
        save_text_inputs()

        errors = validate_prompt_data(
            theme=data["theme"],
            prompt=data["prompt"]
        )

        if errors:
            for error in errors:
                st.warning(error)

        else:
            optimized_prompt = build_optimized_prompt(data)

            cache_key = (
                f"text::{optimized_prompt}"
                f"::1024x1024::low"
            )

            cached_result = st.session_state["generation_cache"].get(cache_key)

            if cached_result is not None:
                st.session_state["last_text_generation"] = {
                    "optimized_prompt": optimized_prompt,
                    "input_data": data.copy(),
                    "bytes": cached_result["image_bytes"],
                    "pedagogical_content": cached_result["pedagogical_content"],
                }

            else:
                result_data = {"bytes": None, "error": None}
                generation_done = threading.Event()

                def generate_image():
                    try:
                        result_data["bytes"] = generate_image_from_text(
                            optimized_prompt
                        )
                    except Exception as exc:
                        result_data["error"] = str(exc)
                    finally:
                        generation_done.set()

                thread = threading.Thread(target=generate_image)
                thread.start()

                timer_placeholder = st.empty()

                with st.spinner("Génération du schéma..."):
                    start_time = time.perf_counter()

                    while not generation_done.is_set():
                        elapsed = time.perf_counter() - start_time
                        timer_placeholder.info(f"Temps écoulé : {elapsed:.1f}s")
                        time.sleep(0.1)

                elapsed = time.perf_counter() - start_time
                elapsed_ms = int(elapsed * 1000)

                timer_placeholder.success(
                    f"Temps final : {elapsed_ms // 1000}s {elapsed_ms % 1000}ms"
                )

                if result_data["error"]:
                    st.error(
                        f"Erreur lors de la génération : {result_data['error']}"
                    )

                else:
                    image_bytes = result_data["bytes"]

                    with st.spinner("Génération du contenu pédagogique..."):
                        pedagogical_content = (
                            generate_pedagogical_content_from_prompt(
                                optimized_prompt
                            )
                        )

                    st.session_state["generation_cache"][cache_key] = {
                        "image_bytes": image_bytes,
                        "pedagogical_content": pedagogical_content
                    }

                    st.session_state["last_text_generation"] = {
                        "optimized_prompt": optimized_prompt,
                        "input_data": data.copy(),
                        "bytes": image_bytes,
                        "pedagogical_content": pedagogical_content,
                    }

            if st.session_state["last_text_generation"] is not None:
                render_saved_text_generation(
                    st.session_state["last_text_generation"],
                    elapsed_time=elapsed
                )
                rendered_result = True

    if (
        not rendered_result
        and st.session_state["last_text_generation"] is not None
    ):
        render_saved_text_generation(
            st.session_state["last_text_generation"]
        )