import streamlit as st

from config.theme import APP_NAME, LOGO_PATH, ENTREVUE_LINK


def render_sidebar():
    with st.sidebar:
        try:
            st.image(LOGO_PATH, width=250)
        except Exception:
            st.markdown("## 🧬")

        st.title(APP_NAME)

        st.markdown("---")

        page = st.radio(
            "Navigation",
            [
                "🏠 Accueil",
                "📝 Texte vers schéma",
                "🖼️ Image vers schéma"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        st.markdown("### À propos")
        st.write(
            "Prototype d'interface pour la génération et la numérisation "
            "de schémas pédagogiques en SVT."
        )

        st.markdown("---")

        st.link_button("📩 Entrevue", ENTREVUE_LINK)

    return page