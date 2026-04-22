import boto3
from datetime import datetime, timedelta

client = boto3.client('ce')

end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

response = client.get_cost_and_usage(
    TimePeriod={'Start': start_date, 'End': end_date},
    Granularity='DAILY',
    Metrics=['UnblendedCost']
    )

print(response)
data = response['ResultsByTime'][0]
cost_amount = round(float(data['Total']['UnblendedCost']['Amount']), 2)
cost_unit = data['Total']['UnblendedCost']['Unit']

print(f"Yesterday's spend: {cost_amount} {cost_unit}")

sns_client = boto3.client('sns', region_name='us-east-1')

TOPIC_ARN = "arn:aws:sns:us-east-1:542672133182:DailyCloudSpend"

message_body = f"Hey there, your AWS spend for yesterday was {cost_amount} {cost_unit}."
subject_line = f"Daily AWS cost: {cost_amount} {cost_unit}."

sns_response = sns_client.publish(
    TopicArn=TOPIC_ARN,
    Message=message_body,
    Subject=subject_line
)

print(f"Message sent! ID: {sns_response['MessageId']}")