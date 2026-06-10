import hashlib
import tempfile
import time
import threading
import io
from pathlib import Path

import streamlit as st
from PIL import Image

from services.service_dalle import edit_image_from_image
from services.service_openai_text import generate_pedagogical_content_from_image
from services.service_pdf import generate_schema_pdf
from utils.prompt_builder import validate_theme


DEFAULT_IMAGE_INSTRUCTION = (
    "Transforme ce schéma en un schéma pédagogique clair, "
    "scientifiquement correct et propre."
)

IMAGE_INPUT_KEYS = [
    "image_to_image_uploader",
    "image_to_image_theme_input",
    "image_to_image_instruction_text_area",
]


def resize_image_for_display(image, max_width, max_height):
    width, height = image.size

    if width > max_width or height > max_height:
        ratio = min(max_width / width, max_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size, Image.LANCZOS)

    return image


def clear_image_to_image_page():
    keys_to_delete = [
        "last_image_generation",
        "generation_cache",
        "image_to_image_saved_inputs",
        "image_to_image_uploaded_bytes",
        "image_to_image_uploaded_name",
        *IMAGE_INPUT_KEYS,
    ]

    for key in keys_to_delete:
        st.session_state.pop(key, None)

    st.rerun()


def save_image_inputs():
    if "image_to_image_saved_inputs" not in st.session_state:
        st.session_state["image_to_image_saved_inputs"] = {}

    st.session_state["image_to_image_saved_inputs"] = {
        "theme": st.session_state.get("image_to_image_theme_input", ""),
        "instruction": st.session_state.get(
            "image_to_image_instruction_text_area",
            DEFAULT_IMAGE_INSTRUCTION
        ),
    }


def load_image_inputs():
    saved = st.session_state.get("image_to_image_saved_inputs", {})

    defaults = {
        "image_to_image_theme_input": saved.get("theme", ""),
        "image_to_image_instruction_text_area": saved.get(
            "instruction",
            DEFAULT_IMAGE_INSTRUCTION
        ),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_saved_uploaded_image():
    if "image_to_image_uploaded_bytes" not in st.session_state:
        return None

    try:
        return Image.open(
            io.BytesIO(st.session_state["image_to_image_uploaded_bytes"])
        )
    except Exception:
        return None


def render_image_uploader():
    load_image_inputs()

    st.markdown("### 📸 Importation de l'image")

    uploaded_file = st.file_uploader(
        "Importez une image",
        type=["png", "jpg", "jpeg"],
        help="Formats acceptés : PNG, JPG, JPEG",
        key="image_to_image_uploader",
    )

    original_image = None
    file_bytes = None

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()

        st.session_state["image_to_image_uploaded_bytes"] = file_bytes
        st.session_state["image_to_image_uploaded_name"] = uploaded_file.name

        original_image = Image.open(io.BytesIO(file_bytes))

    elif "image_to_image_uploaded_bytes" in st.session_state:
        file_bytes = st.session_state["image_to_image_uploaded_bytes"]
        original_image = get_saved_uploaded_image()

    if original_image is not None:
        display_image = resize_image_for_display(
            original_image,
            max_width=600,
            max_height=400
        )

        st.image(
            display_image,
            caption="Image importée",
            width=display_image.width
        )

    theme = st.text_input(
        "Thème du schéma",
        placeholder="Exemple : appareil respiratoire humain",
        key="image_to_image_theme_input",
        on_change=save_image_inputs,
    )

    instruction = st.text_area(
        "Instruction de transformation",
        height=130,
        key="image_to_image_instruction_text_area",
        on_change=save_image_inputs,
    )

    data = {
        "theme": theme,
        "instruction": instruction,
        "file_bytes": file_bytes,
        "uploaded_name": st.session_state.get("image_to_image_uploaded_name"),
        "original_image": original_image,
    }

    st.session_state["image_to_image_saved_inputs"] = {
        "theme": theme,
        "instruction": instruction,
    }

    return data


def render_image_to_image():
    st.title("🖼️ Image vers schéma")

    st.write(
        """
        Importez un schéma dessiné à la main
        afin de le transformer en schéma numérique.
        """
    )

    if "generation_cache" not in st.session_state:
        st.session_state["generation_cache"] = {}

    if "last_image_generation" not in st.session_state:
        st.session_state["last_image_generation"] = None

    data = render_image_uploader()

    file_bytes = data["file_bytes"]
    image = data["original_image"]
    theme = data["theme"]
    instruction = data["instruction"]
    uploaded_name = data["uploaded_name"]

    def render_saved_image_generation(saved, elapsed_time=None):
        original_image = saved["original_image"]
        generated_bytes = saved["bytes"]
        instruction_text = saved["instruction"]
        theme_value = saved.get("theme", "Schéma numérisé")
        pedagogical_content = saved.get("pedagogical_content", {})

        pdf_bytes = generate_schema_pdf(
            image_bytes=generated_bytes,
            input_data={
                "theme": theme_value,
                "niveau": "N/A",
                "language": "N/A",
                "niveau_detail": instruction_text,
            },
            optimized_prompt=instruction_text,
            pedagogical_content=pedagogical_content
        )

        col1, col_arrow, col2 = st.columns([5, 1, 5])

        with col1:
            st.markdown("---")
            st.markdown("### 📥 Schéma importé")
            st.image(
                original_image,
                caption="Schéma manuscrit",
                width="stretch"
            )

            st.markdown("---")
            st.markdown("### Instruction envoyée")
            st.write(f"**Thème :** {theme_value}")
            st.write(f"**Instruction de transformation :** {instruction_text}")

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
            st.markdown("### ✅ Image numérisée")
            st.image(
                generated_bytes,
                caption="Schéma numérisé par DALL·E",
                width="stretch"
            )

            st.success("Image numérisée avec succès.")

            if elapsed_time is not None:
                st.info(f"⏱️ Temps de numérisation : {elapsed_time:.1f}s")

            st.caption("🧠 Modèle : DALL·E")
            st.caption("📐 Résolution : 1024x1024")
            st.caption("⚡ Qualité : low")

            st.download_button(
                label="📥 Télécharger l'image",
                data=generated_bytes,
                file_name=f"Image numérisée - {theme_value}.png",
                mime="image/png",
                key="download_image_to_image_png",
            )

            st.download_button(
                label="📄 Télécharger le contenu pédagogique",
                data=pdf_bytes,
                file_name=f"Contenu pédagogique - {theme_value}.pdf",
                mime="application/pdf",
                key="download_image_to_image_pdf",
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

    col_edit, col_clear, _ = st.columns([1, 1, 5])

    with col_edit:
        edit_clicked = st.button(
            "Numériser le schéma",
            key="image_numériser_button"
        )

    with col_clear:
        clear_clicked = st.button(
            "🧹 Nettoyer",
            key="image_clear_button"
        )

    if clear_clicked:
        clear_image_to_image_page()

    if edit_clicked:
        save_image_inputs()

        theme_error = validate_theme(theme)

        if file_bytes is None or image is None:
            st.warning("Veuillez importer une image.")

        elif theme_error:
            st.warning(theme_error)

        else:
            image_hash = hashlib.sha256(file_bytes).hexdigest()

            cache_key = (
                f"image::{image_hash}::{instruction}"
                f"::1024x1024::low"
            )

            cached_result = st.session_state["generation_cache"].get(cache_key)

            if cached_result is not None:
                st.session_state["last_image_generation"] = {
                    "original_image": image,
                    "instruction": instruction,
                    "theme": theme,
                    "bytes": cached_result["image_bytes"],
                    "pedagogical_content": cached_result.get(
                        "pedagogical_content",
                        {}
                    ),
                }

            else:
                temp_file_path = None
                result_data = {"bytes": None, "error": None}
                generation_done = threading.Event()

                try:
                    suffix = ".png"

                    if uploaded_name:
                        suffix = Path(uploaded_name).suffix or ".png"

                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                        tmp_file.write(file_bytes)
                        temp_file_path = tmp_file.name

                    def generate_image():
                        try:
                            result_data["bytes"] = edit_image_from_image(
                                temp_file_path,
                                instruction
                            )
                        except Exception as exc:
                            result_data["error"] = str(exc)
                        finally:
                            generation_done.set()

                    thread = threading.Thread(target=generate_image)
                    thread.start()

                    timer_placeholder = st.empty()

                    with st.spinner("Numérisation du schéma..."):
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
                            f"Erreur lors de la numérisation : {result_data['error']}"
                        )

                    else:
                        image_bytes = result_data["bytes"]

                        with st.spinner("Génération du contenu pédagogique..."):
                            pedagogical_content = (
                                generate_pedagogical_content_from_image(
                                    image_bytes
                                )
                            )

                        st.session_state["generation_cache"][cache_key] = {
                            "image_bytes": image_bytes,
                            "pedagogical_content": pedagogical_content,
                        }

                        st.session_state["last_image_generation"] = {
                            "original_image": image,
                            "instruction": instruction,
                            "theme": theme,
                            "bytes": image_bytes,
                            "pedagogical_content": pedagogical_content,
                        }

                except Exception as e:
                    st.error(f"Erreur lors de la numérisation : {str(e)}")

                finally:
                    if temp_file_path and Path(temp_file_path).exists():
                        Path(temp_file_path).unlink()

            if st.session_state["last_image_generation"] is not None:
                render_saved_image_generation(
                    st.session_state["last_image_generation"],
                    elapsed_time=elapsed
                )
                rendered_result = True

    if (
        not rendered_result
        and st.session_state["last_image_generation"] is not None
    ):
        render_saved_image_generation(
            st.session_state["last_image_generation"]
        )