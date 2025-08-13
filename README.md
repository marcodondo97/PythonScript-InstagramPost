# Instagrampost

## Introduction

This application automatically generates and publishes Instagram posts by creating random stories using AI, generating corresponding images, and posting them to Instagram. The system integrates multiple AI services to create engaging content without manual intervention.

## Description

The Instagram Post Generator is a Python-based application that leverages AWS Lambda for serverless execution. It combines multiple AI services to create complete Instagram posts:

- **Story Generation**: Uses Hugging Face's GPT model to generate random stories in under 200 characters
- **Image Generation**: Creates AI-generated images based on the story using Stability AI's Stable Diffusion XL
- **Cloud Storage**: Uploads generated images to AWS S3 for public access
- **Social Media Publishing**: Posts content to Instagram using Ayrshare's API

The application is designed to run both locally for testing and on AWS Lambda for production deployment.

### Getting Started

To run this application locally, follow these steps:

**Clone the repository**
```bash
git clone <repository-url>
cd instagrampost
```

**Configure Instagram Profile**
Set up your Instagram account and ensure it's ready for API access through Ayrshare.

**Obtain API Keys**
You need to obtain API keys from the following services:
- [Hugging Face](https://huggingface.co/settings/tokens) API key for story generation
- [Stability AI](https://platform.stability.ai/) API key for image generation
- [Ayrshare](https://ayrshare.com/) API key for Instagram posting

**Create Public S3 Bucket**
Create an [AWS S3](https://aws.amazon.com/s3/) bucket with public read access to store generated images. Configure appropriate CORS settings for web access.

**Configure Environment Variables**
Copy the example environment file and populate it with your API keys:
```bash
cp example.env .env
```

Edit the `.env` file with your actual API credentials:
```
STABILITY_API_KEY=your_stability_api_key
AYRSHARE_KEY=your_ayrshare_api_key
S3_BUCKET_NAME=your_s3_bucket_name
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

**Run the Script Locally**
Execute the script using Python:
```bash
pip install -r requirements.txt
python -c "from lambda_function import generate_instagram_post; result = generate_instagram_post(); print(result)"
```

## Deploy

[Deployment instructions will be added here]
