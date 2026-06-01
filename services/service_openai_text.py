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
# HELPER FUNCTIONS
# =====================================

def extract_json_from_text(text: str) -> dict | None:
    """Extrait le JSON d'un texte qui pourrait contenir du contenu supplémentaire."""
    # Chercher le premier { et le dernier }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        try:
            json_str = text[start_idx:end_idx + 1]
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    return None


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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    response_text = response.choices[0].message.content
    
    # Essayer d'abord un parsing direct
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Si ça échoue, essayer d'extraire le JSON du texte
    extracted = extract_json_from_text(response_text)
    if extracted:
        return extracted
    
    # Fallback : retourner le texte brut comme explication
    return {
        "explication": response_text,
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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": image_data_uri}}
                ]
            }
        ],
        temperature=0.3
    )

    response_text = response.choices[0].message.content
    
    # Essayer d'abord un parsing direct
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Si ça échoue, essayer d'extraire le JSON du texte
    extracted = extract_json_from_text(response_text)
    if extracted:
        return extracted
    
    # Fallback : retourner le texte brut comme explication
    return {
        "explication": response_text,
        "objectifs_pedagogiques": [],
        "competences_visees": [],
        "notions_cles": [],
        "resume": "",
        "questions": [],
        "reponses": []
    }
