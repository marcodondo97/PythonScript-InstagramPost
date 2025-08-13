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
git clone https://github.com/marcodondo97/PythonScript-instagrampost.git
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

### AWS Lambda Deployment

This section explains how to deploy the application to [AWS Lambda](https://aws.amazon.com/lambda/) for automated execution and how to schedule it using [AWS EventBridge](https://aws.amazon.com/eventbridge/).

#### Prerequisites
- AWS CLI configured with appropriate permissions
- Python 3.8+ installed locally
- AWS S3 bucket already created and configured

#### Step 1: Prepare Deployment Package

Install dependencies and create the deployment package:

```bash
# Install dependencies in current directory
pip install requests boto3 python-dotenv social-post-api -t .

# Create deployment ZIP file
zip -r ../lambda_instagram.zip .
```

#### Step 2: Create Lambda Function

1. Go to AWS Lambda Console
2. Click "Create function"
3. Choose "Author from scratch"
4. Set function name: `instagrampost`
5. Runtime: Python 3.9 or later
6. Architecture: x86_64
7. Click "Create function"

#### Step 3: Configure Environment Variables

In the Lambda function configuration, add these environment variables:

```
STABILITY_API_KEY=your_stability_api_key
AYRSHARE_KEY=your_ayrshare_api_key
S3_BUCKET_NAME=your_s3_bucket_name
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

#### Step 4: Set IAM Permissions

Create or update the Lambda execution role with the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:us-east-1:YOUR_ACCOUNT_ID:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:logs:us-east-1:YOUR_ACCOUNT_ID:log-group:/aws/lambda/instagrampost:*",
                "arn:aws:s3:::YOUR_BUCKET_NAME/img/*"
            ]
        }
    ]
}
```

Replace `YOUR_ACCOUNT_ID` with your AWS account ID and `YOUR_BUCKET_NAME` with your S3 bucket name.

#### Step 5: Upload Deployment Package

1. In the Lambda function console, go to "Code" tab
2. Click "Upload from" → ".zip file"
3. Upload the `lambda_instagram.zip` file
4. Click "Save"

#### Step 6: Test the Function

1. Go to "Test" tab in Lambda console
2. Create a new test event (empty JSON `{}`)
3. Click "Test" to verify the function works correctly

#### Step 7: Configure EventBridge Schedule

1. Go to AWS EventBridge Console
2. Create a new rule:
   - Name: `instagrampost-schedule`
   - Rule type: Schedule
   - Define schedule: Cron expression
   - Example for daily at 9 AM UTC: `0 9 * * ? *`
3. Target: Lambda function
4. Function: `instagrampost`
5. Click "Create"

The function will now automatically execute according to your schedule.
