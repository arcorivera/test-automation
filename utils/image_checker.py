import requests
from PIL import Image
import imagehash
from io import BytesIO
import openai
import os

# Set your OpenAI API Key securely (assumes you set this in your system environment)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to check if an image is valid (not broken)
def check_image_validity(image_url):
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.verify()  # Checks if the image is corrupted or broken
            hash_value = imagehash.phash(img)  # perceptual hash for duplicates
            return hash_value
        else:
            return None
    except Exception:
        return None

# Function to detect duplicates based on image hashes
def detect_duplicates(image_hashes):
    seen_hashes = set()
    duplicates = []
    for hash_value in image_hashes:
        if hash_value in seen_hashes:
            duplicates.append(hash_value)
        seen_hashes.add(hash_value)
    return duplicates

# Function to send image to OpenAI for AI-powered insights
def analyze_image_with_openai(image_url):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Analyze this image and tell me if anything seems off."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI Analysis Error: {e}"

# Combined AI-powered image issue detection
def ai_detect_issues(image_urls):
    image_hashes = [check_image_validity(url) for url in image_urls]

    duplicates = detect_duplicates(image_hashes)
    broken_images = [url for url, hash_value in zip(image_urls, image_hashes) if hash_value is None]

    # AI Insights via OpenAI
    openai_insights = []
    for url in image_urls:
        insight = analyze_image_with_openai(url)
        openai_insights.append(f"Image: {url}\nInsight: {insight}\n")

    report = (
        f"Broken Images: {broken_images}\n"
        f"Duplicate Image Hashes: {duplicates}\n\n"
        f"OpenAI Insights:\n" + "\n".join(openai_insights)
    )
    return report
