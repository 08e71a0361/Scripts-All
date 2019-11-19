import json
import boto3
import csv
from operator import itemgetter
#import datetime
from datetime import datetime, timedelta
import sys
s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
def lambda_handler(event, context):
    response = ec2.describe_volumes()
    InstanceId = []
    with open('/tmp/my2.csv','w+') as f:
        fieldnames = ['AvailabilityZone','InstanceId','Tags','VolumeId','KmsKeyId','Size','SnapshotId','CreateTime','Encrypted','State','InstanceAttachTime','Device','State','DeleteOnTermination']
        thewriter = csv.DictWriter(f,fieldnames=fieldnames) 
        thewriter.writeheader()
        now = datetime.utcnow()
        past = now - timedelta(minutes=30)
        future = now + timedelta(minutes = 10)
        for res in response['Volumes']:
            print(res['Size'])
            print(res['AvailabilityZone'])
            print(res['CreateTime'])
            print(res['Encrypted'])
            #print(res['KmsKeyId'])
            print(res['State'])
            print(res['VolumeId'])
            #print(res['Iops'])
            print(res['Tags'])
            print(res['SnapshotId'])
            Size= res['Size']
            AvailabilityZone= res['AvailabilityZone']
            CreateTime= res['CreateTime']
            Encrypted= res['Encrypted']
            if (str(Encrypted)=='False'):
                KmsKeyId = "Not Encrypted"
            else:
                KmsKeyId= res['KmsKeyId']
            State= res['State']
            VolumeId= res['VolumeId']
           # Iops= res['Iops']
            SnapshotId= res['SnapshotId']
            Tags = res['Tags']
            for data in res['Attachments']:
                print(data['InstanceId'])
                print(data['AttachTime'])
                print(data['Device'])
                print(data['State'])
                print(data['DeleteOnTermination'])
                
                InstanceId=data['InstanceId']
                AttachTime=data['AttachTime']
                Device=data['Device']
                StateOfVolume=data['State']
                DeleteOnTermination=data['DeleteOnTermination']
            
                thewriter.writerow({'AvailabilityZone':AvailabilityZone,'Tags':Tags,'InstanceId':InstanceId,'VolumeId':VolumeId,'KmsKeyId':KmsKeyId,'Size':Size,'SnapshotId':SnapshotId,'CreateTime':CreateTime,'Encrypted':Encrypted,'State':State,'InstanceAttachTime':AttachTime,'Device':Device,'State':StateOfVolume,'DeleteOnTermination':DeleteOnTermination})
    bucket_name = 'ebsinventory'
    s3.upload_file('/tmp/my2.csv','ebsinventory', str(datetime.now())+'NCaliforniavol.csv')
