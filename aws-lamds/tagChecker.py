# IAM Role - EC2 read access and SNS access
# Required SNS topic arn as environment variable

import os
import boto3
import yaml

sns_arnList = []
regions = []
requiredTagsList = []

def read_yaml_input():
    global regions,sns_arnList,requiredTagsList
    with open(r'./sns_arn.yml') as file:
        sns_arnList = yaml.full_load(file)
    with open(r'./regions.yml') as file:
        regions = yaml.full_load(file)
    with open(r'./tags.yml') as file:
        requiredTagsList =  yaml.full_load(file)

def send_mail(message):
    sns = boto3.client('sns')
    response = sns.publish( TopicArn=sns_arnList[0],Message=message,)
    print(response)
def lambda_handler(event, context):
    # TODO implement
    read_yaml_input()
    for region in regions["regions"]:
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