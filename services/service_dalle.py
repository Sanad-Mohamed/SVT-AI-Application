import os
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

def generate_image_from_text(
    prompt: str,
    size: str = "1024x1024",
    quality: str = "low"
):

    try:

        result = client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            size=size,
            quality=quality
        )

        image_base64 = result.data[0].b64_json

        image_bytes = base64.b64decode(image_base64)

        return image_bytes

    except Exception as e:

        raise Exception(
            f"Erreur génération text-to-image : {str(e)}"
        )


# =====================================
# IMAGE TO IMAGE
# =====================================

def edit_image_from_image(
    image_path: str,
    prompt: str,
    size: str = "1024x1024",
    quality: str = "low"
):

    try:

        with open(image_path, "rb") as image_file:

            result = client.images.edit(
                model="gpt-image-2",
                image=image_file,
                prompt=prompt,
                size=size,
                quality=quality
            )

        image_base64 = result.data[0].b64_json

        image_bytes = base64.b64decode(image_base64)

        return image_bytes

    except Exception as e:

        raise Exception(
            f"Erreur génération image-to-image : {str(e)}"
        )