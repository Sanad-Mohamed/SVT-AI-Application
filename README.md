# 🧬 SVT AI Application

Application Streamlit de génération et de numérisation de schémas pédagogiques en Sciences de la Vie et de la Terre (SVT) basée sur les modèles d'intelligence artificielle d'OpenAI.

## 📖 Présentation

Cette application a été développée afin d'aider les enseignants à produire rapidement des supports pédagogiques visuels de qualité.

L'application propose deux fonctionnalités principales :

- 📝 **Texte vers schéma** : génération automatique d'un schéma pédagogique à partir d'une description textuelle.
- 🖼️ **Image vers schéma** : transformation et amélioration d'un schéma manuscrit ou d'une image existante en un schéma numérique propre et lisible.

En complément, l'application génère automatiquement un contenu pédagogique associé comprenant :

- Une explication détaillée du schéma
- Un résumé simplifié
- Des objectifs pédagogiques
- Des compétences visées
- Des notions clés
- Des questions pédagogiques
- Des réponses attendues

Les utilisateurs peuvent également télécharger un rapport PDF regroupant le schéma généré et l'ensemble du contenu pédagogique associé.

---

## 🚀 Fonctionnalités

### 📝 Texte vers schéma

- Saisie d'un thème pédagogique
- Description détaillée du schéma souhaité
- Choix du niveau scolaire
- Choix de la langue
- Choix du niveau de détail
- Génération d'un schéma pédagogique via DALL·E
- Génération automatique de contenus pédagogiques associés
- Export PDF

### 🖼️ Image vers schéma

- Import d'une image (PNG, JPG, JPEG)
- Transformation d'un schéma manuscrit en schéma numérique
- Amélioration visuelle du schéma
- Génération automatique de contenus pédagogiques à partir du schéma obtenu
- Export PDF

---

## 🏗️ Architecture du projet

```text
.
├── app.py
├── assets/
│   ├── icons/
│   └── logos/
├── components/
├── config/
├── services/
├── utils/
├── views/
├── requirements.txt
└── README.md
```

---

## 🤖 Technologies utilisées

### Frontend

- Streamlit

### Intelligence Artificielle

- GPT-Image-2
- GPT-4.1 Mini

### Traitement d'images

- Pillow (PIL)

### Génération de documents

- ReportLab

### Gestion de configuration

- python-dotenv

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration

Créer un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Lancement de l'application

```bash
streamlit run app.py
```

L'application sera disponible à l'adresse :

```text
http://localhost:8501
```

---

## 🎯 Cas d'usage

Cette application est destinée principalement à :

- Enseignants de SVT
- Formateurs
- Concepteurs de contenus pédagogiques
- Institutions éducatives
- Acteurs de la transformation numérique de l'éducation

---

## 📚 Résumé du projet

Ce projet porte sur l'utilisation de l'intelligence artificielle générative pour la création et la numérisation de schémas pédagogiques en Sciences de la Vie et de la Terre.

---

## 👨‍💻 Auteur

**Mohamed SANAD**

Data Scientist & AI Engineer

Télécom Paris • ENSIAS