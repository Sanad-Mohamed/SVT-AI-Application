import streamlit as st

from views.sidebar import render_sidebar
from config.theme import APP_NAME, APP_ICON

from views.home import render_home
from views.text_to_image import render_text_to_image
from views.image_to_image import render_image_to_image

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide"
)

page = render_sidebar()

if page == "🏠 Accueil":
    render_home()

elif page == "📝 Texte vers schéma":
    render_text_to_image()

elif page == "🖼️ Image vers schéma":
    render_image_to_image()