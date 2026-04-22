# Automated AWS Cost Monitoring & Notification System

A few days into Adrian Cantrill's AWS Solutions Architect Associates course, I realized I was running up a suprising cost with the various instances and databases I was playing with. I like to expand on what I learn by making it bigger and better, or doing something new with it. To make sure my costs never became unmanagable, I decided to create this system.

## What it is
A serverless, event-driven tool designed to audit AWS cloud spend daily and provide automated alerts via email when budget thresholds are exceeded. This project demonstrates practical cloud financial management and automated system auditing.

![System Architecture](CostMonitorArchitecture.png)

## Architecture Overview

The system is built to be entirely hands-off, operating on a 100% serverless stack to ensure zero cost unless a notification is required.

* **Scheduler (Amazon EventBridge):** Functions as a "Cloud Cron" to trigger the audit cycle every 24 hours at a specified time.
* **Audit Logic (AWS Lambda):** A Python (Boto3) function that queries the **AWS Cost Explorer API** to retrieve unblended cost data for the previous 24-hour period.
* **Threshold Comparison:** The logic compares current spend against a user-defined threshold (e.g., $1.00).
* **Alerting (Amazon SNS):** If the threshold is breached, the system publishes a formatted alert to an SNS Topic.
* **Delivery:** Notifications are delivered instantly to a verified email subscription.

## Key Technical Features

* **Least-Privilege Security:** The Lambda execution role is strictly scoped to `ce:GetCostAndUsage` and `sns:Publish` permissions.
* **Boto3 Integration:** Deep integration with the AWS SDK for Python to parse complex JSON responses from the Cost Explorer.
* **Cost Efficiency:** Leverages the AWS Free Tier; the system incurs near-zero monthly operational costs.

## Repository Structure

* `lambda_function.py`: The core Python logic for cost retrieval and threshold checking.
* `main.tf`: Infrastructure as Code (IaC) to deploy the Lambda, EventBridge rules, and SNS topics.
* `policy.json`: The IAM policy defining the security boundaries for the cost auditor.

## Deployment

This system is deployed via **Terraform**. Simply initialize the workspace, update the threshold variable, and apply to secure your AWS environment against unexpected billing spikes.
