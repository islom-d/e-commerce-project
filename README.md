# AWS E-Commerce Project Deployment

This GitHub Action named **Deploy to AWS** is designed to streamline the deployment of AWS resources using AWS CloudFormation. The action orchestrates several tasks including linting Python code, creating an S3 bucket, uploading Lambda function code to the S3 bucket, and deploying AWS resources using AWS CloudFormation.

## Table of Contents

- [Workflow Overview](#workflow-overview)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Workflow Details](#workflow-details)

## Workflow Overview

### Trigger:
  - Push events to the `main` branch.
  - Manual trigger using `workflow_dispatch`.

### Jobs:
  1. **lint:**
     - Linting Python code with a specified Python version.
  2. **create_bucket:**
     - Creating an S3 bucket using AWS CloudFormation.
  3. **upload_lambda:**
     - Uploading Lambda function code to the S3 bucket.
  4. **create_app:**
     - Deploying AWS resources using another AWS CloudFormation stack.

### Environment Variables:
  - `AWS_REGION`: Preferred AWS region (Default: `us-east-2`).

```yaml

# Excerpt from .github/workflows/deploy_to_aws.yml
name: Deploy to AWS
on:
  push:
    branches:
      - main
  workflow_dispatch:
env:
  AWS_REGION: us-east-2
```

## Prerequisites

### 1. AWS IAM User
Create an AWS IAM user with programmatic access and the necessary permissions to create and manage AWS resources such as S3, Lambda, and CloudFormation. Store the access key ID and secret access key securely.

### 2. GitHub Repository Secrets
Add the IAM user's `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to your repository's secrets. These secrets authenticate the workflow to perform actions on AWS resources.

### 3. AWS Region and Notification Email
Specify your preferred AWS region and your email in the AWS CloudFormation template. The email is used to receive notifications related to AWS CloudFormation stacks.

#### Setup Steps:
   1. Navigate to AWS IAM and create a user with the required permissions.
   2. Configure the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your GitHub repository secrets.
   3. Update the AWS region and your email in the AWS CloudFormation template if needed.

## Usage

1. **Clone the Repository:**
   Fork or clone this repository.
2. **Update Region and Email:**
   Optionally, modify the AWS region in the workflow file and email in the CloudFormation template.
3. **Trigger the Workflow:**
   Push changes to the `main` branch or manually trigger the workflow from the GitHub Actions tab.
4. **Monitor the Progress:**
   Monitor the workflow progress and review logs in the `Actions` tab of your repository.

## Workflow Details

### Lint Job
- Utilizes Python 3.11.
- Performs linting to identify code errors and ensure code quality.

### Create Bucket Job
- Executes AWS CloudFormation to initialize an S3 bucket for Lambda function code.
- Extracts and outputs the bucket name.

### Upload Lambda Job
- Compresses and uploads the Lambda function code to the designated S3 bucket.

### Create App Job
- Utilizes AWS CloudFormation to deploy the remaining resources of the eCommerce application.

