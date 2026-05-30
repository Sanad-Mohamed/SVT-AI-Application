import re


def is_probably_gibberish(text: str) -> bool:
    text = text.strip().lower()

    if len(text) < 3:
        return True

    # Trop peu de voyelles = souvent texte aléatoire
    vowels = sum(1 for c in text if c in "aeiouyàâéèêëîïôùûü")
    if vowels / max(len(text), 1) < 0.2:
        return True

    # Trop de répétitions bizarres
    if re.search(r"(.)\1{3,}", text):
        return True

    return False


def validate_prompt_data(theme: str, prompt: str):
    errors = []

    if not theme.strip():
        errors.append("Veuillez saisir un thème.")

    if not prompt.strip():
        errors.append("Veuillez saisir une description.")

    if theme.strip() and is_probably_gibberish(theme):
        errors.append("Le thème semble incorrect ou incompréhensible.")

    if prompt.strip() and len(prompt.strip()) < 15:
        errors.append("La description est trop courte. Veuillez ajouter plus de détails.")

    if prompt.strip() and is_probably_gibberish(prompt):
        errors.append("La description semble incorrecte ou incompréhensible.")

    return errors


def validate_theme(theme: str):
    if not theme.strip():
        return "Veuillez saisir un thème."

    if theme.strip() and is_probably_gibberish(theme):
        return "Le thème semble incorrect ou incompréhensible."

    return None


def build_optimized_prompt(data: dict) -> str:
    return f"""
Créer un schéma pédagogique clair et scientifiquement correct en SVT.

Thème : {data["theme"]}
Niveau scolaire : {data["niveau"]}
Langue : {data["language"]}
Niveau de détail : {data["niveau_detail"]}

Consignes pédagogiques :
- Le schéma doit être lisible et adapté au niveau {data["niveau"]}.
- {"Ajouter des annotations claires." if data["presence_annotations"] else "Ne pas inclure d'annotations."}
- Utiliser des couleurs pédagogiques.
- Organiser les éléments de manière simple et compréhensible.
- Éviter les erreurs scientifiques.
- Ne pas surcharger le schéma.

Description demandée par l'enseignant :
{data["prompt"]}
""".strip()