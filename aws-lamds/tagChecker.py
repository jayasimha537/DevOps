# IAM Role - EC2 read access and SNS access
# Required SNS topic arn as environment variable

import os
import boto3


def send_mail(message):
    sns = boto3.client('sns')
    response = sns.publish( TopicArn=os.environ['sns_arn'],Message=message,)
    print(response)
def lambda_handler(event, context):
    # TODO implement
    regions=['us-east-2','us-east-1']
    requiredTagsList=['Name','Project','in_use']
    for region in regions:
        tagLessInstanceList=[]
        ec2client = boto3.client('ec2',region_name=region)
        response = ec2client.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instanceTagsList=[]
                for tag in instance["Tags"]:
                     instanceTagsList.append(tag["Key"])
                flag = 1
                if(set(requiredTagsList).issubset(set(instanceTagsList))):
                    flag = 0
                if (flag):
                    tagLessInstanceList.append(instance["InstanceId"])
        if len(tagLessInstanceList) != 0:
            snsMessage="Region : " + region + " == > " + str(tagLessInstanceList)
            send_mail(snsMessage)