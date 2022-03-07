import json
import requests

def lambda_handler(event, context):
    sns_payload = event['Records'][0]['Sns']
    sns_message = json.loads(sns_payload['Message'])
    try:
        message = {'text': sns_message['message']}
        sns_headers = {
            "x-amz-sns-message-id": sns_payload['MessageId'],
            "x-amz-sns-message-type": sns_payload["Type"],
            "x-amz-sns-subscription-arn" : event["Records"][0]["EventSubscriptionArn"],
            "x-amz-sns-topic-arn" : sns_payload["TopicArn"],
            'content-type': 'application/json',
            'User-Agent': "shamirhusein.my.id"
        }
        r = requests.post(url = sns_message['slack_webhook_url'], data = json.dumps(message), headers = sns_headers)
        if  r.status_code == 200: 
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": sns_payload['MessageId'], 
                    "payload": sns_payload
                }),
            }
        else: 
            r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except Exception as e:
        raise SystemExit(err)
 