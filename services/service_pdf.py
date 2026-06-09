from io import BytesIO
from PIL import Image

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as RLImage,
    PageBreak
)


def generate_schema_pdf(
    image_bytes: bytes,
    input_data: dict,
    optimized_prompt: str,
    pedagogical_content: dict
) -> bytes:

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Contenu pédagogique : {input_data['theme']}", styles["Title"]))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("1. Schéma pédagogique", styles["Heading2"]))

    img_buffer = BytesIO(image_bytes)
    img = Image.open(img_buffer)
    img_width, img_height = img.size

    max_width = 20 * cm
    max_height = 16 * cm
    ratio = min(max_width / img_width, max_height / img_height)

    story.append(
        RLImage(
            BytesIO(image_bytes),
            width=img_width * ratio,
            height=img_height * ratio
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("2. Explication du schéma", styles["Heading2"]))
    story.append(Paragraph(pedagogical_content.get("explication", ""), styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("3. Résumé simplifié", styles["Heading2"]))
    story.append(Paragraph(pedagogical_content.get("resume", ""), styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("4. Objectifs pédagogiques", styles["Heading2"]))
    for obj in pedagogical_content.get("objectifs_pedagogiques", []):
        story.append(Paragraph(f"- {obj}", styles["Normal"]))

    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("5. Compétences visées", styles["Heading2"]))
    for comp in pedagogical_content.get("competences_visees", []):
        story.append(Paragraph(f"- {comp}", styles["Normal"]))

    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("6. Notions clés", styles["Heading2"]))
    for notion in pedagogical_content.get("notions_cles", []):
        story.append(Paragraph(f"- {notion}", styles["Normal"]))

    story.append(PageBreak())

    story.append(Paragraph("7. Questions pédagogiques et réponses attendues", styles["Heading2"]))

    questions = pedagogical_content.get("questions", [])
    reponses = pedagogical_content.get("reponses", [])

    for i, question in enumerate(questions):
        story.append(Paragraph(f"Question {i + 1} : {question}", styles["Heading3"]))

        if i < len(reponses):
            story.append(Paragraph(f"Réponse attendue : {reponses[i]}", styles["Normal"]))

        story.append(Spacer(1, 0.3 * cm))

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()