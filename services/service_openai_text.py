import os
import json
import base64

from openai import OpenAI
from dotenv import load_dotenv

# =====================================
# API KEY
# =====================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =====================================
# TEXT TO IMAGE
# =====================================

def generate_pedagogical_content_from_prompt(optimized_prompt: str) -> dict:

    system_prompt = """
Tu es un assistant pédagogique expert en Sciences de la Vie et de la Terre.
Tu produis des contenus clairs, fiables, structurés et adaptés au niveau scolaire demandé.
Tu dois répondre uniquement en JSON valide.
"""

    user_prompt = f"""
Voici le prompt optimisé utilisé pour générer un schéma pédagogique SVT avec DALL·E :

{optimized_prompt}

À partir de ce prompt, génère un contenu pédagogique associé au schéma.

Retourne exactement un JSON avec cette structure :

{{
  "explication": "Une explication détaillée du schéma, claire et adaptée au niveau scolaire.",
  "objectifs_pedagogiques": [
    "Objectif pédagogique 1",
    "Objectif pédagogique 2",
    "Objectif pédagogique 3"
  ],
  "competences_visees": [
    "Compétence visée 1",
    "Compétence visée 2",
    "Compétence visée 3"
  ],
  "notions_cles": [
    "Notion clé 1",
    "Notion clé 2",
    "Notion clé 3",
    "Notion clé 4",
    "Notion clé 5"
  ],
  "resume": "Un résumé simple et court destiné aux élèves.",
  "questions": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ],
  "reponses": [
    "Réponse attendue 1",
    "Réponse attendue 2",
    "Réponse attendue 3",
    "Réponse attendue 4",
    "Réponse attendue 5"
  ]
}}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    try:
        return json.loads(response.output_text)

    except json.JSONDecodeError:
        return {
            "explication": response.output_text,
            "objectifs_pedagogiques": [],
            "competences_visees": [],
            "notions_cles": [],
            "resume": "",
            "questions": [],
            "reponses": []
        }
    

# =====================================
# IMAGE TO IMAGE
# =====================================

def generate_pedagogical_content_from_image(image_bytes: bytes) -> dict:

    system_prompt = """
Tu es un assistant pédagogique expert en Sciences de la Vie et de la Terre.
Tu analyses des schémas pédagogiques et tu produis des contenus clairs, fiables, structurés et adaptés au niveau scolaire approprié.
Tu dois répondre uniquement en JSON valide.
"""

    user_prompt = """
Voici une image de schéma pédagogique numérisé.
Analyse le contenu de ce schéma et génère un contenu pédagogique associé.

Retourne exactement un JSON avec cette structure :

{
  "explication": "Une explication détaillée du schéma, claire et adaptée au niveau scolaire.",
  "objectifs_pedagogiques": [
    "Objectif pédagogique 1",
    "Objectif pédagogique 2",
    "Objectif pédagogique 3"
  ],
  "competences_visees": [
    "Compétence visée 1",
    "Compétence visée 2",
    "Compétence visée 3"
  ],
  "notions_cles": [
    "Notion clé 1",
    "Notion clé 2",
    "Notion clé 3",
    "Notion clé 4",
    "Notion clé 5"
  ],
  "resume": "Un résumé simple et court destiné aux élèves.",
  "questions": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ],
  "reponses": [
    "Réponse attendue 1",
    "Réponse attendue 2",
    "Réponse attendue 3",
    "Réponse attendue 4",
    "Réponse attendue 5"
  ]
}
"""

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_data_uri = f"data:image/png;base64,{image_base64}"

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": user_prompt},
                    {"type": "input_image", "image_url": image_data_uri}
                ]
            }
        ],
        temperature=0.3
    )

    try:
        return json.loads(response.output_text)

    except json.JSONDecodeError:
        return {
            "explication": response.output_text,
            "objectifs_pedagogiques": [],
            "competences_visees": [],
            "notions_cles": [],
            "resume": "",
            "questions": [],
            "reponses": []
        }
