import streamlit as st

from config.theme import (
    APP_NAME,
    TEXT_TO_IMAGE_ICON,
    IMAGE_TO_IMAGE_ICON
)

def render_home():
    
    st.title("🧬 "+APP_NAME)

    st.markdown("""
    Bienvenue dans cette application prototype intelligente de génération et de numérisation de schémas pédagogiques en SVT par le biais du modèle DALL·E d'OpenAI.

    Elle permet aux enseignants de tester deux scénarios :

    1. **Générer un schéma à partir d'un texte**
    2. **Numériser / améliorer un schéma à partir d'une image manuscrite**
    
    L'objectif est de fournir un support pédagogique adapté et de qualité pour les élèves, en facilitant la création et la numérisation de schémas SVT.
    """)

    st.markdown("---")

    st.subheader("🎯 Scénarios proposés")


    col1, col2 = st.columns(2)

    with col1:
        try:
            st.image(TEXT_TO_IMAGE_ICON, width=500)
        except Exception:
            st.markdown("## 📝")

        st.markdown("### Texte vers schéma")

        st.write("""
        L'enseignant décrit le schéma souhaité. L'application génère ensuite un schéma pédagogique adapté.
        """)

    with col2:
        try:
            st.image(IMAGE_TO_IMAGE_ICON, width=500)
        except Exception:
            st.markdown("## 🖼️")

        st.markdown("### Image vers schéma")

        st.write("""
        L'enseignant importe un schéma dessiné à la main. L'application le transforme en schéma numérique propre et lisible.
        """)

    st.markdown("---")

    st.subheader("✨ À propos du modèle DALL·E")

    st.write(
        "DALL·E est un modèle de génération d'images développé par OpenAI. Il permet de créer ou de réinterpréter des schémas pédagogiques "
        "à partir de descriptions textuelles et d'instructions visuelles."
    )

    st.write(
        "Dans cette application, DALL·E intervient dans les deux scénarios :"
    )

    st.markdown(
        "- **Texte vers schéma** : le modèle reçoit une description détaillée et construit un schéma pédagogique clair, annoté et adapté au niveau scolaire choisi.\n"
        "- **Image vers schéma** : le modèle reprend un dessin manuscrit et le transforme en un schéma numérique propre, structuré et prêt à être utilisé en cours."
    )

    st.write(
        "L'objectif est de profiter de la capacité de DALL·E à générer des images cohérentes et pédagogiques tout en simplifiant le travail de préparation des supports."
    )

    st.markdown(
        "[En savoir plus sur DALL·E](https://openai.com/dall-e-2)"
    )