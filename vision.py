import base64
import json
import os
from io import BytesIO

import openai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
IMG_RES = 1080

with open("./prompts/get_actions.txt") as f:
    prompt_get_actions = f.read()

# Function to encode the image
def encode_and_resize(image):
    W, H = image.size
    image = image.resize((IMG_RES, int(IMG_RES * H / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

# 次のアクションを考える
def get_actions(screenshot, objective):
    encoded_screenshot = encode_and_resize(screenshot)
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_get_actions.replace("{objective}", objective),
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_screenshot}", # 画像の入力
                        },
                    },
                ],
            }
        ],
        max_tokens=100,
    )

    try:
        json_response = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print("Error: Invalid JSON response")
        cleaned_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant to fix an invalid JSON response. You need to fix the invalid JSON response to be valid JSON. You must respond in JSON only with no other fluff or bad things will happen. Do not return the JSON inside a code block."},
                {"role": "user", "content": f"The invalid JSON response is: {response.choices[0].message.content}"}
            ]
        )
        try: cleaned_json_response = json.loads(cleaned_response.choices[0].message.content)
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            return {}
        return cleaned_json_response

    return json_response


if __name__ == "__main__":
    image = Image.open("image.png")
    actions = get_actions(image, "upvote the pinterest post")
