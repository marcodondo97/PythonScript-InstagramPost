import requests
import datetime
import boto3
import os
import json
import base64
from ayrshare import SocialPost
from dotenv import load_dotenv

load_dotenv()

def generate_instagram_post():
    """Genera e pubblica contenuto su Instagram"""
    print("Starting Instagram post generation")
    try:
        stability_key = os.environ['STABILITY_API_KEY']
        ayrshare_key = os.environ['AYRSHARE_KEY']
        bucket_name = os.environ['S3_BUCKET_NAME']
        huggingface_key = os.environ['HUGGINGFACE_API_KEY']

        print("Credentials loaded")

        # 1️⃣ Genera storia
        print("Generating story...")
        story_response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {huggingface_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-120b:nscale",
                "messages": [{"role": "user", "content": "tell me a random story in maximum 200 characters"}],
                "parameters": {"max_new_tokens": 50},
                "stream": False
            },
            timeout=30
        )
        if story_response.status_code != 200:
            raise Exception(f"Hugging Face error: {story_response.text}")
        story = story_response.json()["choices"][0]["message"]["content"].strip()
        print(f"Story generated: {story[:50]}...")

        # 2️⃣ Genera immagine
        print("Generating image...")
        image_response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Authorization": f"Bearer {stability_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json={
                "text_prompts": [{"text": story, "weight": 1}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30
            },
            timeout=60
        )
        if image_response.status_code != 200:
            raise Exception(f"Stability AI error: {image_response.text}")
        img_data = base64.b64decode(image_response.json()["artifacts"][0]["base64"])
        print("Image generated")

        # 3️⃣ Upload su S3
        print("Uploading to S3...")
        current_timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M")
        s3_key = f"img/image_{current_timestamp}.jpg"
        s3_client = boto3.client('s3')
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=img_data,
            ContentType='image/jpeg'
        )
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
        print(f"Image uploaded: {image_url}")

        # 4️⃣ Post su Instagram
        print("Posting to Instagram...")
        social = SocialPost(ayrshare_key)
        result = social.post({
            'post': story,
            'platforms': ['instagram'],
            'mediaUrls': [image_url]
        })
        print("Post published successfully")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "story": story,
                "image_url": image_url
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }

# 🔹 Entry point per AWS Lambda
def lambda_handler(event, context):
    return generate_instagram_post()